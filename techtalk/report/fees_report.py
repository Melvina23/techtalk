from odoo import api,fields,models

class FeesPayment(models.AbstractModel):
    _name = 'report.techtalk.report_fees_template'
    _description = 'payment report'

    def _get_report_values(self,docids, data):
        f_date = data['date_from']
        t_date = data['date_to']
        payment_records = self.env['tech.payment'].search([('pay_date', '>=', f_date),('pay_date', '<=', t_date)])
        return {
            'doc_ids': self.ids,
            'payment_records': payment_records
        }

class ReportXlsx(models.AbstractModel):
    _name = 'report.techtalk.fees_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Fees report'

    def generate_xlsx_report(self, workbook, data, obj):
        f_date = data['date_from']
        t_date = data['date_to']
        payment_records = self.env['tech.payment'].search([('pay_date', '>=', f_date), ('pay_date', '<=', t_date)])
        worksheet = workbook.add_worksheet('Fees Details')
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D1D1D1', 'border': 0, 'font_size': 11,
                                             'font_name': 'arial', 'indent': 1})
        val_format = workbook.add_format(
            {'align': 'left', 'font_size': 11, 'font_name': 'arial', 'indent': 1, 'text_wrap': True, 'valign': 'top'})

        row = 0
        # col = 0
        column_widths = {
            'A': 10,
            'B': 15,
            'C': 25,
            'D': 15,
            'E': 20,
            'F': 10,
            'G': 20,
        }
        for col, width in column_widths.items():
            worksheet.set_column(f'{col}:{col}', width)

        # Header row
        headers = ['S.No','Payment ID','Student Name','Payment Date','Course Name','Amount','Payment Method']
        col = 0
        for header in headers:
            worksheet.write(row, col, header, header_format)
            col += 1

        row += 1

        S_no = 1
        for record_id in payment_records:
            col = 0
            # col +=
            worksheet.write(row, col, S_no, val_format)
            col += 1
            worksheet.write(row, col, (record_id.number), val_format)
            col += 1
            worksheet.write(row, col, str(record_id.name), val_format)
            col += 1
            req = record_id.pay_date.strftime('%d-%m-%Y') if record_id.pay_date else ''
            worksheet.write(row, col, req, val_format)
            col += 1
            worksheet.write(row, col, str(record_id.course_id.name), val_format)
            col += 1
            worksheet.write(row, col, int(record_id.amount), val_format)
            col += 1
            worksheet.write(row, col, str(record_id.status), val_format)
            col += 1
            row += 1
            S_no +=1

