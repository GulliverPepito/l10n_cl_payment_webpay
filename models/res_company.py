# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime

class WebPayCompany(models.Model):
    _inherit = "res.company"
    
    commerce_code = fields.Char('Código del Comercio')
    online_mode = fields.Boolean('Online Mode', help='Si esta activo', default='True')

