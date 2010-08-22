# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config

class Prix(AnyEntity):
    __regid__ = 'Prix'
    def dc_title(self):
        monnaie = self.monnaie[0]
        if monnaie.type == u'Livre/Sous/Denier':
            return u'%d£ %ds %.2fd %s' % (self.livres or 0 , self.sous or 0, self.deniers or 0, monnaie.nom)
        elif monnaie.type == u'Florin/Gros':
            return u'%.2ff %.2fg %ds %.2fd %s' % (self.florins or 0, self.gros or 0, self.sous_florins or 0, self.denier_florins or 0, monnaie.nom)
        else:
            return u'%.2f %s' % (self.monnaie_or, monnaie.nom)
