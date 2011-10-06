# -*- coding: utf-8 -*-
from cubicweb.web.facet import RelationFacet, RQLPathFacet
from cubicweb.selectors import is_instance

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
