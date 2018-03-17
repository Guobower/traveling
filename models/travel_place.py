# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelPlace(models.Model):
    """ contains Travel place informations."""
    _name = 'travel.travel.place'
    _rec_name = 'place_name'
    _quick_create = False
    place_name = fields.Char(u'الوجهة', required=True)
    country_id = fields.Many2one('res.country', u'البلد', required=True)