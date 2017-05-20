# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare
_logger = logging.getLogger(__name__)
import wsse
import suds

class AcquirerWebpay(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('webpay', 'Webpay')])
    webpay_private_key = fields.Char('Clave Privada', required_if_provider='webpay')
    webpay_public_cert = fields.Char('Certificado Público', required_if_provider='webpay')
    webpay_cert = fields.Char('Certificado del servidor', required_if_provider='webpay')
    webpay_environment = fields.Selection(
            [('1','INTEGRACION'),
            ('2','CERTIFICACION'),
            ('3 ','PRODUCCION')],
            'Ambiente Webpay', default='2', required_if_provider='webpay')

    def _get_feature_support(self):
        """Get advanced feature support by provider.

        Each provider should add its technical in the corresponding
        key for the following features:
            * fees: support payment fees computations
            * authorize: support authorizing payment (separates
                         authorization and capture)
            * tokenize: support saving payment data in a payment.tokenize
                        object
        """
        res = super(AcquirerWebpay, self)._get_feature_support()
        res['fees'].append('webpay')
        return res

    @api.model
    def _get_webpay_urls(self, environment):
        """ Paypal URLS """
        if environment == 'prod':
            return {
                'webpay_form_url': 'https://www.paypal.com/cgi-bin/webscr',
                'webpay_rest_url': 'https://api.paypal.com/v1/oauth2/token',
            }
        else:
            return {
                'webpay_form_url': 'https://www.sandbox.paypal.com/cgi-bin/webscr',
                'webpay_rest_url': 'https://api.sandbox.paypal.com/v1/oauth2/token',
            }

    @api.multi
    def webpay_form_generate_values(self, values):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        webpay_tx_values = dict(values)
        webpay_tx_values.update({
            'cmd': '_xclick',
            'business': self.company_id.name,
            'item_name': '%s: %s' % (self.company_id.name, values['reference']),
            'item_number': values['reference'],
            'amount': values['amount'],
            'currency_code': values['currency'] and values['currency'].name or '',
            'address1': values.get('partner_address'),
            'city': values.get('partner_city'),
            'country': values.get('partner_country') and values.get('partner_country').code or '',
            'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
            'email': values.get('partner_email'),
            'zip_code': values.get('partner_zip'),
            'first_name': values.get('partner_first_name'),
            'last_name': values.get('partner_last_name'),
            #~ 'paypal_return': '%s' % urlparse.urljoin(base_url, PaypalController._return_url),
            #~ 'notify_url': '%s' % urlparse.urljoin(base_url, PaypalController._notify_url),
            #~ 'cancel_return': '%s' % urlparse.urljoin(base_url, PaypalController._cancel_url),
            #~ 'handling': '%.2f' % paypal_tx_values.pop('fees', 0.0) if self.fees_active else False,
            #~ 'custom': json.dumps({'return_url': '%s' % paypal_tx_values.pop('return_url')}) if paypal_tx_values.get('return_url') else False,
        })
        return webpay_tx_values

    @api.multi
    def webpay_get_form_action_url(self):
        return self._get_webpay_urls(self.environment)['webpay_form_url']

class TxWebpay(models.Model):
    _inherit = 'payment.transaction'

    webpay_txn_type = fields.Char('Tipo Transacción')
