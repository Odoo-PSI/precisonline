# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    psi_company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True, relation="res.currency")
    psi_sale_amount_total = fields.Monetary(compute='_compute_sale_data', string="Sum of Orders", help="Untaxed Total of Confirmed Orders", currency_field='psi_company_currency')
    psi_quotation_count = fields.Integer(compute='_compute_sale_data', string="Number of Quotations")
    psi_sale_order_count = fields.Integer(compute='_compute_sale_data', string="Number of Sale Orders")
    psi_order_ids = fields.One2many('sale.order', 'psi_ticket_id', string='Orders')

    @api.depends('psi_order_ids.state', 'psi_order_ids.currency_id', 'psi_order_ids.amount_untaxed', 'psi_order_ids.date_order', 'psi_order_ids.company_id')
    def _compute_sale_data(self):
        for ticket in self:
            total = 0.0
            quotation_cnt = 0
            sale_order_cnt = 0
            company_currency = ticket.psi_company_currency or self.env.company.currency_id
            for order in ticket.psi_order_ids:
                if order.state in ('draft', 'sent'):
                    quotation_cnt += 1
                if order.state not in ('draft', 'sent', 'cancel'):
                    sale_order_cnt += 1
                    total += order.currency_id._convert(
                    order.amount_untaxed, company_currency, order.company_id, order.date_order or fields.Date.today())
            ticket.psi_sale_amount_total = total
            ticket.psi_quotation_count = quotation_cnt
            ticket.psi_sale_order_count = sale_order_cnt

    # ---------------------------------------------------------
    # Business Methods
    # ---------------------------------------------------------
    def action_sale_quotations_new(self):
        if not self.partner_id:
            return self.env.ref("sale_crm.crm_quotation_partner_action").read()[0]
        else:
            return self.action_new_quotation()

    def action_new_quotation(self):
        temp_cnt = self.psi_quotation_count + self.psi_sale_order_count + 1
        action = self.env.ref("sale_crm.sale_action_quotations_new").read()[0]
        action['context'] = {
            'search_default_psi_ticket_id': self.id,
            'default_psi_ticket_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.team_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_name':"T{:05}-{:02}".format(self.id,temp_cnt),
        }
        return action

    def action_view_sale_quotation(self):
        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_psi_ticket_id': self.id
        }
        action['domain'] = [('psi_ticket_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.mapped('psi_order_ids').filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    def action_view_sale_order(self):
        action = self.env.ref('sale.action_orders').read()[0]
        action['context'] = {
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_psi_ticket_id': self.id,
        }
        action['domain'] = [('psi_ticket_id', '=', self.id), ('state', 'not in', ('draft', 'sent', 'cancel'))]
        orders = self.mapped('psi_order_ids').filtered(lambda l: l.state not in ('draft', 'sent', 'cancel'))
        if len(orders) == 1:
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = orders.id
        return action