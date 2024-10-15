from odoo.http import request, route, Controller
from odoo import http
from odoo.http import request


class LoginController(http.Controller):

    # login page
    @http.route('/login', type='http', auth='public', website=True)
    def login_page(self, **kwargs):
        return request.render('techtalk.login_page', {
            'success': kwargs.get('Login Success'),
        })

    # login submission
    @http.route('/login/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def login_submit(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        # user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
        # if user and user.check_password(password):
        #
        #     request.session.authenticate(request.session.db, email, password)
        #     return request.redirect('/home')

        return request.render('techtalk.login_page', {
            'error': 'Invalid email or password. Please try again.'
        })
