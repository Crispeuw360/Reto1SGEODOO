# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Incidencias',
    'version': '1.0',
    'summary': 'Sistema de gestión de incidencias',
    'category': 'Services',
    'author': 'Tu Nombre',
    'website': 'https://www.tudominio.com',
    'depends': ['base','hr'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/actions.xml',
        #'views/tree_views.xml',
        #'views/form_views.xml',
        #'views/kanban_views.xml',
        'views/menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
