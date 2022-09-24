{
    'name': 'Restaurant Project',
    'version': '14.0.1.0.0',
    'summary': 'This project will help you manage your restaurant properly',
    'sequence': -101,
    'description': """ Restaurant project will help in the managemnt of Restaurant. In this project i am 
    going to implement verious methods.""",
    'category': 'sale and invoicing',
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv',
             'data/sequence.xml',
             'wizard/staff_wizard_view.xml',
             'views/staff_view.xml',
             'views/menu_view.xml',
             ],
    'icon': '/restaurant_project/static/description/Restaurant-icon.png',
    'images': [
        # 'static/description/Restaurant-icon.png',
    ],         
    'demo': [],
    'installable': True,
    'application': True,
    'auto-install': False,
    'license': 'LGPL-3',

}
