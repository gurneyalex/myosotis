#-*- coding: utf-8 -*-

from cubicweb.entities import AnyEntity, fetch_config

class Compte(AnyEntity):
    __regid__ = 'Compte'
    fetch_attrs, fetch_order = fetch_config(['debut', 'fin', 'type_compte', 'inventaire'])
    def dc_title(self):
        if self.type_compte.lower().startswith(u'hôtel'):
            prefix = u"Compte de l'"
        else:
            prefix = u"Compte de " 
        return u'%s%s %s [%s %s]' % (prefix, self.type_compte, self.inventaire, self.debut, self.fin)