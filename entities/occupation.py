from cubicweb.entities import AnyEntity, fetch_config
_ = unicode
class Occupation(AnyEntity):
    __regid__ = 'Occupation'
    def dc_title(self):
        return u'%s : %s' % (self.libelle or '?' , self.valeur or '')
