# -*- coding: utf-8 -*-

from odoo import api, models


class Session(models.Model):
    _inherit = "pos.session"

    @api.multi
    def action_pos_session_closing_control(self):
        super(Session, self).action_pos_session_closing_control()
        return self.env.ref("evap_pos.action_report_pos_session").\
            report_action(self)

    @api.multi
    def get_discount_data(self):
        res = {}
        total_discount = 0.0

        orders = self.order_ids.filtered(
            lambda order: order.lines.filtered('discount')
        )

        for order in orders:
            customer = order.partner_id
            for line in order.lines:
                discount = (line.price_unit * line.qty) - line.price_subtotal
                if customer.id not in res:
                    res[customer.id] = \
                        [customer.name, discount, line.currency_id]
                else:
                    res[customer.id][1] += discount

                total_discount += discount

        return {
            'vals': list(res.values()),
            'total_discount': total_discount,
            'currency': self.env.user.company_id.currency_id
        }
