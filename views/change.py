from cubicweb.web.views import primary
from cubicweb.selectors import is_instance
from cubicweb.web.views.tableview import EntityAttributesTableView

class ChangeTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Change')
    __regid__ = 'myosotis.change.attributestableview'
    columns = ('prix_depart', 'prix_converti', 'ratio')

    def build_prix_depart_cell(self, entity):
        return entity.prix_depart[0].dc_title()
    def build_prix_converti_cell(self, entity):
        return entity.prix_converti[0].dc_title()
    def build_ratio_cell(self, entity):
        return entity.ratio, 1/entity.ratio
