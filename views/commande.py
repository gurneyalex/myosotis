from cubicweb.web.views import primary
from cubicweb.predicates import is_instance
from cubicweb.web.views.tableview import EntityTableView, MainEntityColRenderer, RelationColRenderer

class CommandeTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Commande')
    __regid__ = 'myosotis.commande.attributestableview'
    columns = ('commande', 'numero', 'prix_str', 'date_ordre_str', 'transactions')
    column_renderers = {'transactions': RelationColRenderer(subvid='incontext'),
                        'commande': MainEntityColRenderer(),
                        }

    def build_transactions_cell(self, entity):
        return u', '.join([e.view('incontext') for e in entity.transactions])
