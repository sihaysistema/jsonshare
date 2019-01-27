# -*- coding: utf-8 -*-
# Copyright (c) 2019, SHS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
import requests
import os

# Permite trabajar con acentos, ñ, simbolos, etc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@frappe.whitelist()
def obtener_datos(item, usuario, doctype):
    '''Obtiene la informacion a ser enviada'''
    if doctype == 'Item':
        try:
            item_data = frappe.db.get_values('Item',
                                            filters={'item_code': item},
                                            fieldname=['item_code', 'item_name',
                                                        'item_group', 'stock_uom',
                                                        'standard_rate', 'description',
                                                        'is_stock_item'], as_dict=1)
            preparar_json_item(usuario, item_data)
        except:
            frappe.msgprint(_('Error al obtener informacion de Item'))
    
    if doctype == 'Customer':
        try:
            # Obtiene informacion de Customer
            customer_data = frappe.db.get_values('Customer',
                                                 filters={'customer_name': item},
                                                 fieldname=['customer_name', 'territory',
                                                            'customer_group', 'customer_type'], as_dict=1)
            # Obtiene las direcciones con relacion al cliente
            dynamic_table = frappe.db.get_values('Dynamic Link',
                                                 filters={'link_name': item, 'link_doctype': 'Customer',
                                                          'parenttype': 'Address'},
                                                 fieldname=['parent'], as_dict=1)
            # Obtiene los contactos con relacion al cliente
            dynamic_table_contacts = frappe.db.get_values('Dynamic Link',
                                                          filters={'link_name': item, 'link_doctype': 'Customer',
                                                                   'parenttype': 'Contact'},
                                                          fieldname=['parent'], as_dict=1)

            n_address = len(dynamic_table)
            customer_address = []
            for i in range(0, n_address):
                # Obtiene las direcciones
                customer_address_data = frappe.db.get_values('Address',
                                                        filters={'name': dynamic_table[i]['parent']},
                                                        fieldname=['email_id', 'county', 'city',
                                                                   'address_line1', 'state', 'address_type',
                                                                   'address_title', 'phone', 'country'], as_dict=1)
                # Crea un array con todas las direcciones encontradas
                customer_address.append(customer_address_data)

            # Obtiene los contactos
            n_contact = len(dynamic_table_contacts)
            contact = []
            for i in range(0, n_contact):
                contact_data = frappe.db.get_values('Contact',
                                                    filters={'name': dynamic_table_contacts[i]['parent']},
                                                    fieldname=['email_id', 'first_name', 'last_name',
                                                               'phone', 'mobile_no'], as_dict=1)
                # Crea un array con todos los contactos encontrados
                contact.append(contact_data)

            # Funcion para preparar informacion y mandarla
            preparar_json_customer(usuario, customer_data, customer_address, contact)
        except:
            frappe.msgprint(_('Error al obtener informacion de Customer'))


def preparar_json_customer(usuario, customer_data, customer_address, contact):
    '''Carga a una estructura JSON los datos a enviar'''
    template_data = {}
    template_data['key'] = 'hash'
    template_data['doctype'] = 'Customer'

    doctype_fields = {}
    # Customer Data
    doctype_fields['fields'] = customer_data[0]
    doctype_fields['addresses'] = []
    doctype_fields['contacts'] = []

    for i in customer_address:
        doctype_fields['addresses'].append(i[0])

    for i in contact:
        doctype_fields['contacts'].append(i[0])

    template_data['data'] = doctype_fields
    # Carga la informacion a JSON string
    json_data = json.dumps(template_data)

    # Funcion encargada de enviar la informacion
    # Se le debe pasar la informacion con json.dumps(data)
    compartir_datos(json_data, usuario)


def preparar_json_item(usuario, item_data):
    '''Carga a una estructura JSON los datos a enviar para Item'''
    template_data = {}
    template_data['key'] = 'hash'
    template_data['doctype'] = 'Item'

    doctype_fields = {}
    # Customer Data
    doctype_fields['fields'] = item_data[0]

    template_data['data'] = doctype_fields
    # Carga la informacion a JSON string
    json_data = json.dumps(template_data)

    # Funcion encargada de enviar la informacion
    # Se le debe pasar la informacion con json.dumps(data)
    compartir_datos(json_data, usuario)


