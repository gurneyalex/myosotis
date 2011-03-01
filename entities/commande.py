# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode
class Commande(AnyEntity):
    __regid__ = 'Commande'
    fetch_attrs, fetch_order = fetch_config(('numero', 'prix_str', 'date_ordre_str'))
    def dc_title(self):
        return u'item %d' % self.numero
