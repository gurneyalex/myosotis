# -*- coding: utf-8 -*-
from cubicweb.web.facet import RelationFacet, RQLPathFacet, AttributeFacet, DateRangeFacet
from cubicweb.predicates import is_instance

class CompteType(AttributeFacet):
    __regid__ = 'compte-type'
    __select__ = AttributeFacet.__select__ & is_instance('Compte')
    rtype = 'type_compte'
    order = 1

class CompteStart(DateRangeFacet):
    __regid__ = 'compte-start'
    __select__ = AttributeFacet.__select__ & is_instance('Compte')
    rtype = 'debut'
    order = 2
class CompteEnd(DateRangeFacet):
    __regid__ = 'compte-end'
    __select__ = AttributeFacet.__select__ & is_instance('Compte')
    rtype = 'fin'
    order = 3 

class MateriauxType(AttributeFacet):
    __regid__ = 'materiaux-type'
    __select__ = AttributeFacet.__select__ & is_instance('Materiaux')
    rtype = 'type'

class MateriauxFamille(AttributeFacet):
    __regid__ = 'materiaux-famille'
    __select__ = AttributeFacet.__select__ & is_instance('Materiaux')
    rtype = 'famille'

class ParureType(AttributeFacet):
    __regid__ = 'parure-type'
    __select__ = AttributeFacet.__select__ & is_instance('Parure')
    rtype = 'type'
    order=1

class ParureNature(AttributeFacet):
    __regid__ = 'parure-nature'
    __select__ = AttributeFacet.__select__ & is_instance('Parure')
    rtype = 'nature'
    order=2

class PersonneSexe(RQLPathFacet):
    __regid__ = 'personne-sexe'
    title = 'sexe'
    __select__  = RQLPathFacet.__select__ & is_instance('Personne')
    path = ['X sexe N']
    filter_variable = 'N'
class PersonneTitre(RQLPathFacet):
    __regid__ = 'personne-titre'
    title = 'titre'
    __select__  = RQLPathFacet.__select__ & is_instance('Personne')
    path = ['X titre N']
    filter_variable = 'N'
## class PersonneOccupationIdentite(RQLPathFacet):
##     __regid__ = 'personne-occupation-identite'
##     title = 'identite'
##     __select__  = RQLPathFacet.__select__ & is_instance('Personne')
##     path = ['O personne X', 'O libelle \'identité\'', 'O valeur N']
##     filter_variable = 'N'
## class PersonneOccupation(RQLPathFacet):
##     __regid__ = 'personne-occupation'
##     title = 'occupation'
##     __select__  = RQLPathFacet.__select__ & is_instance('Personne')
##     path = ['O personne X', 'O libelle "occupation"', 'O valeur N']
##     filter_variable = 'N'

class TransactionInCompte(RelationFacet):
    __regid__ = 'transaction-compte'
    target_type = 'Compte'
    role = 'subject'
    rtype = 'compte'
    label_vid = 'textincontext'
    __select__  = RelationFacet.__select__ & is_instance('Transaction')
    order = 1


class TransactionOccasion(RelationFacet):
    __regid__ = 'transaction-occasion'
    target_type = 'Occasion'
    role = 'subject'
    rtype = 'occasion'
    label_vid = 'textincontext'
    no_relation = True
    order = 2

class TransactionDestinataireSexe(RQLPathFacet):
    __regid__ = 'transaction-dest-sexe'
    title = 'sexe destinataire'
    __select__  = RQLPathFacet.__select__ & is_instance('Transaction')
    path = ['X destinataires D', 'D destinataire P', 'P sexe N']
    filter_variable = 'N'
    order = 3

class TransactionDestinataire(RQLPathFacet):
    __regid__ = 'transaction-dest'
    title = 'destinataire'
    __select__  = RQLPathFacet.__select__ & is_instance('Transaction')
    path = ['X destinataires D', 'D destinataire P', 'P identite I']
    filter_variable = 'P'
    label_variable = 'I'
    order = 4

class TransactionDestinataireTitre(RQLPathFacet):
    __regid__ = 'transaction-dest-titre'
    title = 'sexe destinataire'
    __select__  = RQLPathFacet.__select__ & is_instance('Transaction')
    path = ['X destinataires D', 'D destinataire P', 'P titre N']
    filter_variable = 'N'
    order = 5

class PrixSource(AttributeFacet):
    __regid__ = 'prix-source'
    __select__ = AttributeFacet.__select__ & is_instance('Prix')
    rtype = 'source'

class PrixTypeMonnaie(RQLPathFacet):
    __regid__ = 'prix-monnaie-type'
    title = 'Type monnaie'
    __select__  = RQLPathFacet.__select__ & is_instance('Prix')
    path = ['X monnaie M', 'M type T']
    filter_variable = 'T'
    order = 5

class PrixMonnaie(RelationFacet):
    __regid__ = 'prix-monnaie'
    target_type = 'Monnaie'
    role = 'subject'
    rtype = 'monnaie'
    label_vid = 'textincontext'
    __select__  = RelationFacet.__select__ & is_instance('Prix')
    order = 1

class TypeMonnaie(AttributeFacet):
    __regid__ = 'monnaie-type'
    __select__ = AttributeFacet.__select__ & is_instance('Monnaie')
    rtype = 'type'

