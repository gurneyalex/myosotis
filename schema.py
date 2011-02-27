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
from cubicweb.schema import RQLVocabularyConstraint
# TODO:
# * vérifier les cardinalites
# * renommer les relations 'personne'

class Compte(EntityType):
    type_compte = String(maxsize=255, required=True)
    inventaire = String(maxsize=255, required=True, fulltextindexed=True)
    debut = Date()
    fin = Date()
    change_str = String(maxsize=255, fulltextindexed=True) # XXX drop me?
    receveur = SubjectRelation('Personne', cardinality='**')
    base_paradox = Boolean(default=False,
                           description='vient de la base Paradox')
class Transaction(EntityType):
    date = Date()
    type_achat = String(maxsize=2) # a virer ?
    pagination = String(maxsize=255, fulltextindexed=True)
    date_ordre = Date()
    date_recette = Date()
    remarques = String(fulltextindexed=True)
    intervenants = SubjectRelation('Intervenant', composite='subject', cardinality='*1')
    destinataires = SubjectRelation('Destinataire', composite='subject', cardinality='*1')
    travaux = SubjectRelation('Travail', composite='subject', cardinality='**')
    vendeurs = SubjectRelation('Vendeur', composite='subject', cardinality='*1')
    prix_partage = Boolean(required=True, default=False)
    base_paradox = Boolean(default=False, description='vient de la base Paradox')

class compte(RelationDefinition):
    name = 'compte'
    subject = ('Transaction',)
    object = 'Compte'
    cardinality = '1*'
    composite = 'subject'


class achat(RelationDefinition):
    subject = 'Transaction'
    object = ('AchatMateriaux', 'AchatPretPorter', 'AchatFabrication')
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

class change(RelationDefinition):
    subject = ('Compte', 'Transaction')
    object = 'Change'
    cardinality = '*?'
    composite = 'subject'


class AchatFabrication(EntityType):
    date_achat = Date()
    quantite = Int()
    parure = SubjectRelation('Parure', cardinality='1*', inlined=True)
    avec_mat = SubjectRelation('FabriqueAvecMat', cardinality='*1')

class AchatMateriaux(EntityType):
    date_achat = Date()
    type_mesure = String(maxsize=255, fulltextindexed=True)
    quantite = Float()
    unite = String(maxsize=255, fulltextindexed=True)
    provenance_mesure = String(maxsize=255, fulltextindexed=True)
    conversion = Float()
    materiaux = SubjectRelation('Materiaux', cardinality='1*', inlined=True)

class AchatPretPorter(EntityType):
    date_achat = Date()
    quantite = Float()
    parure = SubjectRelation('Parure', cardinality='1*', inlined=True)

class Change(EntityType):
    #dans_compte = String(maxsize=255, fulltextindexed=True) # dummy, to help data import
    #compte = SubjectRelation('Compte', cardinality='?*')
    prix_depart = SubjectRelation('Prix', cardinality='??')
    prix_converti = SubjectRelation('Prix', cardinality='??')


class FabriqueAvecMat(EntityType):
    type_mesure = String(maxsize=255, fulltextindexed=True)
    quantite = Float()
    unite = String(maxsize=255, fulltextindexed=True)
    provenance_mesure = String(maxsize=255, fulltextindexed=True)
    conversion = Float()
    usage = String(fulltextindexed=True)
    achat_matiere = SubjectRelation('AchatMateriaux', cardinality='1*')

class Lieu(EntityType):
    ville = String(maxsize=255, required=True, fulltextindexed=True)
    region = String(maxsize=255, fulltextindexed=True)
    remarques = String(fulltextindexed=True)

class lieu(RelationDefinition):
    subject = ('Transaction', 'Occasion')
    object= 'Lieu'
    cardinality = '?*'
    inlined = True

