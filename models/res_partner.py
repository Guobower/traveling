# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    """ add passport number to client info."""
    _inherit = 'res.partner'

    passport_number = fields.Char(u'رقم جواز السفر', required=True)
    user_id = fields.Many2one(string=u'المؤظف المسؤول')
    # in agency we don't have shipping address
    type = fields.Selection(
        [('contact', 'Contact'),
         ('other', 'Other address')])