from odoo import api, models, fields
from odoo.exceptions import ValidationError
from datetime import datetime


class Payment(models.Model):
    _name = 'tech.payment'
    _rec_name = 'name'
    _description = 'This model store student fees details'
    _inherit = ['mail.thread']

    name = fields.Char(string='Student Name', required=True, tracking=True)
    number = fields.Char(string='Reference Number', readonly=True, tracking=True)
    pay_date = fields.Date(string='Date', default=fields.Date.today(), readonly=True)
    amount = fields.Integer(string='Amount', readonly=True, tracking=True, compute='_course_id', store=True)
    status = fields.Selection([
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    ], string='Payment Method')

    # student
    course_id = fields.Many2one('tech.courses',string='Course Name')

    # button
    button = fields.Selection([
        ('Show', 'Show'),
        ('Notshow', 'Notshow'),
    ], string='button', default='Show')

    @api.model_create_multi
    def create(self, vals):
        try:
            a = str((self.env['tech.payment'].search([])[-1].id) + 1)
        except IndexError:
            a = "1"
        for rec in vals:
            rec.update({
                'name': rec.get('name').title(),
                'number': "PAY00" + a
            })
            return super(Payment, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(Payment, self).write(vals)

    @api.depends('course_id')
    def _course_id(self):
        if self.course_id:
            self.amount = self.course_id.amount

    def pay_fee(self):
        pass
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Student confirmation successfully!!!",
                'type': 'rainbow_man',
            }
        }