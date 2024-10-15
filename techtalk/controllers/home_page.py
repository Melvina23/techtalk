from odoo.http import request, route, Controller
from odoo import http
from odoo.http import request

class Homepage(http.Controller):

    # home page
    @http.route('/', auth='public', website=True)
    def homepage(self, **kwargs):
        search_id = request.env['tech.courses'].search([])
        if search_id:
            course = []
            for i in search_id:
                course.append({
                    'id': i.id,
                    'name' : i.name,
                    'start_date' : i.start_date,
                    'end_date' : i.end_date,
                    'image' : i.image,
                })
            return request.render('techtalk.homepage_template', {'course': course})
        return request.render('techtalk.homepage_template')

    # readmore page
    @route('/readmore-page/<int:course_id>', auth='public', type='http', website=True)
    def create_readmore(self,course_id):
        search_id = request.env['tech.courses'].search([('id','=',course_id)])
        if search_id:
            course = []
            for i in search_id:
                course.append({
                    'id': i.id,
                    'name': i.name,
                    'start_date': i.start_date,
                    'end_date': i.end_date,
                    'amount': int(i.amount),
                    'image': i.image,
                })
            return request.render('techtalk.course_readmore',{'course': course})
        return request.render('techtalk.course_readmore')

    # about page
    @http.route('/about', type='http', auth='public', website=True)
    def about(self):
        return request.render('techtalk.about_template')

    # Trail
    @http.route('/check', type='http', auth='public', website=True)
    def check(self):
        return request.render('techtalk.checkup')
