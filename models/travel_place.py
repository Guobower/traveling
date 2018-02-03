# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelPlace(models.Model):
    """ contains Travel place informations."""
    _name = 'travel.travel.place'
    _rec_name = 'place_name'
    _quick_create = False

    place_name = fields.Char(u'الوجهة', required=True)
    state_id = fields.Many2one('res.country.state', u'الولاية', required=True)
    country_id = fields.Many2one(related='state_id.country_id', readonly=True)