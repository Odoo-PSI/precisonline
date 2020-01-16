# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError


class HelpdeskTicketCreateTimesheet(models.TransientModel):
    _name = 'helpdesk.ticket.create.timesheet'
    _description = "Create Timesheet for ticket with task"

    _sql_constraints = [('time_positive', 'CHECK(time_spent > 0)', 'The timesheet\'s time must be positive' )]

    @api.model
    def default_get(self, fields):
        result = super(HelpdeskTicketCreateTimesheet, self).default_get(fields)
        active_model = self._context.get('active_model')
        if active_model != 'helpdesk.ticket':
            raise UserError(_("You can only apply this action from a ticket."))

        active_id = self._context.get('active_id')

        if 'task_id' in fields and active_id:
            ticket_id = self.env['helpdesk.ticket'].browse(active_id)
            result['ticket_id'] = active_id
            result['task_id'] = ticket_id.task_id.id
            result['project_id'] = ticket_id.project_id.id
            # result['description'] = ticket_id.name
        return result

    time_spent = fields.Float('Time', precision_digits=2)
    description = fields.Char('Description')
    ticket_id = fields.Many2one('helpdesk.ticket', "Ticket", help="Ticket for which timesheet entry is made", required=True)
    project_id = fields.Many2one('project.project', "Project", help="Project for which timesheet entry is made", required=True)
    task_id = fields.Many2one('project.task', "Task", help="Task for which timesheet entry is made", required=True, domain="[('project_id', '=', project_id)]")

    def save_timesheet(self):
        values = {
            'task_id': self.task_id.id,
            'project_id': self.task_id.project_id.id,
            'helpdesk_ticket_id':self.ticket_id.id,
            'date': datetime.now(),
            'name': self.description,
            'user_id': self.env.uid,
            'unit_amount': self.time_spent,
        }
        self.ticket_id.write({
            'psi_timesheet_timer_start': False,
            'psi_timesheet_timer_pause': False,
            'psi_timesheet_timer_last_stop': fields.datetime.now(),
        })
        self.task_id.write({
            'timesheet_timer_start': False,
            'timesheet_timer_pause': False,
            'timesheet_timer_last_stop': fields.datetime.now(),
        })
        return self.env['account.analytic.line'].create(values)