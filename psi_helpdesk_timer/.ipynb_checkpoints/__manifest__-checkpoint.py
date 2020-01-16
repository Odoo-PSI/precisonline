# -*- coding: utf-8 -*-
{
    'name': 'PSI Helpdesk Timer',

    'summary': 'Add Timer function to Helpdesk Module',

    'description': """
        01-14-20 - Jeff Mueller, Add Timer functions to Helpdesk Ticket.
    """,

    'author': "Precision Solutions, Inc",
    'website': "http://www.precisonline.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Helpdesk',
    'sequence': 50,
    'version': '0.1',
    'installable': True,
    'application': False,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['helpdesk', 'timesheet_grid', 'sale_management'],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_ticket_create_timesheet.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ]
}
