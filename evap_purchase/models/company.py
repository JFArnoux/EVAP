# -*- coding: utf-8 -*-

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    ice = fields.Char(string="I.C.E.", help="I.C.E.")
    register = fields.Char(string="Registre du commerce", help="Register")
    tax_identification = fields.Char(
        string="Identifiant fiscal",
        help="Tax Identification"
    )
    patent = fields.Char(string="Patente", help="Patent")
