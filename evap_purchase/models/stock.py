# -*- coding: utf-8 -*-

from odoo import api, models


class Receipt(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):
        """
            When receipt is validated, update relevant products' sales price
            from `Prix de vente` tab in Purchase Order.
        """
        res = super(Receipt, self).button_validate()
        Order = self.env['purchase.order'].search([
            ('name', '=', self.origin)
        ])
        if Order:
            product_vals = {
                line.product_id.id: line.list_price
                for line in Order.order_line_ids
            }
            for line in self.move_ids_without_package:
                product = line.product_id
                product.write({
                    'list_price':
                        product.id in product_vals and
                        product_vals[product.id] or 0.0,
                    'available_in_pos': True
                })
        return res
