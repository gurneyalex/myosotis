# coding: utf-8

from odoo import api, fields, models, _


class Compte(models.Model):
    _name = 'myosotis.compte'

    name = fields.Char(compute='_get_name', store=True)
    type_compte = fields.Char(required=True)
    inventaire = fields.Char(required=True, index=True)
    debut = fields.Date()
    fin = fields.Date()
    change_str = fields.Char()  # drop me?
    receveur_id = fields.Many2many('myosotis.personne', string='Receveur')
    base_paradox = fields.Boolean(help='vient de la base Paradox')
    historic = fields.Boolean(
        default=True,
        help="vrai si le compte est historique, "
        "faux s'il s'agit d'un compte utilisé par "
        "exemple pour la gestion des changes"
    )
    change_ids = fields.One2many(
        'myosotis.change', 'compte_id',
        string='Changes'
    )
    commande_ids = fields.One2many(
        'myosotis.commande', 'compte_id',
        string='Commandes')
    commande_count = fields.Integer(
        compute='_get_count_commande',
        store=True
    )
    transaction_ids = fields.One2many(
        'myosotis.transaction', 'compte_id',
        string='Transactions')
    commande_count = fields.Integer(
        compute='_get_count_transaction',
        store=True
    )

    description = fields.Text(compute='_get_description')

    @api.depends('commande_ids')
    def _get_count_commande(self):
        for rec in self:
            rec.commande_count = len(rec.commande_ids)

    @api.depends('transaction_ids')
    def _get_count_transaction(self):
        for rec in self:
            rec.transaction_count = len(rec.transaction_ids)

    @api.depends('inventaire', 'type_compte', 'debut', 'fin')
    def _get_name(self):
        for rec in self:
            if rec.inventaire().startswith('compte'):
                prefix = ''
                type_compte = ''
            else:
                prefix = _('Compte de ')
                type_compte = rec.type_compte + ' '
            rec.name = '%s%s%s [%s %s]' % (
                prefix, type_compte, rec.inventaire, rec.debut, rec.fin)

    @api.depends('transaction_count', 'commande_count')
    def _get_description(self):
        for rec in self:
            title = rec.dc_long_title()
            nb_cdes = rec.commande_count
            nb_trans = rec.transaction_count
            description = '%d commandes, %d transactions' % (nb_cdes, nb_trans)
            rec.description = '\n\n'.join([title,
                                           description])
            # rec.description = '<h2>%s</h2><p>%s</p>' % (xml_escape(title),
            #                                             xml_escape(description))
