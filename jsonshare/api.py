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


def validar_peticion():
    pass


@frappe.whitelist(allow_guest=True)
def receivejson(data):
    '''Verifica que el origen sea confiable y procede al manejo de la
    peticion'''
    item_data = json.loads(data)

    if item_data['key'] == 'hash':
        # mensaje = guardar_dato_recibido(item_data)
        return 200