from odoo.http import request, route, Controller
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class RegisterController(http.Controller):

    # Registration form
    @http.route('/register', type='http', auth='public', website=True, methods=['GET'])
    def register(self, **kwargs):
        course = request.env['tech.courses'].search([])
        district = request.env['tech.district'].search([])
        state = request.env['res.country.state'].search([])
        country = request.env['res.country'].search([])

        return request.render('techtalk.register_stud',{
            'course': course,
            'district': district,
            'state': state,
            'country': country,
            'assets': 'web.assets_frontend',
        })

    @http.route('/register/stud', auth='public', methods=['POST'], type='http', csrf=False)
    def create_register(self, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        dob = kwargs.get('dob')
        gender = kwargs.get('gender')
        aadhar = kwargs.get('aadhar')
        qualifi = kwargs.get('qualifi')
        phone = kwargs.get('phone')
        father = kwargs.get('father')
        mother = kwargs.get('mother')
        mobile = kwargs.get('mobile')
        street = kwargs.get('street')
        city = kwargs.get('city')
        district_id = kwargs.get('district')
        state_id = kwargs.get('state')
        country_id = kwargs.get('country')
        zipcode = kwargs.get('zipcode')
        course_id = kwargs.get('course_id')

        if not name or not email:
            return request.redirect('/error_page')

        existing_records = request.env['tech.register'].search([('email', '=', email)])
        if existing_records:
            error_message = 'This email is already registered. Please use a different email.'
            return request.render('techtalk.response_template', {'error': error_message}) if request.env['ir.ui.view'].search_count([('key', '=', 'techtalk.response_template')]) else request.redirect('/error_page')

        records = request.env['tech.register'].sudo().create({
                'name': name,
                'email': email,
                'aadhar': aadhar,
                'qualifi': qualifi,
                'dob': dob,
                'gender': gender,
                'phone': phone,
                'father': father,
                'mother': mother,
                'mobile': mobile,
                'street': street,
                'city': city,
                'district_id': district_id,
                'state_id': state_id,
                'country_id': country_id,
                'zipcode': zipcode,
                'course_id': course_id,
            })
        district = request.env['tech.district'].search([('id', '=', district_id)])
        z1=(district.name)
        state = request.env['res.country.state'].search([('id', '=', state_id)])
        z2=(state.name)
        country = request.env['res.country'].search([('id', '=', country_id)])
        z3=(country.name)

        return request.render('techtalk.add_success',{'records':records,'z1':z1,'z2':z2,'z3':z3})

    @http.route('/register/print', auth='public', methods=['POST'], type='http', csrf=False)
    def create_print(self,**kwargs):
        email = kwargs.get('abc')
        abc = request.env['tech.register'].search([('email', '=', email)])
        records = {}
        records['records'] = abc

    # @http.route('/register/print', auth='public', methods=['POST'], type='http', csrf=False)
    # def create_print(self, **kwargs):
    #     email = kwargs.get('abc')
    #
    #     # Try to find the record
    #     record = request.env['tech.register'].search([('email', '=', email)], limit=1)
    #     print(record)
    #     if record:
    #         print("*************")
    #         return request.env.ref('techtalk.ctrl_stud_report_action').report_action(record)
    #
    #     print("*************")
    #     return request.redirect('/')

