# -*- coding: utf-8 -*-
# copyright 2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
# -*- coding: utf-8 -*-
"""cubicweb-myosotis schema"""

from yams.buildobjs import (EntityType, String, Float, SubjectRelation,
                            Int, Boolean, Bytes, Datetime, Date,
                            RichString, RelationDefinition)  #pylint:disable-msg=E0611

# TODO:
# * vérifier les cardinalites
# * renommer les relations 'personne'

class Compte(EntityType):
    type_compte = String(maxsize=255, required=True)
    inventaire = String(maxsize=255, required=True)
    debut = Date()
    fin = Date()
    change = String(maxsize=255)
    receveur = SubjectRelation('Personne', cardinality='**')

class Transaction(EntityType):
    date = Date()
    type_achat = String(maxsize=2) # a virer ?
    pagination = String(maxsize=255)
    date_ordre = Date()
    date_recette = Date()
    remarques = String()
    intervenants = SubjectRelation('Intervenant', composite='subject', cardinality='*1')
    destinataires = SubjectRelation('Destinataire', composite='subject', cardinality='*1')
    artisans = SubjectRelation('Artisan', composite='subject', cardinality='*1')
    vendeurs = SubjectRelation('Vendeur', composite='subject', cardinality='*1')
    prix_partage = Boolean(required=True, default=False)

class compte(RelationDefinition):
    name = 'compte'
    subject = ('Transaction',)
    object = 'Compte'
    cardinality = '1*'
    composite = 'subject'


class achat_mp(RelationDefinition):
    subject = 'Transaction'
    object = 'AchatMateriaux'
    cardinality = '*1'
    composite = 'subject'


class achat_pp(RelationDefinition):
    subject = 'Transaction'
    object = 'AchatPretPorter'
    cardinality = '*1'
    composite = 'subject'


class achat_fa(RelationDefinition):
    subject = 'Transaction'
    object = 'AchatFabrication'
    cardinality = '*1'
    composite = 'subject'



class occasion(RelationDefinition):
    subject = 'Transaction'
    object = 'Occasion'
    cardinality = '?*'

class prix_ensemble(RelationDefinition):
    subject = 'Transaction'
    object = 'Prix'
    cardinality = '?*'
    composite = 'subject'
    inlined=True

class prix_total(RelationDefinition):
    subject = ('AchatFabrication', 'AchatPretPorter', 'AchatMateriaux')
    object = 'Prix'
    cardinality = '??'
    composite = 'subject'
    inlined = True

class prix_unitaire(RelationDefinition):
    subject = ('AchatFabrication', 'AchatPretPorter', 'AchatMateriaux')
    object = 'Prix'
    cardinality = '??'
    composite = 'subject'
    inlined = True

class AchatFabrication(EntityType):
    date_achat = Date()
    quantite = Int()
    parure = SubjectRelation('Parure', cardinality='1*', inlined=True)
    avec_mat = SubjectRelation('FabriqueAvecMat', cardinality='*1')

class AchatMateriaux(EntityType):
    date_achat = Date()
    type_mesure = String(maxsize=255)
    quantite = Float()
    unite = String(maxsize=255)
    provenance_mesure = String(maxsize=255)
    conversion = Float()
    materiaux = SubjectRelation('Materiaux', cardinality='1*', inlined=True)

class AchatPretPorter(EntityType):
    date_achat = Date()
    quantite = Float()
    parure = SubjectRelation('Parure', cardinality='1*', inlined=True)

class Change(EntityType):
    compte = SubjectRelation('Compte', cardinality='?*')
    prix_depart = SubjectRelation('Prix', cardinality='??')
    prix_converti = SubjectRelation('Prix', cardinality='??')

class FabriqueAvecMat(EntityType):
    type_mesure = String(maxsize=255)
    quantite = Float()
    unite = String(maxsize=255)
    provenance_mesure = String(maxsize=255)
    conversion = Float()
    usage = String()
    achat_matiere = SubjectRelation('AchatMateriaux', cardinality='1*')

class Lieu(EntityType):
    ville = String(maxsize=255, required=True)
    region = String(maxsize=255)
    remarques = String()

class lieu(RelationDefinition):
    subject = ('Transaction', 'Occasion')
    object= 'Lieu'
    cardinality = '?*'
    inlined = True

