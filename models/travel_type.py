# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelType(models.Model):
    """ contains trip type information"""
    _name = 'travel.travel.type'
    _quick_create = False

    name = fields.Char(u'نوع الرحلة')
