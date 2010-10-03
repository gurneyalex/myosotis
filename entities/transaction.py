# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode
class Transaction(AnyEntity):
    __regid__ = 'Transaction'
    fetch_attrs, fetch_order = fetch_config(('pagination','date', 'date_ordre', 'date_recette'))
    def dc_title(self):
        if self.date is None:
            date = _('pas de date')
        else:
            date = self.date
        return u'%s p. %s [n° %d, %s]' % ( self.compte[0].inventaire, self.pagination, self.eid, date,)
