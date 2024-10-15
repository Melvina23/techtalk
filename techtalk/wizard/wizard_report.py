from odoo import api,fields,models

class Report(models.TransientModel):
    _name = 'fees.report'

    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)


    def print_pdf(self):
        data = {}
        data['date_from'] = self.date_from
        data['date_to'] = self.date_to
        print(data)
        return self.env.ref('techtalk.fees_report_wizard').report_action(self, data=data)

    def print_xlsx(self):
        data = {}
        data['date_from'] = self.date_from
        data['date_to'] = self.date_to
        return self.env.ref('techtalk.fees_report_xlsx').report_action(self, data=data)