# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode
class Lieu(AnyEntity):
    __regid__ = 'Lieu'
    def dc_title(self):
        return u'%s, %s' % (self.ville, self.region)