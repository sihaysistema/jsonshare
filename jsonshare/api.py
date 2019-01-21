# -*- coding: utf-8 -*-
# Copyright (c) 2019, SHS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json

@frappe.whitelist(allow_guest=True)
def sumtwo(num1, num2):
    sumoftwo = int(num1) + int(num2)
    return sumoftwo

@frappe.whitelist(allow_guest=True)
def receivejson(**kwargs):
    '''NO CAMBIAR'''
    kwargs=frappe._dict(kwargs)
    return kwargs

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
