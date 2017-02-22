# -*- coding: utf-8 -*-

from openerp import models, api, fields
from openerp.osv import osv
from openerp.tools.translate import _
import re
import sys
import logging

_logger = logging.getLogger(__name__)


class account_invoice(models.Model):
	_inherit = 'account.invoice'

	@api.multi
	def invoice_retrieve_cae(self):
		self.ensure_one()
		if self.journal_id:
			vals = {
				'journal_id': self.journal_id.id
				}
			wizard_id = self.env['invoice.query.cae'].create(vals)
	                return {
				'type': 'ir.actions.act_window',
        	                'name': 'Consultar CAE',
                	        'res_model': 'invoice.query.cae',
                        	'res_id': wizard_id.id,
	                        'view_type': 'form',
        	                'view_mode': 'form',
                	        'target': 'new',
                        	'nodestroy': True,
	                        }

