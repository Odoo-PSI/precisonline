# -*- coding: utf-8 -*-
from odoo import http

# class PsiTaskToHelpdesk(http.Controller):
#     @http.route('/psi_task_to_helpdesk/psi_task_to_helpdesk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/psi_task_to_helpdesk/psi_task_to_helpdesk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('psi_task_to_helpdesk.listing', {
#             'root': '/psi_task_to_helpdesk/psi_task_to_helpdesk',
#             'objects': http.request.env['psi_task_to_helpdesk.psi_task_to_helpdesk'].search([]),
#         })

#     @http.route('/psi_task_to_helpdesk/psi_task_to_helpdesk/objects/<model("psi_task_to_helpdesk.psi_task_to_helpdesk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('psi_task_to_helpdesk.object', {
#             'object': obj
#         })