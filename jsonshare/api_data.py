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
            frappe.msgprint(_('FAIL Customer'))


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
    # try:
    #     # Manda data como json string
    #     r = requests.post(url, data=json_data)
    # except:
    #     frappe.msgprint(_('Error En la comunicacion'))
    # else:
    #     # Codigo de estado
    #     frappe.msgprint(_(r.status_code))
    #     # Contenido de la respuesta
    #     frappe.msgprint(_(r.content))
