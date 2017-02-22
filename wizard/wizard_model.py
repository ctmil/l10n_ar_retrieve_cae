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
		fecha_vto = None
		for key in r.keys():
			if type(r[key]) == dict:
				cod_autorizacion = r[key].get('CodAutorizacion',None)
			fec_vto = r[key].get('FchVto',None)
			if fec_vto:
				fecha_vto = fec_vto[:4] + '-' + fec_vto[4:6] + '-' + fec_vto[6:9]
		import pdb;pdb.set_trace()
		if cod_autorizacion and fecha_vto:
			vals = {
				'afip_cae': str(cod_autorizacion),
				'afip_cae_due': fecha_vto		
				}
			return_id = invoice_id.write(vals)
			return None
			
