from odoo import fields, models, api


class transactionReport(models.TransientModel):
    _name = 'omixe.transactionreport'
    _description = 'Description'

    transId = fields.Many2one(comodel_name='omixe.transaction', string='Guest')
    From = fields.Date(string='From')
    To = fields.Date(string='To')

    def action_transactionreport(self):
        filter = []
        transId = self.transId
        From = self.From
        To = self.To
        if transId:
            filter += [('guestId', '=', transId.id)]
        if From:
            filter += [('date', '>=', From)]
        if To:
            filter += [('date', '<=', To)]
        print(filter)
        trans = self.env['omixe.transaction'].search_read(filter)
        print(trans)
        data = {
            'form': self.read()[0],
            'x': trans,
        }
        print(data)
        return self.env.ref('omixe.printreport_pdf').report_action(self, data=data)
    