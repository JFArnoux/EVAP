# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleInvoices(models.TransientModel):
    _name = "wizard.sale.invoices"
    _description = "Sale Invoices"

    date_start = fields.Datetime(string="Start Date")
    date_end = fields.Datetime(string="End Date")

    config_ids = fields.Many2many("pos.config", string="Shops")

    @api.multi
    def generate_report(self):
        domain = [
            ('order_id.date_order', '>=', self.date_start),
            ('order_id.date_order', '<', self.date_end),
        ]
        if self.config_ids:
            domain += [
                ('order_id.session_id.config_id', 'in', self.config_ids.ids)
            ]

        return {
            'name': _('Lignes tickets'),
            'view_type': 'form',
            'view_mode': 'tree,form,pivot',
            'res_model': 'pos.order.line',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': domain,
            'context': {
                'tree_view_ref': 'evap_pos.pos_order_line_tree_view_inherited'
            },
        }
