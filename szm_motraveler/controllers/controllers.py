# -*- coding: utf-8 -*-
# from odoo import http


# class SzmMotraveler(http.Controller):
#     @http.route('/szm_motraveler/szm_motraveler/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/szm_motraveler/szm_motraveler/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('szm_motraveler.listing', {
#             'root': '/szm_motraveler/szm_motraveler',
#             'objects': http.request.env['szm_motraveler.szm_motraveler'].search([]),
#         })

#     @http.route('/szm_motraveler/szm_motraveler/objects/<model("szm_motraveler.szm_motraveler"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('szm_motraveler.object', {
#             'object': obj
#         })
