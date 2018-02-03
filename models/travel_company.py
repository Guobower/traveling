# -*- coding: utf-8 -*-


from odoo import models, fields, api


class TravelCompany(models.Model):
    """ contains Travel company information"""

    _name = 'travel.travel.company'
    _quick_create = False

    name = fields.Char(u'إسم الشركة', required=True)