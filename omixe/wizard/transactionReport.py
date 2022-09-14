from odoo import fields, models, api


class transactionReport(models.TransientModel):
    _name = 'omixe.transactionreport'
    _description = 'Description'

    guestId = fields.Many2one(comodel_name='omixe.guest', string='Guest')
    From = fields.Date(string='From')
    To = fields.Date(string='To')

    def action_transactionreport(self):
        filter = []
        guestId = self.guestId
        From = self.From
        To = self.To
        if guestId:
            filter += [('name', '=', guestId.id)]
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
    