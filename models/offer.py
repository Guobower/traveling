# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Offer(models.Model):
    """ contains Travel Offer information."""
    _name = "travel.offer"
    _quick_create = False

    name = fields.Char(string=u'رقم العرض', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))

    company_id = fields.Many2one('res.company', u'الشركة')
    state = fields.Selection([('draft', u'مسودة'),
                              ('confirmed', u'عرض مؤكد'),
                              ('expired', u'إنتهى'),
                              ('canceled', u'ألغى'),
                              ], default='draft')

    des_travel_place_id = fields.Many2one('travel.travel.place', u'الوجهة',
                                          required=True,
                                          )

    price = fields.Float(u'مبلغ المسافر الواحد', required=True,)

    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id,

                                  )

    travel_type = fields.Many2one('travel.travel.type', u'نوع الرحلة', required=True,

                                  )
    travel_way = fields.Many2one('travel.travel.way', u'وسيلة السفر')

    travel_company_id = fields.Many2one(comodel_name='travel.travel.company',
                                        string=u'شركة الرحلة',
                                        required=True)

    begin_date = fields.Date(u'تاريخ بداية العرض', required=True,

                             )
    end_date = fields.Date(u'تاريخ نهاية العرض',)

    max_customers = fields.Integer(u'عدد العملاء الأقصى', required=True, default=2)
    min_customers = fields.Integer(u'عدد العملاء الأدنى', required=True, default=2)

    travel_ids = fields.One2many(comodel_name='travel.travel',
                                 inverse_name='offer_id',
                                 string=u'الرحلات')
    total_amount = fields.Float(u'المداخيل')


    @api.multi
    def confirm_offer(self):
        """ change state to confirmed"""
        self.ensure_one()
        if not self.name or self.name == _('New'):
            name = self.company_id and self.env['ir.sequence'].with_context(force_company=self.company_id.id).next_by_code('travel.offer') \
                   or self.env['ir.sequence'].next_by_code('travel.offer') or _('New')
        self.write({
            'state': 'confirmed',
            'name': name,

        })

    @api.multi
    def cancel_offer(self):
        """ change state to confirmed"""
        self.write({'state': 'canceled'})

    @api.multi
    def offer_expired(self):
        """ offer is expired"""
        val = {'state': 'expired',}
        if not self.end_date:
            val['end_date'] = fields.Date.context_today(self)
        self.write(val)

    @api.multi
    def name_get(self):
        """ change representation."""
        result = []
        for rec in self:
            result.append((rec.id, '%s %s' % (rec.name, rec.des_travel_place_id.place_name)))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if ' ' in name:
            names = name.split(' ')
            recs = self.search([('name', 'ilike', names[0])] + args, limit=limit)
        else:
            recs = self.search(['|', ('name', 'ilike', name), ('des_travel_place_id.place_name', 'ilike', name)] + args, limit=limit)
        return recs.name_get()

