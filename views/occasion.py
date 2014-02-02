from cubicweb.web.views import primary
from cubicweb.predicates import is_instance
from cubicweb.web.views.tableview import EntityTableView, MainEntityColRenderer, RelationColRenderer, RelatedEntityColRenderer

def get_lieu(e):
    return e.lieu and e.lieu[0] or None

class OccasionTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Occasion')
    __regid__ = 'myosotis.occasion.attributestableview'
    columns = ('type', 'date', 'lieu', 'remarques')
    column_renderers = {'lieu': RelatedEntityColRenderer(vid='outofcontext',
                                                        getrelated=get_lieu),
                       'type': MainEntityColRenderer(vid='incontext'),
                       }
