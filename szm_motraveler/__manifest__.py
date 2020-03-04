# -*- coding: utf-8 -*-
{
    'name': 'SZM Hemp Manufacturing Enhancements',

    'summary': 'General Manufacturing Enhancements',

    'description': """
        03/02/2020, Jeff Mueller, Create new Manufacturing Order view that allows fast
                    data entry of consumed material and timesheet entries.
    """,

    'author': "Precision Solutions, Inc",
    'website': "http://www.precisonline.com",

    'category': 'Manufacturing',
    'sequence': 50,
    'version': '0.1',
    'installable': True,
    'application': False,
    'auto_install': False,

    # any module necessary for this one to work correctly
    'depends': ['stock', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_production_views.xml',
        'report/mrp_production_templates.xml',
        'report/mrp_report_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ]
}
