# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions


class Travel(models.Model):
    """ contains travel information."""
    _name = 'travel.travel'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Travel information'

    state = fields.Selection([('draft', u'مسودة'),
                              ('confirmed', u'رحلة مؤكدة'),
                              ('time_fixed', u'حدد موعد الرحلة'),
                              ('started', u'بدأت الرحلة'),
                              ('ended', u'إنتهت الرحلة'),
                              ('canceled', u'رحلة ملغات'),
                              ], default='draft',
                             track_visibility='onchange',
                             index=True, readonly=True)

    name = fields.Char(string=u'رقم العرض',
                       required=True,
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))

    company_id = fields.Many2one('res.company', u'الشركة')

    offer_id = fields.Many2one('travel.offer', u'عرض الرحلة',
                               readonly=True,
                               states={'draft': [('readonly', False)]})

    dep_travel_place_id = fields.Many2one('travel.travel.place', u'الإنطلاق',
                                          required=True,
                                          readonly=True,
                                          states={'draft': [('readonly', False)]}
                                          )

    des_travel_place_id = fields.Many2one('travel.travel.place', u'الوجهة',
                                          required=True,
                                          readonly=True,
                                          states={'draft': [('readonly', False)]}
                                          )
    price = fields.Float(u'مبلغ المسافر الواحد', required=True,readonly=True, states={'draft': [('readonly', False)]})

    total_amount = fields.Float(u'المجموع',
                                compute='get_total',
                                readonly=True,
                                store=True)

    paid_amount = fields.Float(string=u'المبلغ المدفوع',
                               compute='get_total_paid',
                               readonly=True,
                               store=True)

    customers_count = fields.Integer(string=u'عدد المسافرين',
                                     readonly=True,
                                     compute='count_customers',
                                     store=True)

    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id,
                                  readonly=True,
                                  states={'draft': [('readonly', False)]}
                                  )
    travel_type = fields.Many2one('travel.travel.type', u'نوع الرحلة', required=True,
                                  readonly=True,
                                  states={'draft': [('readonly', False)]}
                                  )
    travel_way = fields.Many2one('travel.travel.way', u'وسيلة السفر')

    travel_company_id = fields.Many2one(comodel_name='travel.travel.company',
                                        string=u'شركة الرحلة',
                                        required=True,
                                        )

    travel_go_date = fields.Date(u'ساعة الإنطلاق',readonly=True, states={'confirmed': [('readonly', False)]})

    travel_return_date = fields.Date(u'ساعة الرجوع', readonly=True, states={'confirmed': [('readonly', False)]})

    passenger_ids = fields.One2many(comodel_name='travel.passenger',
                                    inverse_name='travel_id',
                                    string='Passenger List',
                                    )

    @api.onchange('offer_id')
    def onchange_offer_id(self):
        """ set default value for fields that exist in offer"""
        if self.offer_id:
            if self.offer_id.state == 'canceled':
                self.offer_id = False
                return {'warning': {'title': _('خطأ'), 'message': _(u'لا يمكنك إختيار عرض ملغى')}}
            if self.offer_id.state == 'expired':
                self.offer_id = False
                return {'warning': {'title': _('خطأ'), 'message': _(u'لا يمكنك إختيار عرض منتهي')}}
            if self.offer_id.state not in 'confirmed':
                self.offer_id = False
                return {'warning': {'title': _('خطأ'), 'message': _(u'لا يمكنك إختيار عرض غير مؤكد')}}
            if self.offer_id and self.offer_id.end_date > fields.Date.context_today(self):
                self.offer_id = False
                return {'warning': {'title': _('خطأ'), 'message': _(u'تاريخ نهاية العرض  %s أقل من تاريخ اليوم لا يمكنك إختيار هذا العرض') % self.offer_id.end_date}}
            self.des_travel_place_id = self.offer_id.des_travel_place_id
            self.currency_id = self.offer_id.currency_id
            if self.offer_id.travel_company_id:
                self.travel_company_id = self.offer_id.travel_company_id
            if self.offer_id.travel_way:
                self.travel_way = self.offer_id.travel_way
            if self.offer_id.travel_type:
                self.travel_type = self.offer_id.travel_type
            if self.offer_id.price:
                self.price = self.offer_id.price

    @api.multi
    def confirm_travel(self):
        """ change state to confirmed"""
        self.ensure_one()
        if not self.name or self.name == _('New'):
            name = self.company_id and self.env['ir.sequence'].with_context(force_company=self.company_id.id).next_by_code(
                'travel.travel') \
                   or self.env['ir.sequence'].next_by_code('travel.travel') or _('New')
        self.write({
            'state': 'confirmed',
            'name': name,

        })

    @api.depends('passenger_ids', 'price')
    def count_customers(self):
        """ count number of costumers."""
        for rec in self:
            rec.update({
                'customers_count': rec.passenger_ids and len(rec.passenger_ids) or 0,
            })

    @api.depends('passenger_ids', 'passenger_ids.amount')
    def get_total(self):
        """ compute amount paid of total passengers."""
        for rec in self:
            if rec.passenger_ids:
                rec.total_amount = sum(passenger.amount for passenger in rec.passenger_ids )
            else:
                rec.total_amount = 0.0

    @api.depends('passenger_ids', 'passenger_ids.amount_paid')
    def get_total_paid(self):
        """ compute amount paid of total passengers."""
        for rec in self:
            if rec.passenger_ids:
                rec.paid_amount = sum(passenger.amount_paid for passenger in rec.passenger_ids )
            else:
                rec.paid_amount = 0.0

    @api.constrains('passenger_ids')
    def prevent_duplication(self):
        """ you cannot affect the some client two time"""
        for rec in self:
            if rec.passenger_ids and len(rec.passenger_ids) > len(rec.passenger_ids.mapped('passenger_id')):
                raise exceptions.ValidationError(u'!!لا يمكنك إعادة إدراج نفس الزبون مرتين')
