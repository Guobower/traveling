# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TravelPassenger(models.Model):
    """ contains detail about passenger and his payments."""
    _name = 'travel.passenger'

    passenger_id = fields.Many2one(comodel_name='res.partner',
                                   string='Passenger',
                                   required=True,
                                   domain=[('customer', '=', True)])
    travel_id = fields.Many2one(comodel_name='travel.travel',
                                string='Travel',
                                requied=True,)

    amount = fields.Float('ثمن الرحلة')
    amount_paid = fields.Float('المبلغ المدفوع', )


