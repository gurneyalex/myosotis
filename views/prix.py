from cubicweb.web.views.tableview import EntityAttributesTableView
from cubicweb.selectors import is_instance

class PrixTableView(EntityAttributesTableView):
    __regid__ = 'table'
    __select__ = is_instance('Prix')
    columns = ('type_monnaie', 'monnaie', 'livres', 'sous', 'deniers', 'florins', 'gros', 'sous_florins', 'denier_florins')

    def call(self, *args, **kwargs):
        req = self._cw
        req.add_js('jquery.tablesorter.js')
        req.add_css(('cubicweb.tablesorter.css', 'cubicweb.tableview.css'))
        return super(PrixTableView, self).call(*args, **kwargs)

    def build_type_monnaie_cell(self, entity):
        return entity.monnaie[0].type

    def build_monnaie_cell(self, entity):
        return entity.monnaie[0].nom
