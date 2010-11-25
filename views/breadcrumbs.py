from cubicweb.web.views.ibreadcrumbs import IBreadCrumbsAdapter
from cubicweb.selectors import is_instance, has_related_entities

class TransactionBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Transaction') & has_related_entities('compte')
    def parent_entity(self):
        return self.entity.compte[0]


class AchatBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('AchatMateriaux', 'AchatPretPorter', 'AchatFabrication') & \
                 has_related_entities('achat', 'object')
    def parent_entity(self):
        return self.entity.reverse_achat[0]

class OccasionBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Occasion') & has_related_entities('occasion', 'object')
    def parent_entity(self):
        return self.entity.reverse_occasion[0]

    
# XXX todo: Parure, Materiaux

class OccupationBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Occupation') & has_related_entities('personne')
    def parent_entity(self):
        return self.entity.personne[0]

class TravailBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ =  is_instance('Travail') & has_related_entities('travaux', 'object')
    def parent_entity(self):
        if self.entity.reverse_travaux:
            return self.entity.reverse_travaux[0]

class VendeurBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ =  is_instance('Vendeur') & has_related_entities('vendeurs', 'object')
    def parent_entity(self):
        return self.entity.reverse_vendeurs[0]

class DestinataireBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ =  is_instance('Destinataire') & has_related_entities('destinataires', 'object')
    def parent_entity(self):
        return self.entity.reverse_destinataires[0]

class IntervenantBreadCrumbAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('Intervenant') & has_related_entities('intervenants', 'object')
    def parent_entity(self):
        return self.entity.reverse_intervenants[0]

class FabriqueAvecMatBCAdapter(IBreadCrumbsAdapter):
    __select__ = is_instance('FabriqueAvecMat') & has_related_entities('avec_mat', 'object')
    def parent_entity(self):
        return self.entity.reverse_avec_mat[0]
