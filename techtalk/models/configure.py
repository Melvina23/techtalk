from odoo import api, fields, models

class Country(models.Model):
    _name = 'tech.country'
    _rec_name = 'name'
    _description = 'This model store country details'


    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec.update({'name': rec.get('name').title()})
        return super(Country, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(Country, self).write(vals)
   

class State(models.Model):
    _name = 'tech.state'
    _rec_name = 'name'
    _description = 'This model store state details'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec.update({'name': rec.get('name').title()})
        return super(State, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(State, self).write(vals)


class District(models.Model):
    _name = 'tech.district'
    _rec_name = 'name'
    _description = 'This model store district details'

    name = fields.Char(string="Name")
    code = fields.Char(string="Code") 

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            rec.update({'name': rec.get('name').title()})
        return super(District, self).create(vals)

    def write(self, vals):
        if vals.get('name'):
            vals.update({'name': vals.get('name').title()})
        return super(District, self).write(vals)
             