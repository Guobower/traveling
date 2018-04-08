# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, exceptions
import re


class Travel(models.Model):
    """ contains travel information."""
    _name = 'travel.travel'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'Travel information'

    state = fields.Selection([('draft', u'مسودة'),
                              ('confirmed', u'رحلة مؤكدة'),
                              ('closed', u'رحلة مدفوعة'),
                              ('canceled', u'رحلة ملغات'),
                              ], default='draft',
                             track_visibility='onchange',
                             index=True, readonly=True)

    name = fields.Char(string=u'رقم الرحلة',
                       required=True,
                       copy=False,
                       readonly=True,
                       index=True,
                       default=lambda self: _('New'))
    bar_code = fields.Integer('رمز الرحلة', readonly=True)

    partner_id = fields.Many2one(comodel_name='res.partner',
                                 string=u'العميل',
                                 required=True)

    company_id = fields.Many2one(comodel_name='res.company',
                                 string=u'الشركة')

    airport_id = fields.Many2one(comodel_name='travel.airport',
                                 string=u'محطة الإنطلاق',
                                 required=True,
                                 readonly=True,
                                 states={'draft': [('readonly', False)]}
                                 )

    des_travel_place_id = fields.Many2one(comodel_name='travel.travel.place',
                                          string=u'الوجهة',
                                          required=True,
                                          readonly=True,
                                          states={'draft': [('readonly', False)]}
                                          )
    price = fields.Float(u'المبلغ المستحق', required=True)

    paid_amount = fields.Float(string=u'المبلغ المدفوع',
                               compute='_get_total_payment',
                               store=True)

    customers_count = fields.Integer(string=u'عدد المسافرين',
                                     readonly=True,
                                     compute='count_customers',
                                     store=True)

    currency_id = fields.Many2one('res.currency', string=u'عملة الشركة', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id,
                                  readonly=True)

    travel_type = fields.Many2one('travel.travel.type', u'نوع الرحلة', required=True)

    travel_way = fields.Many2one(comodel_name='travel.travel.way',
                                 string=u'وسيلة السفر',
                                 required=1,
                                 states={'draft': [('readonly', False)]})

    travel_company_id = fields.Many2one(comodel_name='travel.travel.company',
                                        string=u'شركة الرحلة',
                                        required=True,
                                        )

    travel_go_date = fields.Date(string=u'ساعة الإنطلاق')

    travel_return_date = fields.Date(string=u'ساعة الرجوع')

    accompanied_ids = fields.Many2many(comodel_name='res.partner',
                                     relation='travel_partners_rel',
                                     string=u'المسافرين المرافقين',
                                     )
    payment_ids = fields.One2many(comodel_name='travel.payment',
                                  inverse_name='travel_id',
                                  string='الدفعات',
                                  domain=[('active', '=', True)])


    @api.multi
    def confirm_travel(self):
        """ change state to confirmed"""
        self.ensure_one()
        if not self.name or self.name == _('New'):
            name = self.company_id and self.env['ir.sequence'].with_context(force_company=self.company_id.id).next_by_code(
                'travel.travel') \
                   or self.env['ir.sequence'].next_by_code('travel.travel') or _('New')
            bare_code = int(filter(str.isdigit, str(name)))
        self.write({
            'state': 'confirmed',
            'name': name,
            'bar_code': bare_code,
        })

    @api.depends('partner_id', 'accompanied_ids')
    def count_customers(self):
        """ count number of costumers."""
        for rec in self:
            rec.update({
                'customers_count': (rec.partner_id and 1 or 0) + (rec.accompanied_ids and len(rec.accompanied_ids) or 0),
            })

    @api.constrains('accompanied_ids')
    def prevent_duplication(self):
        """ you cannot affect the some client two time"""
        for rec in self:
            if rec.accompanied_ids and len(rec.accompanied_ids) > len(rec.accompanied_ids.mapped('id'))\
                    or rec.partner_id.id in rec.accompanied_ids.ids:
                raise exceptions.ValidationError(u'!!لا يمكنك إعادة إدراج نفس الزبون مرتين')


    @api.depends('payment_ids', 'payment_ids.company_currency_amount')
    def _get_total_payment(self):
        """ compute the amount paid by the client"""
        for rec in self:
            total_paid = 0.0
            for payment in rec.payment_ids:
                total_paid += payment.company_currency_amount
            rec.paid_amount = total_paid
