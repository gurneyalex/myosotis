

from cubicweb.entities import AnyEntity, fetch_config

class Compte(AnyEntity):
    __regid__ = 'Compte'
    fetch_attrs, fetch_order = fetch_config(['debut', 'fin', 'type_compte', 'inventaire'])
    def dc_title(self):
        return self.inventaire
