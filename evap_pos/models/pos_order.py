# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _process_order(self, pos_order):
        order = super(PosOrder, self)._process_order(pos_order)
        """
            This email is for those contacts who have `Pas depoint de fidélité`
            field defined as True.
        """
        if order and order.partner_id.has_no_loyalty_points:
            template = self.env.ref('evap_pos.email_template_loyalty_points')
            template.send_mail(order.id)
        return order


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    currency_id = fields.Many2one(
        related="order_id.session_id.config_id.currency_id",
        string="Devise",
    )
