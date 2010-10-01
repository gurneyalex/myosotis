from cubicweb.web.views import primary
from cubicweb.selectors import is_instance
from cubicweb.web.views.tableview import EntityAttributesTableView

class OccasionTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Occasion')
    __regid__ = 'myosotis.occasion.attributestableview'
    columns = ('type', 'date', 'lieu', 'remarques')

    def build_lieu_cell(self, entity):
        if entity.lieu:
            return entity.lieu[0].dc_title()
        else:
            return u''
