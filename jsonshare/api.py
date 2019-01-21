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


def guardar_dato_recibido(item_fields):
    frappe.msgprint(_(item_fields))
    # for item in item_fields:
    #         if not frappe.db.exists('Item', _(item.get('item_code'))):
    #             frappe.doc({
    #                 'doctype': 'Item',
    #                 'item_name': _(item.get('item_name'))
    #             }).insert(ignore_permissions=True)

    return 200


@frappe.whitelist(allow_guest=True)
def receivejson(data_in):
    '''NO CAMBIAR'''
    # kwargs=frappe._dict(kwargs)
    # return kwargs
    # Se pueden agregar verificaciones del json recibido
    item_data = json.loads(data_in)
    guardar_dato_recibido(item_data)



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
        # frappe.msgprint(_(r.status_code))
        pass


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
                                                    'is_stock_item', 'opening_stock'], as_dict=1)

        compartir_data(item_data)
    except:
        frappe.msgprint(_('FAIL'))

    # # UPDATE DATA
    # update_item=frappe.get_doc("Item", item_code)
    # update_item.crop_cycle=""
    # update_item.save()

    # # DELETE DATA
    # delete_item=frappe.get_doc("Item", item_code)
    # delete_item.delete()
