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
	invoice_number = fields.Integer('Nro de Factura')

        @api.multi
        def execute(self):
		invoice_id = self.env['account.invoice'].browse(self.env.context['active_id'])
		conn = self.journal_id.afip_connection_id
		serv = self.journal_id.afip_connection_id.server_id
		r = serv.wsfe_query_invoice(conn.id,self.journal_id.journal_class_id.afip_code,self.invoice_number,self.point_of_sale)
		#print r
		#import pdb;pdb.set_trace()
		for key in r.keys():
			cod_autorizacion = key.get('CodAutorizacion',None)
			if key == 'FchVto':
				fecha_vto = r['FchVto'][:4] + '-' + r['FchVto'][4:6] + '-' + r['FchVto'][6:9]
		if cod_autorizacion and fecha_vto:
			vals = {
				'afip_cae': cod_autorizacion,
				'afip_cae_due': fecha_vto		
				}
			invoice_id.write(vals)
			return None
			
