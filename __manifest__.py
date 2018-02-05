{
    'name': 'Tourist agency management',
    'category': 'travel',
    'description': """
        This module have basics to manage Tourist agency
    """,
    'version': '0.0.1',
    'data': [
        'views/res_partner_views.xml',
        'views/travel_place_view.xml',
        'views/offer_view.xml',
        'views/res_currency_views.xml',
        'views/travel_views.xml',
        # data
        'data/ir_sequence_data.xml',
        'data/travel_type_data.xml',
        'data/travel_way_data.xml',
        'data/companies_data.xml',
    ],
    'depends': ['base_setup', 'mail'],
    'install': True,
    'application': True,
}