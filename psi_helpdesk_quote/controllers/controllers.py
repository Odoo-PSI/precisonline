# -*- coding: utf-8 -*-
# from odoo import http


# class PsiHelpdeskQuote(http.Controller):
#     @http.route('/psi_helpdesk_quote/psi_helpdesk_quote/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/psi_helpdesk_quote/psi_helpdesk_quote/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('psi_helpdesk_quote.listing', {
#             'root': '/psi_helpdesk_quote/psi_helpdesk_quote',
#             'objects': http.request.env['psi_helpdesk_quote.psi_helpdesk_quote'].search([]),
#         })

#     @http.route('/psi_helpdesk_quote/psi_helpdesk_quote/objects/<model("psi_helpdesk_quote.psi_helpdesk_quote"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('psi_helpdesk_quote.object', {
#             'object': obj
#         })
