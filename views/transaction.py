from cubicweb.web.views import primary
from cubicweb.selectors import is_instance
from cubicweb.web.views.tableview import EntityAttributesTableView

class TransactionPrimaryView(primary.PrimaryView):
    __select__ = primary.PrimaryView.__select__ & is_instance('Transaction')
    def render_entity_relations(self, entity):
        _ = self._cw._
        super(TransactionPrimaryView, self).render_entity_relations(entity)
        ## subst = {'eid': entity.eid}
        ## rql = "Any T, P, D ORDERBY P WHERE T is Transaction, T compte C, C eid %(eid)s, T pagination P, T date D"
        ## rset = self._cw.execute(rql, subst)
        ## self.wview('editable-table', rset, 'null', title=_('Transactions'))

class TransactionTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Transaction')
    __regid__ = 'myosotis.transaction.attributestableview'
    columns = ('transaction', 'date', 'pagination', 'date_ordre', 'date_recette', )

    def build_transaction_cell(self, entity):
        return entity.dc_title()
