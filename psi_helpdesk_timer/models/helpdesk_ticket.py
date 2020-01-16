# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from math import ceil

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'
    
    psi_timesheet_timer_start = fields.Datetime("Timesheet Timer Start", default=None)
    psi_timesheet_timer_pause = fields.Datetime("Timesheet Timer Last Pause")
    psi_timesheet_timer_first_start = fields.Datetime("Timesheet Timer First Use", readonly=True)
    psi_timesheet_timer_last_stop = fields.Datetime("Timesheet Timer Last Use", readonly=True)
    psi_display_timesheet_timer = fields.Boolean("Display Timesheet Time", compute='_compute_display_timesheet_timer')

    @api.depends('task_id.allow_timesheets', 'project_id.allow_timesheet_timer', 'task_id.analytic_account_active')
    def _compute_display_timesheet_timer(self):
        for ticket in self:
            ticket.psi_display_timesheet_timer = ticket.project_id.allow_timesheet_timer

    # ---------------------------------------------------------
    # Timer Methods
    # ---------------------------------------------------------

    def action_timer_start(self):
        self.ensure_one()
        # Get list of tickets for user that are in a started status (from model helpdesk)
        if not self.psi_timesheet_timer_first_start:
            self.write({'psi_timesheet_timer_first_start': fields.Datetime.now()})
        return self.write({'psi_timesheet_timer_start': fields.Datetime.now()})

    def action_timer_pause(self):
        self.write({'psi_timesheet_timer_pause': fields.Datetime.now()})

    def action_timer_resume(self):
        new_start = self.psi_timesheet_timer_start + (fields.Datetime.now() - self.psi_timesheet_timer_pause)
        self.write({
            'psi_timesheet_timer_start': new_start,
            'psi_timesheet_timer_pause': False
        })

    def action_timer_stop(self):
        self.ensure_one()
        start_time = self.psi_timesheet_timer_start
        if start_time:  # timer was either running or paused
            pause_time = self.psi_timesheet_timer_pause
            if pause_time:
                start_time = start_time + (fields.Datetime.now() - pause_time)
            minutes_spent = (fields.Datetime.now() - start_time).total_seconds() / 60
            minutes_spent = self._timer_rounding(minutes_spent)
            return self._action_create_timesheet(minutes_spent * 60 / 3600)
        return False

    def _timer_rounding(self, minutes_spent):
        minimum_duration = int(self.env['ir.config_parameter'].sudo().get_param('sale_timesheet_enterprise.timesheet_min_duration', 0))
        rounding = int(self.env['ir.config_parameter'].sudo().get_param('sale_timesheet_enterprise.timesheet_rounding', 0))
        minutes_spent = max(minimum_duration, minutes_spent)
        if rounding and ceil(minutes_spent % rounding) != 0:
            minutes_spent = ceil(minutes_spent / rounding) * rounding
        return minutes_spent

    # ---------------------------------------------------------
    # Business Methods
    # ---------------------------------------------------------

    def _action_create_timesheet(self, time_spent):
        return {
            "name": _("Confirm Time Spent"),
            "type": 'ir.actions.act_window',
            "res_model": 'helpdesk.ticket.create.timesheet',
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
                'active_id': self.id,
                'active_model': 'helpdesk.ticket',
                'default_time_spent': time_spent,
            },
        }