from odoo import api, fields, models
from odoo.exceptions import ValidationError


class transaction(models.Model):
    _name = 'omixe.transaction'
    _description = 'Transaction'

    name = fields.Integer(string='Invoice Number', required=True)
    date = fields.Datetime(string='Transaction Date', default=fields.Datetime.now())
    maks = fields.Integer(string='Guests/room', required=True)
    item = fields.Integer(string='Room(s)', required=True)
    total = fields.Integer(string='Total Price (+VAT 15%)', compute='_compute_total')
    guestId = fields.Many2one(comodel_name='omixe.guest', string='Guest List', required=True)
    roomId = fields.Many2one(comodel_name='omixe.room', string='Room List', required=True)    
    bed = fields.Selection(string='Extra Bed', selection=[
                            ('noExtra', 'No Extra Bed'), 
                            ('single', 'Single Bed (+1 guest)'), 
                            ('queen', 'Queen Bed (+2 guests)')],
                           required=True, default='noExtra')
    prices = fields.Integer(string='Extra Price')
    state = fields.Selection(string='Status', selection=[
                            ('onprogress', 'On Progress'), 
                            ('confirm', 'Confirm'),
                            ('done', 'Done'),
                            ('cancel', 'Cancelled')],
                             required=True, readonly=True, default='onprogress')
    
     
    def action_confirm(self):
        self.write({'state': 'confirm'})
    def action_done(self):
        self.write({'state': 'done'})
    def action_cancel(self):
        self.write({'state': 'cancel'})
    def action_onprogress(self):
        self.write({'state': 'onprogress'})
    
    
    @api.onchange('bed')
    def _onchange_prices(self):
        if (self.bed == 'noExtra'):
            self.prices = 0
        elif (self.bed == 'single'):
            self.prices = 50000
        elif (self.bed == 'queen'):
            self.prices = 75000    
    
    
    _sql_constraints = [
        (
            'nota_unique',
            'unique (name)',
            ('This Invoice Number was already existed.')
        )
    ]
    
    
    @api.constrains('bed')
    def _check_bed(self):
        for rec in self:
            if rec.bed == 'single' and rec.roomId.name == 'Single Room':
                raise ValidationError('Sorry, {} is not allowed to add an extra bed.'.format(rec.roomId.name))
            elif rec.bed == 'queen' and rec.roomId.name == 'Single Room':
                raise ValidationError('Sorry, {} is not allowed to add an extra bed.'.format(rec.roomId.name))
            elif rec.bed == 'single' and rec.roomId.name == 'Double Room':
                raise ValidationError('Sorry, {} is not allowed to add an extra bed.'.format(rec.roomId.name))
            elif rec.bed == 'queen' and rec.roomId.name == 'Double Room':
                raise ValidationError('Sorry, {} is not allowed to add an extra bed.'.format(rec.roomId.name))
            
            
    @api.depends('total')
    def _compute_total(self):
        for rec in self:
            rec.total = ((rec.roomId.price * 0.15) + rec.roomId.price) * rec.item + rec.prices + (rec.prices * 0.15)
    
    
    @api.constrains('maks')
    def _check_maks(self):
        for rec in self:
            if rec.maks > rec.roomId.person:
                raise ValidationError("The maximum guest(s) in this room is {}. Please book another room or add an extra bed.".format(rec.roomId.person))
            elif rec.maks < 1:
                raise ValidationError("Please input guests more than {}".format(rec.maks))
    
             
    @api.constrains('item')
    def check_quantity(self):
        for rec in self:
            if rec.item < 1:
                raise ValidationError("Please input rooms more than {}.".format(rec.item))
            elif (rec.roomId.avail < rec.item):
                raise ValidationError("Sorry, {} is not available now. Please check another room.".format(rec.roomId.name))


    @api.ondelete(at_uninstall=False)
    def _ondelete_transaction(self):
        if self.filtered(lambda line: line.state != 'cancel'):
            raise ValidationError("Can only delete it if the status is 'Cancelled'")
        else:
            if self.roomId.transIds:
                a = []
                for rec in self:
                    a = self.env['omixe.transaction'].search([('roomId','=', rec.roomId.id)])
                    print(a)
                    for b in a:
                        print(str(b.roomId.name) + ' ' + str(b.item))
                        b.roomId.avail += b.item
    
    
    def write(self, vals):
        for rec in self:
            a = self.env['omixe.room'].search([('transIds', '=', rec.id)])
            print(a)
            for data in a:
                print(str(data.name) + ' ' + str(data.transIds.item) + ' ' + str(data.avail))
                data.avail += data.transIds.item
        res = super(transaction,self).write(vals)
        for rec in self:
            b = self.env['omixe.room'].search([('transIds', '=', rec.id)])
            print(a)   
            print(b)
            for databaru in b:
                if databaru in a:
                    print(str(databaru.name) + ' ' + str(databaru.transIds.item) + ' ' + str(databaru.avail))
                    databaru.avail -= databaru.transIds.item
                else:
                    pass
        return res
    
    
    @api.model
    def create(self, vals):
        rec = super(transaction,self).create(vals)
        if rec.item:
            self.env['omixe.room'].search([('id', '=', rec.roomId.id)]).write({'avail': rec.roomId.avail - rec.item})
        return rec
    
    
    