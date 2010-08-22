from cubicweb.entities import AnyEntity, fetch_config

class Occupation(AnyEntity):
    __regid__ = 'Occupation'
    def dc_title(self):
        return '%s : %s' % (self.libelle, self.valeur)
