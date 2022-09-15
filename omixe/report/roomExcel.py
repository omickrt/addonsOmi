from odoo import api, fields, models


class partnerXlsx(models.Model):
    _name = 'report.omixe.report_room_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    report_date = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, guest):
        sheet = workbook.add_worksheet('Guest List')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.report_date))
        sheet.write(1, 0, 'Room Type', bold)
        sheet.write(1, 1, 'Max Guests', bold)
        sheet.write(1, 2, 'Room Price', bold)
        sheet.write(1, 3, 'Availability', bold)
        sheet.write(1, 4, 'Transaction List', bold)

        row = 2
        col = 0
        for obj in guest:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col+1, obj.person)
            sheet.write(row, col+2, obj.price)
            sheet.write(row, col+3, obj.avail)
            for x in obj.trans_ids:
                sheet.write(row, col+4, x.guest_id.name)
                col += 1
            row+=1