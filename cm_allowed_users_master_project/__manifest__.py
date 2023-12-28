{
    'name': 'cm_allowed_users_master_project',
    'version': '1.0',
    'summary': 'Add extra delivery charge to Purchase Order lines',
    'description': 'This module adds an extra delivery charge to the subtotal in Purchase Order lines.',
    'category': 'Purchase',
    'author': 'Abhinay',
    'website': 'https://www.example.com',
    'depends': ['purchase','base'],
    'data': [
        'views/charge.xml',
    ],
    'installable': True,
    'application': False,
}
