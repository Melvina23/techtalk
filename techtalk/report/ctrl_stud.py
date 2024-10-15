from odoo import api,fields,models

class ReportCtrl(models.AbstractModel):
    _name = 'report.techtalk.report_ctrl_stud_template'
    _description = 'Report'

    def _get_report_values(self,docids, data):
        print("*********************")
        print(data)
        p_id   = data['id']
        records = self.env['tech.register'].search([('id', '=', p_id)])
        # print(records)
        return {
            'doc_ids': self.ids,
            'records': records
        }

