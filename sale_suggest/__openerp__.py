# -*- coding: utf-8 -*-
###############################################################################
#
#   sale_suggest for OpenERP
#   Copyright (C) 2014-TODAY Akretion <http://www.akretion.com>.
#   @author Arthur Vuillard <arthur.vuillard@akretion.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'sale_suggest',
    'version': '0.1',
    'category': 'Generic Modules/Others',
    'license': 'AGPL-3',
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'description': """
Product suggestion in a sale order
==================================

Features :
----------
    * 

Technical informations :
------------------------
    * 
""",
    'depends': [
        'sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/wizard_suggestions.xml',
        'views/sale.xml',
    ],
    'demo': ['tests/data.xml'],
    'installable': True,
}
