# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    psi_ticket_id = fields.Many2one(
        'helpdesk.ticket', string='Ticket', check_company=True,
        domain="[('active', '=', 'TRUE'), ('company_id', '=', False), ('company_id', '=', company_id)]")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _timesheet_create_project(self):
        """ Generate project for the given so line, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        self.ensure_one()
        account = self.order_id.analytic_account_id
        if not account:
            self.order_id._create_analytic_account(prefix=self.product_id.default_code or None)
            account = self.order_id.analytic_account_id

        # create the project or duplicate one
        values = {
            'name': '%s - %s' % (self.order_id.client_order_ref, self.order_id.name) if self.order_id.client_order_ref else self.order_id.name,
            'allow_timesheets': True,
            'analytic_account_id': account.id,
            'partner_id': self.order_id.partner_id.id,
            'sale_line_id': self.id,
            'sale_order_id': self.order_id.id,
            'active': True,
            'company_id': self.company_id.id,
        }

        if self.product_id.project_template_id:
            """ psi_helpdesk_quote, JRM 2020 Jan 10, Project Name is to be the prefix of the sales order 
            # values['name'] = "%s - %s" % (values['name'], self.product_id.project_template_id.name) -> """
            temp_name = values['name'].split('-')
            values['name'] = temp_name[0]
            """ psi_helpdesk_quote, JRM 2020 Jan 10 <- """
            project = self.product_id.project_template_id.copy(values)
            project.tasks.write({
                'sale_line_id': self.id,
                'partner_id': self.order_id.partner_id.id,
                'email_from': self.order_id.partner_id.email,
            })
            # duplicating a project doesn't set the SO on sub-tasks
            project.tasks.filtered(lambda task: task.parent_id != False).write({
                'sale_line_id': self.id,
            })
            """ psi_helpdesk_quote, JRM 2020 Jan 13, Update Helpdesk Ticket project with newly created
            project ->"""
            ticket = self.order_id.psi_ticket_id
            if ticket:
                ticket.write({
                    'project_id' : project.id
                })
            """ psi_helpdesk_quote, JRM 2020 Jan 13 <- """
        else:
            project = self.env['project.project'].create(values)

        # Avoid new tasks to go to 'Undefined Stage'
        if not project.type_ids:
            project.type_ids = self.env['project.task.type'].create({'name': _('New')})

        # link project as generated by current so line
        self.write({'project_id': project.id})
        return project

    def _timesheet_service_generation(self):
        """ For service lines, create the task or the project. If already exists, it simply links
            the existing one to the line.
            Note: If the SO was confirmed, cancelled, set to draft then confirmed, avoid creating a
            new project/task. This explains the searches on 'sale_line_id' on project/task. This also
            implied if so line of generated task has been modified, we may regenerate it.
        """
        so_line_task_global_project = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking == 'task_global_project')
        so_line_new_project = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking in ['project_only', 'task_in_project'])

        # search so lines from SO of current so lines having their project generated, in order to check if the current one can
        # create its own project, or reuse the one of its order.
        map_so_project = {}
        if so_line_new_project:
            order_ids = self.mapped('order_id').ids
            so_lines_with_project = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), ('product_id.service_tracking', 'in', ['project_only', 'task_in_project']), ('product_id.project_template_id', '=', False)])
            map_so_project = {sol.order_id.id: sol.project_id for sol in so_lines_with_project}
            so_lines_with_project_templates = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), ('product_id.service_tracking', 'in', ['project_only', 'task_in_project']), ('product_id.project_template_id', '!=', False)])
            map_so_project_templates = {(sol.order_id.id, sol.product_id.project_template_id.id): sol.project_id for sol in so_lines_with_project_templates}

        # search the global project of current SO lines, in which create their task
        map_sol_project = {}
        if so_line_task_global_project:
            map_sol_project = {sol.id: sol.product_id.with_context(force_company=sol.company_id.id).project_id for sol in so_line_task_global_project}

        def _can_create_project(sol):
            if not sol.project_id:
                if sol.product_id.project_template_id:
                    return (sol.order_id.id, sol.product_id.project_template_id.id) not in map_so_project_templates
                elif sol.order_id.id not in map_so_project:
                    return True
            return False

        def _determine_project(so_line):
            """Determine the project for this sale order line.
            Rules are different based on the service_tracking:

            - 'project_only': the project_id can only come from the sale order line itself
            - 'task_in_project': the project_id comes from the sale order line only if no project_id was configured
              on the parent sale order"""

            if so_line.product_id.service_tracking == 'project_only':
                return so_line.project_id
            elif so_line.product_id.service_tracking == 'task_in_project':
                return so_line.order_id.project_id or so_line.project_id

            return False

        # task_global_project: create task in global project
        for so_line in so_line_task_global_project:
            if not so_line.task_id:
                if map_sol_project.get(so_line.id):
                    so_line._timesheet_create_task(project=map_sol_project[so_line.id])

        # project_only, task_in_project: create a new project, based or not on a template (1 per SO). May be create a task too.
        # if 'task_in_project' and project_id configured on SO, use that one instead
        for so_line in so_line_new_project:
            project = _determine_project(so_line)
            """ psi_helpdesk_quote, JRM 2020 Jan 10 
            If Project associated to a ticket and a project has already been assigned to the ticket,
            use the existing project and create all subsequent tasks on that project.
            get the project number -> """
            if self.order_id.psi_ticket_id.project_id.allow_billable and not self.order_id.psi_ticket_id.project_id.psi_global_project:
                project = self.order_id.psi_ticket_id.project_id
            """ psi_helpdesk_quote, JRM 2020 Jan 10 """
            if not project and _can_create_project(so_line):
                project = so_line._timesheet_create_project()
                if so_line.product_id.project_template_id:
                    map_so_project_templates[(so_line.order_id.id, so_line.product_id.project_template_id.id)] = project
                else:
                    map_so_project[so_line.order_id.id] = project
            elif not project:
                # Attach subsequent SO lines to the created project
                so_line.project_id = (
                    map_so_project_templates.get((so_line.order_id.id, so_line.product_id.project_template_id.id))
                    or map_so_project.get(so_line.order_id.id)
                )
            if so_line.product_id.service_tracking == 'task_in_project':
                if not project:
                    if so_line.product_id.project_template_id:
                        project = map_so_project_templates[(so_line.order_id.id, so_line.product_id.project_template_id.id)]
                    else:
                        project = map_so_project[so_line.order_id.id]
                if not so_line.task_id:
                    so_line._timesheet_create_task(project=project)
