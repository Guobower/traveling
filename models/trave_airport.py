# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Airport(models.Model):
    """ contains list aiport names."""
    _name = 'travel.airport'

    name = fields.Char(u'إسم المطار')