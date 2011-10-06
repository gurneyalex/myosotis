# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config

class Monnaie(AnyEntity):
    __regid__ = 'Monnaie'
    fetch_attrs, fetch_order = fetch_config(['nom', 'type'])

class Prix(AnyEntity):
    __regid__ = 'Prix'
    fetch_attrs, fetch_order = fetch_config(('livres', 'sous', 'deniers', 'florins', 'gros', 'sous_florins', 'denier_florins', 'monnaie'))

    def dc_title(self):
#        self.complete()
        monnaie = self.monnaie[0]
#        return u'%s %s' % (self.float_value, monnaie.nom)
        if monnaie.type == u'Livre/Sous/Denier':
            return u'%s£ %ss %sd %s' % (self.livres or 0 , self.sous or 0, self.deniers or 0, monnaie.nom)
        elif monnaie.type == u'Florin/Gros':
            return u'%sf %sg %ss %sd %s' % (self.florins or 0, self.gros or 0, self.sous_florins or 0, self.denier_florins or 0, monnaie.nom)
        else:
            return u'%s %s' % (self.monnaie_or, monnaie.nom)

    @property
    def float_value(self):
        monnaie = self.monnaie[0]
        if monnaie.type == u'Livre/Sous/Denier':
            return (self.deniers or 0) + 12*((self.sous or 0) + 20*(self.livres or 0))
        elif monnaie.type == u'Florin/Gros':
            return (self.denier_florins or 0) + 12*((self.sous_florins or 0) + 12*(self.gros or 0) + 20*(self.florins or 0))
        else:
            return self.monnaie_or or 0

