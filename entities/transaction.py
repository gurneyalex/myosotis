from cubicweb.entities import AnyEntity, fetch_config

class Transaction(AnyEntity):
    __regid__ = 'Transaction'
    def dc_title(self):
        return u'%s p. %s [%d %s]' % ( self.compte[0].inventaire, self.pagination, self.eid, self.date,)
