# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Techtalk',
    'version': '1.0',
    'category': 'techtalk',
    'sequence': 225,
    'summary': 'techtalk application',
    'depends': ['mail','website','website_profile'],
    'license':[],
    'data': [
        'security/techtalk_security.xml',
        'security/ir.model.access.csv',
        'data/image.xml',
        'data/login.xml',
        'data/register.xml',
        'data/mail_template.xml',
        'views/report/ctrl_register_template.xml',
        'views/report/fees_template.xml',
        'views/report/fees_report.xml',
        'views/report/register_template.xml',
        'views/report/sample.xml',
        'views/home_page.xml',
        'views/courses.xml',
        'views/register.xml',
        'views/configure.xml',
        'views/instructor.xml',
        'views/student.xml',
        'views/payment.xml',
        'views/marks.xml',
        'views/res_users.xml',
        'wizard/wizard_report.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}
