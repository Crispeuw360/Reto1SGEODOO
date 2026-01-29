{
    'name': 'Reto1SGEODOO',
    'version': '1.0',
    'summary': 'Sistema de gestión de incidencias',
    'category': 'Services',
    'author': 'Tu Nombre',
    'website': 'https://www.tudominio.com',
    'depends': ['base', 'hr', 'mail',"project"],
    'data': [
        # 1. PRIMERO: Seguridad
        'security/groups.xml',
        'security/ir.model.access.csv',

        # 2. SEGUNDO: Acciones (DEBE estar ANTES de las vistas)
        'views/actions.xml',

        # 3. TERCERO: Vistas (que referencian las acciones)
        'views/incidencia_views.xml',
        'views/Comentario_views.xml',

        # 4. CUARTO: Menús (que referencian las acciones)
        'views/menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}