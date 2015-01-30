{
    'name': "MCI-SOGEM",
    'category': '1.0.0',
    'sequence': 3,
    'author': 'SmileCI',
    'website': 'http://www.smile.ci',
    'summary': 'Gestion de la Sante',
    'description': """
TRANSFORMATION ISA
==============================

This application enables you to manage important aspects of your company's

You can manage:
---------------
* Production
* Medical
* Prestation
* Comptabilite
    """,
    'depends' : [
        'base',
        'web',
        'mail'
    ],
    'data' : [
        'mcisogem_isa_data.xml',
        'views/mcisogem_isa_admin_view.xml',
        'views/mcisogem_isa_production_view.xml',
        'views/mcisogem_isa_tableref_view.xml',
        'views/mcisogem_isa_exercice_police_view.xml',
        'views/mcisogem_isa_medical_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