class Personne(EntityType):
    identite = String(maxsize=255, required=True)
    nom = String(maxsize=64)
    surnom = String(maxsize=64)
    diminutif = String(maxsize=64)
    occupation = String(maxsize=30, default='inconnue', required=True)
    titre = String(maxsize=128)
    sexe = String(vocabulary=['M', 'F'], required=True, default='M')
    lieu_domicile = SubjectRelation('Lieu', cardinality='?*', inlined=True)
    lieu_origine = SubjectRelation('Lieu', cardinality='?*', inlined=True)
    remarques= String()
    rattachement = String(maxsize=64)
    maj_occupation= Boolean(default=True)

class Occupation(EntityType):
    libelle = String(maxsize=255)
    valeur = String(maxsize=255)
    compte = SubjectRelation('Compte', cardinality='1*')
    pagination = String(maxsize=64)
    rattache_a = SubjectRelation('Personne', cardinality='?*')
    occupation = String(maxsize=255)
    personne = SubjectRelation('Personne', cardinality = '?*', composite='subject', inlined=True)

class Artisan(EntityType):
    artisan = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)
    salaire_argent = SubjectRelation('Prix', cardinality='??', inlined=True, composite='subject')
    salaire_nature_qt = Int()
    salaire_nature_obj = String(maxsize=64)
    nombre_aides = Int()
    designation_aides = String(maxsize=64)
    salaire_aides = SubjectRelation('Prix', cardinality='??', inlined=True, composite='subject')
    tache = String(maxsize=64)
    duree = Int()
    date_travaille = Date()
    remarques = String()
    facon_et_etoffes = Boolean(default=False, required=True)

class Vendeur(EntityType): # MLVendeur
    expression = String(maxsize=255)
    vendeur = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)


class Destinataire(EntityType):
    nombre = String(maxsize=255)
    destinataire = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)

class Intervenant(EntityType): # MLIntervenant
    intervenant = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)
    indemnite = Int()
    nb_moyen_transport = Int()
    moyen_transport = String(maxsize=255)
    prix_transport = SubjectRelation('Prix', cardinality='??')
    nombre_valets = Int()
    prix_valet = SubjectRelation('Prix', cardinality='??')
    duree = Int() # XXX
    payeur = Boolean(default=False, required=True)
    pris = Boolean(default=False, required=True)
    commandement = Boolean(default=False, required=True)
    relation_de = Boolean(default=False, required=True)
    donne_par = Boolean()
    par_la_main = Boolean()
    present = Boolean()
    delivre_a = Boolean()
    fait_compte_avec  = Boolean()

class Parure(EntityType):
    type = String(maxsize=255)
    nature = String(maxsize=255)
    caracteristique = String(maxsize=255)
    composee_de = SubjectRelation('MateriauxParure', cardinality='*1', composite='subject')

class MateriauxParure(EntityType):
    type_mesure = String(maxsize=255)
    quantite = Float()
    unite = String(maxsize=255)
    provenance_mesure = String(maxsize=255)
    conversion=Float()
    materiaux_achete = Boolean(required=True, default=False)
    materiaux = SubjectRelation('Materiaux', cardinality='1*',  inlined=True)
    usage = String(maxsize=255)


class Materiaux(EntityType):
    nom = String(maxsize=255, required=True)
    type = String(vocabulary=['E', 'F', 'M', 'O', 'B', 'P'], required=True)
    famille = String(maxsize=255, default=u"laine", required=True)
    couleur = String(maxsize=255)
    carac_couleur = String(maxsize=255)
    carac_facture = String(maxsize=255)
    provenance = SubjectRelation('Lieu', cardinality='?*', inlined=True)

class Monnaie(EntityType):
    nom = String(maxsize=255, required=True)
    type = String(required=True, vocabulary=['Livre/Sous/Denier', 'Florin/Gros', 'Or'])

class Occasion(EntityType):
    type = String(maxsize=255, required=True)
    date = Date()
    remarques = String()


class Prix(EntityType):
    monnaie = SubjectRelation('Monnaie', cardinality='1*')
    livres = Int()
    sous = Int()
    deniers = Float()
    florins = Float()
    gros = Float()
    sous_florins = Int()
    denier_florins = Float()
    monnaie_or = Float()
    conversion = Float()

