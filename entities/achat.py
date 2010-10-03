# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode


class AchatFabrication(AnyEntity):
    __regid__ = 'AchatFabrication'
    def dc_title(self):
        quantite = self.quantite or 1
        parure = self.parure[0].dc_title()
        return u'Fabrication %d %s' % (quantite, parure)

class AchatPretPorter(AnyEntity):
    __regid__ = 'AchatPretPorter'
    def dc_title(self):
        quantite = self.quantite or 1
        parure = self.parure[0].dc_title()
        return u'Prêt à Porter %d %s' % (quantite, parure)

class AchatMateriaux(AnyEntity):
    __regid__ = 'AchatMateriaux'
    def dc_title(self):
        if self.quantite is not None:
            unite = self.unite
            quantite = self.quantite
            if self.provenance_mesure:
                unite = '%s de %s' % (unite, self.provenance_mesure)
        else:
            unite = u''
            quantite = u''
        return 'Achat %s %s %s' % (quantite, unite, self.materiaux[0].dc_title())

class FabriqueAvecMat(AnyEntity):
    __regid__ = 'FabriqueAvecMat'
    def dc_title(self):
        return u'fabrique avec %s' % self.achat_matiere[0].dc_title()

class MateriauxParure(AnyEntity):
    __regid__ = 'MateriauxParure'
    fetch_attrs, fetch_order = fetch_config(['usage', 'provenance', 'type_mesure', 'quantite', 'unite','conversion', 'materiaux_achete' , ])
    def dc_title(self):
        return self.materiaux[0].dc_title()

class Parure(AnyEntity):
    __regid__ = 'Parure'
    fetch_attrs, fetch_order = fetch_config(['type', 'nature', 'caracteristique'])
    
    def dc_title(self):
        return '%s %s' % (self.nature, self.caracteristique)

class Materiaux(AnyEntity):
    __regid__ = 'Materiaux'
    fetch_attrs, _ = fetch_config(['type', 'famille', 'nom', 'couleur', 'carac_couleur', 'carac_facture'])
    def dc_title(self):
        if self.provenance:
            prov = u' de %s' % self.provenance[0].dc_title()
        else:
            prov = '' 
        title = u'[%s-%s] %s %s%s' % (self.type, self.famille,
                                      self.nom, self.couleur,
                                      prov)
        return title


    @classmethod
    def fetch_order(cls, attr, var):
        if attr in ('type', 'famille', 'nom', 'couleur'):
            return '%s ASC' % var
        return None
