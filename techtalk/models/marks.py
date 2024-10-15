from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Marks(models.Model):
    _name = 'tech.marks'
    _rec_name = 'stud_id'

    stud_id = fields.Many2one('tech.student', string="Student Name", required=True)
    pro_first  = fields.Float(string="Project 1")
    pro_sec  = fields.Float(string="Project 2")
    pro_third  = fields.Float(string="Project 3")
