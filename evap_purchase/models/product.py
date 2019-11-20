# -*- coding: utf-8 -*-

from odoo import fields, models


class Product(models.Model):
    _inherit = "product.template"

    customs_duty = fields.Float(string="Droit de douane", help="Customs Cost")