def compartir_datos(json_data, usuario):
    '''Comparte la informacion por HTTP/S, debe recibir la informacion con
        json.dumps(data)'''
    # Obtiene la single table el metodo a ejecutar
    # Parametro 1 : Nombre doctype, Parametro 2: Nombre campo, parametro 3: deshabilida cache
    metodo_api = frappe.db.get_single_value('Configuracion JsonShare', 'nombre', cache=False)
    url = '{0}/{1}'.format(usuario, metodo_api)

    frappe.msgprint(_(url))
    frappe.msgprint(_(json_data))
    try:
        # Manda data como json string
        r = requests.post(url, data=json_data)
    except:
        frappe.msgprint(_('Error En la comunicacion'))
    else:
        # Codigo de estado
        frappe.msgprint(_(r.status_code))
        # Contenido de la respuesta
        frappe.msgprint(_(r.content))


# Metodos para guardar data recibida REST-API
# Customer
def create_customer(data_customer):
    data = data_customer

    message_exists = 'The name of that customer already exists'

    if data['doctype'] == 'Customer':
        # Cargamos todos los campos
        customer_json = data['data']
        # Cargamos los campos de customer
        customer_fields = customer_json['fields']

        if not frappe.db.exists('Customer', _(customer_fields.get('customer_name'))):
            new_customer = frappe.new_doc("Customer")

            if not create_territory(_(customer_fields['territory'])):
                new_customer.territory = customer_fields['territory']

            if not create_customer_group(_(customer_fields.get('customer_group'))):
                new_customer.customer_group = customer_fields.get('customer_group')

            new_customer.customer_group = 'All Customer Groups'
            new_customer.customer_name = customer_fields.get('customer_name')
            new_customer.customer_type = customer_fields.get('customer_type')
            new_customer.save(ignore_permissions=True)
        else:
            return message_exists

        # Cargamos el array de direcciones
        customer_addresses = customer_json['addresses']
        if not create_address_from_array(customer_addresses):
            pass
            # do nothing

        customer_contacts = customer_json['contacts']
        if not create_contact_from_array(customer_contacts):
            pass


def create_territory(territory_name):
    if not frappe.db.exists('Territory', _(territory_name)):
        new_territory = frappe.new_doc("Territory")
        new_territory.territory_name = _(territory_name)
        parent_territory = frappe.db.get_values('Territory',
                                                filters={'parent_territory': ""},
                                                fieldname=['name'], as_dict=1)
        new_territory.parent_territory = parent_territory[0]['name']
        new_territory.save(ignore_permissions=True)
    else:
        return false


def create_customer_group(customer_group_name):
    if not frappe.db.exists('Customer Group', _(customer_group_name)):
        new_customer_group = frappe.new_doc("Customer Group")
        new_customer_group.customer_group_name = _(customer_group_name)
        customer_group_parent = frappe.db.get_values('Customer Group',
                                                filters={'parent_customer_group': ""},
                                                fieldname=['name'], as_dict=1)
        new_customer_group.parent_customer_group = customer_group_parent[0]['name']
        new_customer_group.save(ignore_permissions=True)
    else:
        return false


def create_address_from_array(customer_addresses):
    for i in customer_addresses:
        doc = i
        if not frappe.db.exists('Address', _(doc['address_title'])):
            new_address = frappe.new_doc("Address")
            new_address.address_title = _(doc['address_title'])
            new_address.address_type = _(doc['address_type'])
            new_address.address_line1 = _(doc['address_line1'])
            new_address.city = _(doc['city'])
            new_address.save(ignore_permissions=True)
        else:
            return false


def create_contact_from_array(contacts):
    for i in contacts:
        doc = i
        #  Verificar como buscar el titulo del contacto, no solo el nombre
        if not frappe.db.exists('Contact', _(doc['first_name'])):
            new_contact = frappe.new_doc("Contact")
            new_contact.first_name = _(doc['first_name'])
            new_contact.last_name = _(doc['last_name'])
            new_contact.mobile_no = _(doc['mobile_no'])
            new_contact.phone = _(doc['phone'])
            new_contact.email_id = _(doc['email_id'])
            new_contact.save(ignore_permissions=True)
        else:
            return false
