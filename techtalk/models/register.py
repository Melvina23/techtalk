from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re

class Register(models.Model):
    _name = 'tech.register'
    _rec_name = 'name'
    _description = 'This model stores register details'
    _inherit = ['mail.thread']

    ref_no = fields.Char(string='Reference Number')
    date = fields.Date(string='Date', default=fields.Date.today(), readonly=True)
    name = fields.Char(string='Full Name', required=True, tracking=True)
    email = fields.Char(string='Email', tracking=True)
    aadhar = fields.Char(string='Aadhar Nubmer', size=12, tracking=True)
    dob = fields.Date(string='Date of Birth')
    qualifi = fields.Selection([
        ('UG','UG'),
        ('PG','PG'),
    ], string='Qualification')
    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ], string='Gender')
    phone = fields.Char(string='Phone', size=10, tracking=True)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    zipcode = fields.Char(string='PinCode', size=6)
    image = fields.Binary(string='Image')

    # family details
    father = fields.Char(string='Father Name')
    mother = fields.Char(string='Mother Name')
    mobile = fields.Char(string='Parents Number', size=10)

    # mail
    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ], default='Draft', string="Status")

    check = fields.Selection([
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled')
    ], default='Pending', string="Status")

    # configure
    district_id = fields.Many2one('tech.district', string='District')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')

    # relation
    course_id = fields.Many2one('tech.courses', string='Technology')

    @api.model_create_multi
    def create(self, vals):
        try:
            a = str((self.env['tech.register'].search([])[-1].id) + 1)
        except IndexError:
            a = "1"
        for rec in vals:
            rec.update({
                'name': rec.get('name').title(),
                'ref_no': "AP000" + a
            })
            return super(Register, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(Register, self).write(vals)

    @api.constrains('aadhar')
    def _check_aadhar(self):
        for record in self:
            if record.aadhar:
                if len(record.aadhar) != 12 or not re.match(r'^\d{12}$', record.aadhar):
                    raise ValidationError("Aadhar number must be exactly 12 digits long and contain only numbers.")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', record.email)
                if match is None:
                    raise ValidationError('Invalid Email Address')

    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = r"(^[6-9]\d{9})"
        for record in self:
            if record.phone and not re.match(phone_pattern, record.phone):
                raise ValidationError("The phone number'%s' is not valid." % record.phone)

    @api.constrains('mobile')
    def _check_mobile(self):
        mobile_pattern = r"(^[6-9]\d{9})"
        for record in self:
            if record.mobile and not re.match(mobile_pattern, record.mobile):
                raise ValidationError("The phone number'%s' is not valid." % record.mobile)

    # mail
    def set_approved(self):
        for record in self:
            record.state = 'Approved'
            if record.email:
                temp_id = self.env.ref('techtalk.send_client_approved')
                temp_id.send_mail(record.id, force_send=True)
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': "Approve mail sent successfully!!!",
                        'type': 'rainbow_man'
                    }
                }

    def set_rejected(self):
        for record in self:
            record.state = 'Rejected'
            if record.email:
                temp_id = self.env.ref('techtalk.send_client_rejected')
                temp_id.send_mail(record.id, force_send=True)
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': "Reject mail sent successfully!!!",
                        'type': 'rainbow_man',
                    }
                }

    def confirm(self):
        for record in self:
            existing_student = self.env['tech.student'].search([('email', '=', record.email)], limit=1)
            if existing_student:
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': "Student already confirmed!!!",
                        'type': 'rainbow_man',
                    }
                }
            else:
                confirm_det = self.env['tech.student'].create({
                    'name': record.name,
                    'dob': record.dob,
                    'gender': record.gender,
                    'email': record.email,
                    'phone': record.phone,
                    'course_id': record.course_id.id,
                    'street': record.street,
                    'city': record.city,
                    'district_id': record.district_id.id,
                    'state_id': record.state_id.id,
                    'country_id': record.country_id.id,
                    'zipcode': record.zipcode,
                })
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': "Student confirmed successfully!",
                        'type': 'rainbow_man',
                    }
                }
