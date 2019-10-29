# -*- coding: utf-8 -*-
{
    'name': "psi_timesheet_detail",

    'summary': """
        Task and Helpdesk ticket selection on timesheet details.""",

    'description': """
        Module will remove task header from helpdesk tickets and
        apply task to timesheet details. Time sheet details will
        also be represented on the customer invoice.
    """,

    'author': "Precision Solutions",
    'website': "https://www.precisonline.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'timesheet_grid', 'helpdesk', 'helpdesk_timesheet', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/psi_views.xml',
        'views/psi_qweb.xml',
        # 'views/psi_employee_task_rate.xml',
        # 'data/psi_timesheet_data.xml',
    ],
}