class Personne(EntityType):
    identite = String(maxsize=255, required=True, fulltextindexed=True)
    nom = String(maxsize=64, fulltextindexed=True)
    surnom = String(maxsize=64, fulltextindexed=True)
    diminutif = String(maxsize=64, fulltextindexed=True)
    #occupation = String(maxsize=30, default='inconnue', required=True, fulltextindexed=True)
    titre = String(maxsize=128, fulltextindexed=True)
    sexe = String(vocabulary=['M', 'F'], required=True, default='M')
    ville_domicile = String(maxsize=255, fulltextindexed=True) # XXX
    ville_origine = String(maxsize=255, fulltextindexed=True) # XXX
    lieu_domicile = SubjectRelation('Lieu', cardinality='?*', inlined=True)
    lieu_origine = SubjectRelation('Lieu', cardinality='?*', inlined=True)
    remarques= String(fulltextindexed=True)
    rattachement = String(maxsize=64, fulltextindexed=True)
    #maj_occupation= Boolean(default=True)
    base_paradox = Boolean(default=False, description='vient de la base Paradox')

class Occupation(EntityType):
    libelle = String(maxsize=255, fulltextindexed=True)
    valeur = String(maxsize=255, fulltextindexed=True)
    compte = SubjectRelation('Compte', cardinality='1*')
    pagination = String(maxsize=64, fulltextindexed=True)
    rattache_a = SubjectRelation('Personne', cardinality='?*')
    occupation = String(maxsize=255, fulltextindexed=True)
    personne = SubjectRelation('Personne', cardinality = '?*', composite='subject', inlined=True)

class Travail(EntityType):
    artisan = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)
    salaire_argent = SubjectRelation('Prix', cardinality='??', inlined=True, composite='subject')
    salaire_nature_qt = Int()
    salaire_nature_obj = String(maxsize=64, fulltextindexed=True)
    nombre_aides = Int()
    designation_aides = String(maxsize=64, fulltextindexed=True)
    salaire_aides = SubjectRelation('Prix', cardinality='??', inlined=True, composite='subject')
    tache = String(maxsize=64, fulltextindexed=True)
    duree = Int()
    date_travail = Date()
    remarques = String(fulltextindexed=True)
    facon_et_etoffe = Boolean(default=False, required=True)

class Vendeur(EntityType): # MLVendeur
    expression = String(maxsize=255, fulltextindexed=True)
    vendeur = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)


class Destinataire(EntityType):
    nombre = String(maxsize=255, fulltextindexed=True)
    destinataire = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)

class Intervenant(EntityType): # MLIntervenant
    intervenant = SubjectRelation('Personne', cardinality='1*', composite='object', inlined=True)
    indemnite = Int()
    nb_moyen_transport = Int()
    moyen_transport = String(maxsize=255, fulltextindexed=True)
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
    type = String(maxsize=255, fulltextindexed=True)
    nature = String(maxsize=255, fulltextindexed=True)
    caracteristique = String(maxsize=255, fulltextindexed=True)
    composee_de = SubjectRelation('MateriauxParure', cardinality='*1', composite='subject')

class MateriauxParure(EntityType):
    type_mesure = String(maxsize=255)
    quantite = Float()
    unite = String(maxsize=255, fulltextindexed=True)
    provenance_mesure = String(maxsize=255, fulltextindexed=True)
    conversion=Float()
    materiaux_achete = Boolean(required=True, default=False)
    materiaux = SubjectRelation('Materiaux', cardinality='1*',  inlined=True)
    usage = String(maxsize=255, fulltextindexed=True)


class Materiaux(EntityType):
    nom = String(maxsize=255, required=True)
    type = String(vocabulary=['E', 'F', 'M', 'O', 'B', 'P'], required=True)
    famille = String(maxsize=255, default=u"laine", required=True, fulltextindexed=True)
    couleur = String(maxsize=255, fulltextindexed=True)
    carac_couleur = String(maxsize=255, fulltextindexed=True)
    carac_facture = String(maxsize=255, fulltextindexed=True)
    provenance = SubjectRelation('Lieu', cardinality='?*', inlined=True)

class Monnaie(EntityType):
    nom = String(maxsize=255, required=True, fulltextindexed=True)
    type = String(required=True, vocabulary=['Livre/Sous/Denier', 'Florin/Gros', 'Or'])

class Occasion(EntityType):
    type = String(maxsize=255, required=True, fulltextindexed=True)
    date = Date()
    remarques = String(fulltextindexed=True)


class Prix(EntityType):
    monnaie = SubjectRelation('Monnaie', cardinality='1*', inlined=True)
    livres = Int()
    sous = Int()
    deniers = Float()
    florins = Float()
    gros = Float()
    sous_florins = Int()
    denier_florins = Float()
    monnaie_or = Float()
    conversion = Float()

