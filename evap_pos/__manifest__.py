# -*- coding: utf-8 -*-

{
    'name': 'EVAP Point of Sale and Loyalty Customizations',
    'version': '1.0',
    'summary': 'Point of Sale and Loyalty Customizations',
    'category': 'Point of Sale',
    'description': '',
    'depends': ['pos_loyalty', 'account', 'evap_purchase'],
    'data': [
        'data/email_template.xml',
        'data/paperformats.xml',

        'views/assets.xml',
        'views/partner_view.xml',
        'views/pos_order_line_views.xml',

        'wizard/sale_invoice_view.xml',

        'report/report_invoice.xml',
        'report/report_session.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'installable': True,
}
