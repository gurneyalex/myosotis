from cubicweb.web.views import primary
from cubicweb.selectors import implements

class ComptePrimaryView(primary.PrimaryView):
    __select__ = primary.PrimaryView.__select__ & implements('Compte')
    def render_entity_relations(self, entity):
        _ = self._cw._
        super(ComptePrimaryView, self).render_entity_relations(entity)
        subst = {'eid': entity.eid}
        rql = "Any T, P, D ORDERBY P WHERE T is Transaction, T compte C, C eid %(eid)s, T pagination P, T date D"
        rset = self._cw.execute(rql, subst)
        self.wview('editable-table', rset, 'null', title=_('Transactions'))
