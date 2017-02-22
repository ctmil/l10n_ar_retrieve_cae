from openerp import models, fields, api, _
from openerp.exceptions import except_orm
from openerp.osv import osv
import urllib2, httplib, urlparse, gzip, requests, json
from StringIO import StringIO
import openerp.addons.decimal_precision as dp
from datetime import date
import logging
import ast
from openerp import exceptions
from openerp.exceptions import ValidationError

#Get the logger
_logger = logging.getLogger(__name__)

class invoice_query_cae(models.TransientModel):
        _name = 'invoice.query.cae'

	journal_id = fields.Many2one('account.journal',string='Diario')
	point_of_sale = fields.Integer('Punto de Venta',related='journal_id.point_of_sale')
	invoice_number = fields.Integer('Nro de Factura',required=True)

        @api.multi
        def execute(self):
		import pdb;pdb.set_trace()
