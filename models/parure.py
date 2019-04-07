from odoo import models, fields

from .achat import _TYPES_MESURE


class Parure(models.Model):
    _name = 'myosotis.parure'

    type = fields.Char()
    nature = fields.Char()
    caracteristique = fields.Char()
    composition_ids = fields.One2many('myosotis.materiaux.parure', 'parure_id')


class MateriauxParure(models.Model):
    _name = 'myosotis.materiaux.parure'

    type_mesure = fields.Selection(_TYPES_MESURE)
    quantite = fields.Float()
    unite = fields.Char()
    provenance_mesure = fields.Char()
    conversion = fields.Float()

    parure_id = fields.Many2one('myosotis.parure', required=True)
    materiaux_achete = fields.Boolean()
    materiau_id = fields.Many2one('myosotis.materiaux', required=True)
    usage = fields.Char()
