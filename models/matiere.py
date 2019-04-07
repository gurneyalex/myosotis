from odoo import models, fields


class Materiaux(models.Model):
    _name = 'myosotis.materiaux'

    name = fields.Char(required=True)
    type = fields.Selection([('E', 'E'),
                             ('F', 'F'),
                             ('M', 'M'),
                             ('O', 'O'),
                             ('B', 'B'),
                             ('P', 'P'),
                             ('?', '?'),
                             ], required=True)
    famille = fields.Selection([('laine', 'laine'),
                                ('toile', 'toile'),
                                (u'mélangé', 'mélangé'),
                                ('NA', 'NA'),
                                ('soie', 'soie'),
                                ], default='laine',
                               required=True)
    couleur = fields.Char()
    carac_couleur = fields.Char()
    carac_facture = fields.Char()
    provenance_id = fields.Many2one('myosotis.location')
    
