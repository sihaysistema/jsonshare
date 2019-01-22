# -*- coding: utf-8 -*-
# Copyright (c) 2019, SHS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
import requests


@frappe.whitelist()
def obtener_usuarios():
    if frappe.db.exists('Usuarios Compartidos', {'parent': 'Configuracion JsonShare'}):
        usuarios_data = frappe.db.get_values('Usuarios Compartidos',
                                             filters={'parent': 'Configuracion JsonShare'},
                                             fieldname=['host_name'])

    # Retorna los datos como lista
    return usuarios_data
