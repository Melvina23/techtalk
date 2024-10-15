from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime
import re

class Student(models.Model):
    _name = 'tech.student'
    _rec_name = 'name'
    _description = 'This model store student details'

    ref_no = fields.Char(string='Reference Number')
    name = fields.Char(string='Full Name', required=True)
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age' ,store=True)
    gender = fields.Selection([
        ('Male','Male'),
        ('Female','Female'),
        ('Others','Others')
    ], string='Gender')
    email = fields.Char(string='Email', required=True)
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
    course_id = fields.Many2one('tech.courses', string='Technology')
    inst_id = fields.Many2one('tech.instructor', string='Instructor Name', compute='_course_id', store=True)
    mark_ids = fields.One2many('tech.marks', 'stud_id', string='Marks')

    @api.model_create_multi
    def create(self, vals):
        try:
            a = str((self.env['tech.student'].search([])[-1].id) + 1)
        except IndexError:
            a = "1"
        for rec in vals:
            rec.update({
                'name': rec.get('name').title(),
                'ref_no': "STUD00" + a
            })
            return super(Student, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(Student, self).write(vals)

    @api.depends('dob')
    def _compute_age(self):
        for record in self:
            if record.dob:
                today = datetime.today().date()
                if record.dob > today:
                    raise ValidationError("The birthdate cannot be in the future.")
                record.age = int(today.year - record.dob.year - ((today.month, today.day) < (record.dob.month, record.dob.day)))
            else:
                record.age = 0

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

    @api.depends('course_id')
    def _course_id(self):
        if self.course_id:
            self.inst_id = self.course_id.instructor_id.id
        else:
            self.inst_id = False
