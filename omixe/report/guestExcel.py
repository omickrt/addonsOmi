from odoo import api, fields, models


class partnerXlsx(models.Model):
    _name = 'report.omixe.report_guest_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    reportDate = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, guest):
        sheet = workbook.add_worksheet('Guest List')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.reportDate))
        sheet.write(1, 0, 'Name', bold)
        sheet.write(1, 1, 'ID Number', bold)
        sheet.write(1, 2, 'Phone Number', bold)
        sheet.write(1, 3, 'Email', bold)

        row = 2
        col = 0
        for obj in guest:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.noId)
            sheet.write(row, col+2, obj.phone)
            sheet.write(row, col+3, obj.email)
            row += 1