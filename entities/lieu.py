# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode
class Lieu(AnyEntity):
    __regid__ = 'Lieu'
    fetch_attrs, cw_fetch_order = fetch_config(['ville', 'region'])
    def dc_title(self):
        return u'%s' % (self.ville)
    def dc_long_title(self):
        #self.complete()
        return u'%s (%s)' % (self.ville, self.region)
