# -*- coding: utf-8 -*-
{
    'name': 'PSI Helpdesk Quote',

    'summary': 'Add Quote function to Helpdesk Module',

    'description': """
        12-16-19 - Jeff Mueller, Add Quote button and views to Helpdesk Ticket.
    """,

    'author': "Precision Solutions, Inc",
    'website': "http://www.precisonline.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Operations/Helpdesk',
    'sequence': 50,
    'version': '0.2',
    'installable': True,
    'application': False,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['crm', 'helpdesk', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ]
}