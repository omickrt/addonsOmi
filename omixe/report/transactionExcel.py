from odoo import api, fields, models


class partnerXlsx(models.Model):
    _name = 'report.omixe.report_transaction_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    report_date = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, guest):
        sheet = workbook.add_worksheet('Guest List')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.report_date))
        sheet.write(1, 0, 'No.Nota', bold)
        sheet.write(1, 1, 'Guest Name', bold)
        sheet.write(1, 2, 'Transaction Date', bold)
        sheet.write(1, 3, 'Room Type', bold)
        sheet.write(1, 4, 'Guests/room', bold)
        sheet.write(1, 5, 'Room(s)', bold)
        sheet.write(1, 6, 'Extra Bed', bold)
        sheet.write(1, 7, 'Status', bold)
        sheet.write(1, 8, 'Total Price (+VAT)', bold)

        row = 2
        col = 0
        for obj in guest:
            col = 0
            sheet.write(row, col, obj.name)
            for x in obj.guest_id:
                sheet.write(row, col+1, x.name)
            sheet.write(row, col+2, str(obj.date))
            for x in obj.room_id:
                sheet.write(row, col+3, x.name)
            sheet.write(row, col+4, obj.maks)
            sheet.write(row, col+5, obj.item)
            sheet.write(row, col+6, obj.bed)
            sheet.write(row, col+7, obj.state)
            sheet.write(row, col+8, obj.total)
            row+=1