from cubicweb.web.views import primary
from cubicweb.view import EntityView
from cubicweb.predicates import is_instance
from cubicweb.web.views.tableview import EntityTableView, RelationColRenderer, MainEntityColRenderer

class ChangeTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Change')
    __regid__ = 'myosotis.change.attributestableview'
    columns = ('date', 'ratio', 'prix_depart', 'prix_converti')
    column_renderers = {'prix_depart': RelationColRenderer(),
                        'prix_converti': RelationColRenderer(),
                        'date': MainEntityColRenderer(vid='change_date_view'),
                        'ratio': MainEntityColRenderer(vid='change_ratio_view'),
                        
                        }

class ChangeRatioView(EntityView):
    __regid__ = 'change_ratio_view'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        ratio = entity.ratio
        self.w(u'%s' % ratio)


class ChangeDateView(EntityView):
    __regid__ = 'change_date_view'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        date = entity.date
        self.w(u'%s' % date)

