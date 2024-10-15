from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re

class Courses(models.Model):
    _name = 'tech.courses'
    _rec_name = 'name'
    _description = 'This model store courses details'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, tracking=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    amount = fields.Float(string='Amount', required=True, tracking=True)
    desc = fields.Text(string='Description')
    image = fields.Image(string='Image')

    state = fields.Selection([
        ('Planned','Planned'),
        ('Ongoing','Ongoing'),
        ('Completed','Completed')
    ], string='Status')

    # relation
    instructor_id = fields.Many2one('tech.instructor', string='Instructor Name')

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec.update({'name': rec.get('name').title()})
        return super(Courses, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(Courses, self).write(vals)