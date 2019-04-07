# coding: utf-8
from odoo import models, fields, api


_TYPES_MESURE = [
    ('pelleterie', 'Pelleterie'),
    ('longueur', 'Longueur'),
    ('unité', 'Unité'),
    ('poids', 'Poids'),
    ('longeur', 'Longueur'),
    ('', 'N/A'),
]


class Achat(models.Model):
    _name = 'myosotis.achat'

    transaction_id = fields.Many2one(
        'myosotis.transaction',
        string="Transaction"
    )
    date_achat = fields.Date()
    prix_total_id = fields.Many2one(
        'myosotis.prix',
        string="Prix Total"
    )
    prix_unitaire_id = fields.Many2one(
        'myosotis.prix',
        string="Prix Unitaire"
    )
    quantite = fields.Float()
    quantite_plusieurs = fields.Boolean(
        help='Vrai si quantité est "plusieurs"'
    )
    remarques = fields.Text()


class AchatFabrication(models.Model):
    _name = 'myosotis.achat.fabrication'
    _inherits = 'myosotis.achat'

    parure_id = fields.Many2one(
        'myosotis.parure',
        string='Parure'
    )
    avec_mat = fields.One2many(
        'myosotis.fabrique.avec.mat', 'achat_fabrication_id',
        string="Avec Matériaux"
    )


class AchatMateriaux(models.Model):
    _name = 'myosotis.achat.materiaux'
    _inherits = 'myosotis.achat'

    type_mesure = fields.Selection(  # XXX extract to 'myosotis.unit'
        _TYPES_MESURE,
    )
    unit = fields.Char()
    provenance_mesure = fields.Char()
    materiaux_id = fields.Many2one(
        "myosotis.materiaux",
        string="Matériaux"
    )


class AchatPretPorter(models.Model):
    _name = 'myosotis.achat.pretporter'
    _inherits = 'myosotis.achat'

    parure_id = fields.Many2one(
        'myosotis.parure',
        string='Parure'
    )


class FabriqueAvecMat(models.Model):
    _name = 'myosotis.fabrique.avec.mat'

    type_mesure = fields.Selection(
        _TYPES_MESURE
    )
    quantite = fields.Float()
    unit = fields.Char()
    provenance_mesure = fields.Char()
    conversion = fields.Float()
    usage = fields.Text()
    achat_fabrication_id = fields.Many2one(
        'myosotis.achat.fabrication'
    )
    achat_matiere_id = fields.Many2one(  # to check
        'myosotis.achat.materiaux',
        string='Achat Matière',
        # TODO : domain to force both achats in the same compte
    )
