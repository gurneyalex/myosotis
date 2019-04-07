from odoo import models, fields


class Personne(models.Model):
    _name = 'myosotis.personne'

    identity = fields.Char(required=True)
    nom = fields.Char()
    surnom = fields.Char()
    diminutif = fields.Char()
    titre = fields.Char()
    sexe = fields.Selection(
        [('M', 'Homme'),
         ('F', 'Femme'),
         ('?', '?')],
        required=True,
        default='M'
    )
    ville_domicile = fields.Char()
    ville_origine = fields.Char()
    location_domicile_id = fields.Many2one('myosotis.location')
    location_origine_id = fields.Many2one('myosotis.location')
    remarks = fields.Text()
    rattachement = fields.Char()
    base_paradox = fields.Boolean(help='vient de la base Paradox')
    occupation_ids = fields.One2many(
        'myosotis.occupation', 'personne_id'
    )


class Occupation(models.Model):
    _name = 'myosotis.occupation'

    libelle = fields.Char()
    valeur = fields.Char()
    compte_id = fields.Many2one('myosotis.compte')
    annee = fields.Integer()
    pagination = fields.Char()
    rattached_id = fields.Many2one(
        'myosotis.personne'
    )
    occupation = fields.Char()
    personne_id = fields.Many2one('myosotis.personne')


class Travail(models.Model):
    _name = 'myosotis.travail'

    artisan_id = fields.Many2one('myosotis.personne', required=True)
    salaire_argent_id = fields.Many2one('myosotis.prix')
    salaire_nature_qt = fields.Integer()
    salaire_nature_obj = fields.Char()
    nombre_aides = fields.Integer()
    designation_aides = fields.Integer()
    salaire_aides_id = fields.Many2one('myosotis.prix')
    tache = fields.Char()
    duree = fields.Integer()
    date_travail = fields.Date()
    remarques = fields.Text()
    facon_et_etoffe = fields.Boolean()


class Vendeur(models.Model):
    _name = 'myosotis.vendeur'

    expression = fields.Char()
    vendeur_id = fields.Many2one('myosotis.personne', required=True)


class Destinataire(models.Model):
    _name = 'myosotis.destinataire'

    destinataire_id = fields.Many2one('myosotis.personne', required=True)
    nombre = fields.Integer()


class Intervenant(models.Model):
    _name = 'myosotis.intervenant'

    intervenant_id = fields.Many2one('myosotis.personne', required=True)
    indemnite = fields.Integer()
    nb_moyen_transport = fields.Integer()
    moyen_transport = fields.Char()
    prix_transport_id = fields.Many2one('myosotis.prix')
    nombre_valets = fields.Integer()
    prix_valets_id = fields.Many2one('myosotis.prix')
    duree = fields.Integer()  # XXX
    payeur = fields.Boolean()
    pris = fields.Boolean()
    commandement = fields.Boolean()
    relation_de = fields.Boolean()
    donne_par = fields.Boolean()
    par_la_main = fields.Boolean()
    present = fields.Boolean()
    delivre_a = fields.Boolean()
    fait_compte_avec = fields.Boolean()
