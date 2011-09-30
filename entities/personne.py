# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode



class Destinataire(AnyEntity):
    __regid__ = 'Destinataire'
    def dc_title(self):
        if self.nombre != u'1':
            return _('%s %s') % (self.nombre, self.destinataire[0].dc_title())
        else:
            return self.destinataire[0].dc_title()
