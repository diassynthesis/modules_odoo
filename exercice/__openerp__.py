# -*- coding: utf-8 -*-
{
    'name': 'EXERCICE',
    'version': '1.0.0',
    'category': 'Tests',
    'sequence': 7,
    'author': 'KONE Aziz',
    'summary': 'Gestion des etudiants dans un etablissement scolaire',
    'description': """Gestion des etudiants""",
    'depends': [],
    'data': [
        'views/exercice_list_view.xml',
        'views/exercice_form_view.xml',
        'views/exercice_menu_action_view.xml',
        'exercice_data_view.xml',
    ],
    'test': [
        'test/exercice_test.yml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}