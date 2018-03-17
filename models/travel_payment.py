# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Payment(models.Model):
    """ payment of travel"""
    _name = 'travel.payment'
    _order = 'payment_date desc'

    travel_id = fields.Many2one(comodel_name='travel.travel',
                                string=u'الرحلة')

    amount = fields.Float(string=u'الدفعة',
                          required=True)

    currency_id = fields.Many2one(comodel_name='res.currency',
                                  string=u'عملة الدفعة',
                                  required=True,
                                  default=lambda self: self.env.user.company_id.currency_id.id)

    company_currency_amount = fields.Float(string=u'المبلغ بعملة الشركة',
                                           required=True)

    company_currency_id = fields.Many2one(comodel_name='res.currency',
                                          string=u'عملة الشركة',
                                          readonly=True,
                                          required=True,
                                          default=lambda self: self.env.user.company_id.currency_id.id)

    payment_date = fields.Datetime(string=u'ساعة الدفع',
                                   required=True,
                                   default=fields.Datetime.now())

    active = fields.Boolean('Active', default=True)

    @api.onchange('amount', 'currency_id')
    def onchange_payment(self):
        """  """
        if self.amount:
            self.company_currency_amount = self.amount * self.currency_id.rate / self.company_currency_id.rate

    @api.multi
    def unlink(self):
        """ make record invisible."""
        self.write({'active': False})
