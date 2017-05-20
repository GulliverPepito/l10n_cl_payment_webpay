# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2017 Marlon Falcón Hernandez
#    (<http://www.falconsolutions.cl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Integración Webpay y Odoo MFH',
    'version': '10.0.0.1.0',
    'author': "Falcón Solutions, Marlon Falcón",
    'maintainer': 'Falcon Solutions',
    'website': 'http://www.falconsolutions.cl',
    'depends': ['website_sale'],
    'license': 'AGPL-3',
    'category': 'Settings',
    'summary': 'Integración Webpay y Odoo',
    'description': """
Integración Webpay y Odoo
=====================================================
* Integración con API de Webpay
        """,
    'data': [
        'views/res_company_view.xml',
        'views/payment_view.xml',
        'views/payment_webpay_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
    'external_dependencies': {
        'python': ['suds','wsse'],
     },
    'installable': True,
    'auto_install': False,
}

