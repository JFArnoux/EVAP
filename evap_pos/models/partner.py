# -*- coding: utf-8 -*-

from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    has_no_loyalty_points = fields.Boolean(
        string="Pas de point de fidélité",
        help="""
            For the contacts who have the field `Pas de point de fidélité`
            defined, they won’t benefit from the loyalty program.
            Their loyalty points will be always 0.
        """
    )
