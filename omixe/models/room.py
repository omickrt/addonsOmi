from odoo import api, fields, models


class room(models.Model):
    _name = 'omixe.room'
    _description = 'Room Type'
    
    name = fields.Selection(string='Room List', selection=[
        ('Single Room', 'Single Room'), 
        ('Double Room', 'Double Room'),
        ('Queen Room', 'Queen Room'),
        ('Family Room', 'Family Room'),
        ('Deluxe Room', 'Deluxe Room'),
        ('Superior Room', 'Superior Room'),
        ('Suite Room', 'Suite Room'),
        ])
    
    person = fields.Integer(string='Max Guests')
    price = fields.Integer(string='Price List (not include VAT)')
    
    @api.onchange('name')
    def _onchange_name(self):
        if (self.name == 'Single Room'):
            self.person = 1
            self.price = 100000
        if (self.name == 'Double Room'):
            self.person = 2
            self.price = 150000
        if (self.name == 'Queen Room'):
            self.person = 2
            self.price = 200000
        if (self.name == 'Family Room'):
            self.person = 4
            self.price = 300000
        if (self.name == 'Deluxe Room'):
            self.person = 2
            self.price = 450000
        if (self.name == 'Superior Room'):
            self.person = 2
            self.price = 750000
        if (self.name == 'Suite Room'):
            self.person = 2
            self.price = 1000000
    
    
    
    avail = fields.Integer(string='Availability (Room)')
    transIds = fields.One2many(comodel_name='omixe.transaction', inverse_name='roomId', string='Transaction List')
    desc = fields.Char(string='Description')
    
    
    
    