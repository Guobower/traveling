# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelWay(models.Model):
    """ contains list of travel way like bus , flyt ...etc."""

    _name = 'travel.travel.way'
    _quick_create = False

    name = fields.Char(u'طريقة السفر', required=True)