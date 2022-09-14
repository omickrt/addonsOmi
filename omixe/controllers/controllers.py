# -*- coding: utf-8 -*-
# from odoo import http


# class Omixe(http.Controller):
#     @http.route('/omixe/omixe', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/omixe/omixe/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('omixe.listing', {
#             'root': '/omixe/omixe',
#             'objects': http.request.env['omixe.omixe'].search([]),
#         })

#     @http.route('/omixe/omixe/objects/<model("omixe.omixe"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('omixe.object', {
#             'object': obj
#         })
