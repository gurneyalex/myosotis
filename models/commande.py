# coding: utf-8
from odoo import models, fields, api


class Commande(models.Model):
    _name = 'myosotis.commande'

    numero = fields.Integer(required=True)
    prix_str = fields.Char()
    date_ordre_str = fields.Char()
    transaction_ids = fields.One2many('myosotis.transaction', 'commande_id')
    compte_id = fields.Many2one('myosotis.compte', required=True)
