# coding: utf-8
from odoo import models, fields, api


class Prix(models.Model):
    _name = 'myosotis.prix'

    monnaie_id = fields.Many2one('myosotis.monnaie')
    livres = fields.Integer()
    sous = fields.Integer()
    deniers = fields.Float()
    florins = fields.Float()
    florins_ad = fields.Fload()
    gros = fields.Float()
    sous_florins = fields.Integer()
    denier_florins = fields.Integer()
    monnaie_or = fields.Float()
    conversion = fields.Float()
    source = fields.Selection(
        [('direct', 'direct'),
         ('conv_transaction', 'Conversion Transaction'),
         ('conv_compte', 'Conversion Compte'),
         ('conv_voisin', 'Conversion voisin'),
         ('conv_voisin 2', 'Conversion voisin 2nd ordre'),
         ('no_transaction', 'Pas de transaction'),
        ]
    )
    changes = fields.Many2many('myosotis.change')


class Change(models.Model):
    _name = 'myosotis.change'
    compte_id = fields.Many2one('myosotis.compte')
    transaction_id = fields.Many2one('myosotis.transaction')
    price_from_id = fields.Many2one('myosotis.prix')
    price_to_id = fields.Many2one('myosotis.prix')
    

    
class Monnaie(models.Model):
    _name = 'myosotis.monnaie'

    name = fields.Char(required=True, index=True)
    type = fields.Selection(
        [('Livre/Sous/Denier', 'Livre/Sous/Denier'),
         ('Florin/Gros', 'Florin/Gros'),
         ('Or', 'Or'),
        ]
    )
    nb_gros = fields.Float()
