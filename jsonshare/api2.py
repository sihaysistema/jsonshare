# -*- coding: utf-8 -*-
# Copyright (c) 2019, SHS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from api_data import *
import json
import requests
import os

# Permite trabajar con acentos, ñ, simbolos, etc
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@frappe.whitelist(allow_guest=True)
def sumtwo(num1, num2):
    sumoftwo = int(num1) + int(num2)
    return sumoftwo


@frappe.whitelist(allow_guest=True)
def receivejson1(**kwargs):
    '''NO CAMBIAR'''
    kwargs=kwargs
    return kwargs


@frappe.whitelist(allow_guest=True)
def hello_world(**kwargs):
    '''NO CAMBIAR'''
    hello = 'Hello World'
    return hello

def guardar_dato_recibido(item_fields):
    # Guarda el numero de items recibidos a crear
    n_item = 0
    n_uom = 0
    mensaje = ''

    for item in item_fields:
        if not frappe.db.exists('Item', _(item.get('item_code'))):
            n_item = len(item_fields)
            new_item = frappe.new_doc('Item')
            new_item.item_code = _(item.get('item_code'))
            new_item.item_name = _(item.get('item_name'))
            new_item.description = _(item.get('description'))
            new_item.is_stock_item = _(item.get('is_stock_item'))

            if item.get('item_group') != 'All Item Groups':
                new_item.item_group = 'All Item Groups'
            else:
                new_item.item_group = _(item.get('item_group'))

            if not frappe.db.exists('UOM', _(item.get('stock_uom'))):
                new_stock_uom = frappe.new_doc("UOM")
                new_stock_uom.uom_name = _(item.get('stock_uom'))
                new_stock_uom.save(ignore_permissions=True)
                n_uom += 1
            else:
                new_item.stock_uom = _(item.get('stock_uom'))
            
            new_item.save(ignore_permissions=True)
            mensaje = '{0} Items creados, {1} UOM creados'.format(n_item, n_uom)
        else:
            mensaje = 'Item compartido ya existe'

    return mensaje


@frappe.whitelist(allow_guest=True)
def receivejson(data):
    item_data = json.loads(data)
    mensaje = guardar_dato_recibido(item_data)
    return mensaje


@frappe.whitelist(allow_guest=True)
def receivejson_customer(data):
    customer_data = json.loads(data)
    #frappe.publish_realtime(event='global',message='Alguien llamo este metodo de receive json',room=None)
    mensaje = create_customer(customer_data)
    frappe.publish_realtime(event='eval_js', message='alert("{0}")'.format('funcionando'), user=frappe.session.user)
    return mensaje

def mensaje():
    frappe.publish_realtime(event='msgprint',message='Alguien llamo este metodo de receive json')

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

# def create_address(customer_addresses):
#     if not frappe.db.exists('Address', _(address_title)):
#         new_address = frappe.new_doc("Address")
#         new_address.title = _(territory_name)
#         new_address.type =
#         new_address.address_line1 =
#         new_address.city =
#         new_territory.save(ignore_permissions=True)
#     else:
#         return false
    # # find if customer group exists as sent
    # # if it exists, do not create it
    # # if it doesn't, we refer to root, so we create it under root
    # # we will separate the node groups created by a parent folder with the server address of the sender.    
    # # if parent_customer_group is None or parent == 'All Customer Groups'
    # # create the customer group
    # # else:
    # # find the customer group root