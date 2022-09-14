from odoo import api, fields, models
from odoo.exceptions import ValidationError


class guest(models.Model):
    _name = 'omixe.guest'
    _description = 'Guest'

    name = fields.Char(string='Name', required=True)
    noId = fields.Char(string='ID Number', required=True)
    phone = fields.Char(string='Phone Number', required=True)
    email = fields.Char(string='Email')

        
    @api.constrains('noId')
    def _check_noId(self):
        for rec in self:
            if rec.noId:
                a = self.env['omixe.guest'].search([('id','!=',rec.id),('noId','=',rec.noId)])
                if a:
                    raise ValidationError("ID Number was already existed.")

    
    