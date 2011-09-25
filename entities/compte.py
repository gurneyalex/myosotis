#-*- coding: utf-8 -*-
from logilab.mtconverter import xml_escape
from cubicweb.entities import AnyEntity, fetch_config

class Compte(AnyEntity):
    __regid__ = 'Compte'
    fetch_attrs, fetch_order = fetch_config(['debut', 'fin', 'type_compte', 'inventaire'])
    def dc_title(self):
        return self.inventaire
    
    def dc_long_title(self):
        type_compte = self.type_compte + u' '
        if self.inventaire.lower().startswith('compte'):
            prefix = ''
            type_compte = ''
        elif self.type_compte.lower().startswith(u'hôtel'):
            prefix = u"Compte de l'"
        else:
            prefix = u"Compte de " 
        return u'%s%s%s [%s %s]' % (prefix, type_compte, self.inventaire, self.debut, self.fin)

    def dc_description(self, format='text/plain'):
        title = self.dc_long_title()
        rql = 'Any C, COUNT(CDE) GROUPBY C WHERE CDE is Commande, CDE compte C, C eid %(eid)s'
        rset = self._cw.execute(rql, {'eid': self.eid})
        if not rset:
            nb_cdes = 0
        else:
            nb_cdes = rset[0][1]
        rql = 'Any C, COUNT(CDE) GROUPBY C WHERE CDE is Transaction, CDE compte C, C eid %(eid)s'
        rset = self._cw.execute(rql, {'eid': self.eid})
        if not rset:
            nb_trans = 0
        else:
            nb_trans = rset[0][1]
        description = '%d commandes, %d transactions' % (nb_cdes, nb_trans)
        if format == 'text/plain':
            return u'\n\n'.join([title,
                                description])
        elif format == 'text/html':
            return u'<h2>%s</h2><p>%s</p>' % (xml_escape(title), xml_escape(description))
        return u''
