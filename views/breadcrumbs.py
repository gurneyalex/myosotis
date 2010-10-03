from cubicweb.web.views.ibreadcrumbs import IBreadCrumbsAdapter
from cubicweb.selectors import is_instance

class TransactionBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Transaction')
    def parent_entity(self):
        return self.entity.compte[0]


class AchatBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('AchatMateriaux', 'AchatPretPorter', 'AchatFabrication')
    def parent_entity(self):
        return self.entity.reverse_achat[0]

class OccasionBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Occasion')
    def parent_entity(self):
        return self.entity.reverse_occasion[0]

    
# XXX todo: Parure, Materiaux

class OccupationBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Occupation')
    def parent_entity(self):
        return self.entity.personne[0]

class TravailBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ =  is_instance('Travail')
    def parent_entity(self):
        return self.entity.reverse_travaux[0]

class VendeurBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ =  is_instance('Vendeur')
    def parent_entity(self):
        return self.entity.reverse_vendeurs[0]

class DestinataireBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ =  is_instance('Destinataire')
    def parent_entity(self):
        return self.entity.reverse_destinataires[0]

class IntervenantBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Intervenant')
    def parent_entity(self):
        return self.entity.reverse_intervenants[0]

class FabriqueAvecMatBCAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('FabriqueAvecMat')
    def parent_entity(self):
        return self.entity.reverse_avec_mat[0]
