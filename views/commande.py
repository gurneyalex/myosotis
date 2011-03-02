from cubicweb.web.views import primary
from cubicweb.selectors import is_instance
from cubicweb.web.views.tableview import EntityAttributesTableView

class CommandeTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Commande')
    __regid__ = 'myosotis.commande.attributestableview'
    columns = ('commande', 'numero', 'prix_str', 'date_ordre_str', 'transactions')

    def build_commande_cell(self, entity):
        return entity.view('incontext')

    def build_transactions_cell(self, entity):
        return u', '.join([e.view('incontext') for e in entity.transactions])
