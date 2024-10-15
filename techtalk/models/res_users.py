from odoo import api,fields,models

class Users(models.Model):
    _inherit = "res.users"

    inst_id = fields.Many2one('tech.instructor', string='Instructor')
    stud_id = fields.Many2one('tech.student', string='Student')

