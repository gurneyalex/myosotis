# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode

class Personne(AnyEntity):
    __regid__ = 'Personne'
    fetch_attrs, fetch_order = fetch_config(['identite', 'sexe', 'nom'])

class Destinataire(AnyEntity):
    __regid__ = 'Destinataire'
    fetch_attrs = ['nombre', 'destinataire']
    def dc_title(self):
        if self.nombre != u'1':
            return _('%s %s') % (self.nombre, self.destinataire[0].dc_title())
        else:
            return self.destinataire[0].dc_title()
