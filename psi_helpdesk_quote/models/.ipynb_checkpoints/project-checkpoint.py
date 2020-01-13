# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Project(models.Model):
    _inherit = 'project.project'
    
    psi_global_project = fields.Boolean('Customer General Project?', default=False, help="Identifies if this is a generic support project for a customer.")