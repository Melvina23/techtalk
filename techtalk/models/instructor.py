from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re

class Instructor(models.Model):
    _name = 'tech.instructor'
    _rec_name = 'name'
    _description = 'This model store instructor details'
    _inherit = ['mail.thread']

    ref_no = fields.Char(string='Reference Number')
    name = fields.Char(string='Full Name', required=True, tracking=True)
    dob = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    ], string='Gender', tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    phone = fields.Char(string='Phone', size=10)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    zipcode = fields.Char(string='Zip Code', size=6)
    image = fields.Binary(string='Image')

    # configure
    district_id = fields.Many2one('tech.district', string='District')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')

    # relation
    course_id = fields.Many2one('tech.courses', string='Course Name')
    stud_ids = fields.One2many('tech.student','inst_id', string='Student Details')

    @api.model_create_multi
    def create(self, vals):
        try:
            a = str((self.env['tech.instructor'].search([])[-1].id) + 1)
        except IndexError:
            a = "1"
        for rec in vals:
            rec.update({
                'name': rec.get('name').title(),
                'ref_no': "INS00" + a
            })
            return super(Instructor, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(Instructor, self).write(vals)

    @api.constrains('dob')
    def _check_dob(self):
        for record in self:
            if record.dob and record.dob > fields.Date.today():
                raise ValidationError("The birthdate cannot be in the future.")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                # Validate email format
                match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', record.email)
                if match is None:
                    raise ValidationError('Invalid Email Address')

    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = r"(^[6-9]\d{9})"
        for record in self:
            if record.phone and not re.match(phone_pattern, record.phone):
                raise ValidationError("The phone number'%s' is not valid." % record.phone)
