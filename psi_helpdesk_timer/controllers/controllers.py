# -*- coding: utf-8 -*-
# from odoo import http


# class PsiHelpdeskTimer(http.Controller):
#     @http.route('/psi_helpdesk_timer/psi_helpdesk_timer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/psi_helpdesk_timer/psi_helpdesk_timer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('psi_helpdesk_timer.listing', {
#             'root': '/psi_helpdesk_timer/psi_helpdesk_timer',
#             'objects': http.request.env['psi_helpdesk_timer.psi_helpdesk_timer'].search([]),
#         })

#     @http.route('/psi_helpdesk_timer/psi_helpdesk_timer/objects/<model("psi_helpdesk_timer.psi_helpdesk_timer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('psi_helpdesk_timer.object', {
#             'object': obj
#         })
