# coding: utf-8
from odoo import models, fields, api


class Transaction(models.Model):
    _name = 'myosotis.transaction'

    date = fields.Date()
    type_achat = fields.Char()  # to remove ?
    pagination = fields.Char()
    date_ordre = fields.Date()
    date_recette = fields.Date()
    remarques = fields.Text()
    intervenant_ids = fields.One2many(
        'myosotis.intervenant', 'transaction_id',
        string="Intervenants"
    )
    destinataire_ids = fields.One2many(
        'myosotis.destinataire', 'transaction_id',
        string="Destinataires"
    )
    travail_ids = fields.Many2many(
        'myosotis.travail',
        string='Travaux'
    )
    vendeur_ids = fields.One2many(
        'myosotis.vendeur', 'transaction_id',
        string="Vendeurs"
    )
    prix_partage = fields.Boolean()
    base_paradox = fields.Boolean()
    compte_id = fields.Many2one(
        'myosotis.compte',
        string='Compte',
        required=True)
    prix_ensemble_id = fields.Many2one(
        'myosotis.prix',
        string="Prix Ensemble"
    )
    occasion_id = fields.Many2one(
        'myosotis.occasion',
        string="Occasion"
    )
    achat_ids = fields.One2many('myosotis.achat', 'transaction_id')
    location_id = fields.Many2one('myosotis.location')
    change_ids = fields.One2many(
        'myosotis.change', 'transaction_id',
        string='Changes'
    )
