from cubicweb.web.views import primary
from cubicweb.predicates import is_instance
from cubicweb.web.views.tableview import EntityTableView, RelationColRenderer

class ChangeTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Change')
    __regid__ = 'myosotis.change.attributestableview'
    columns = ('prix_depart', 'prix_converti')
    column_renderers = {'prix_depart': RelationColRenderer(),
                        'prix_converti': RelationColRenderer(),
                        }
