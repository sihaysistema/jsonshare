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

def compartir_data(data):
    url = 'http://192.168.0.46/api/method/jsonshare.api.receivejson'

    try:
        r = requests.post(url, data=json.dumps(data))
        # frappe.msgprint(_(json.dumps(data)))
    except:
        # Codigo Status
        # print('Status : ' + str(r.status_code) + '\n')
        frappe.msgprint(_('Error'))
        # frappe.msgprint(_(json.dumps(data)))
    else:
        frappe.msgprint(_(r.status_code))
        frappe.msgprint(_(r.content))

@frappe.whitelist()
def crud(item):
    '''Funcion encarga de obtener datos y mandarlos por HTTP
        funcionalidades extras'''
    # GET DATA
    # if frappe.db.exists('Items, {'numero_dte': serie_original_factura}):
    try:
        item_data = frappe.db.get_values('Item',
                                         filters={'item_code': item},
                                         fieldname=['item_code', 'item_name',
                                                    'item_group', 'stock_uom',
                                                    'standard_rate', 'description',
                                                    'is_stock_item'], as_dict=1)
        compartir_data(item_data)
    except:
        frappe.msgprint(_('FAIL'))

def mensaje():
    frappe.publish_realtime(event='msgprint',message='Alguien llamo este metodo de receive json')

def guardar_dato_recibido(item_fields):
    # frappe.msgprint(_(item_fields))
    for item in item_fields:
        new_item = frappe.new_doc("Item")
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
        else:
            new_item.stock_uom = _(item.get('stock_uom'))
        new_item.save(ignore_permissions=True)
    hello = 'Se ha creado un nuevo Item'
    return hello
    #return 200

@frappe.whitelist(allow_guest=True)
def receivejson(data):
    item_data = json.loads(data)
    guardar_dato_recibido(item_data)
    #frappe.publish_realtime(event='global',message='Alguien llamo este metodo de receive json',room=None)
    hello = 'Se ha creado un nuevo Item'
    return hello