from logilab.mtconverter import xml_escape
from cubicweb.view import EntityView
from cubicweb.web.views.tableview import EntityTableView, MainEntityColRenderer, RelationColRenderer, RelatedEntityColRenderer
from cubicweb.predicates import is_instance

class MonnaieTypeView(EntityView):
    __regid__ = 'type_monnaie'
    __select__ = is_instance('Monnaie')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(xml_escape(entity.type))

class PrixTableView(EntityTableView):
    __regid__ = 'table'
    __select__ = is_instance('Prix')
    columns = ('type_monnaie', 'monnaie', 'livres', 'sous', 'deniers', 'florins', 'gros', 'sous_florins', 'denier_florins')
    column_renderers = {'type_monnaie': RelatedEntityColRenderer(getrelated=lambda e: e.monnaie and e.monnaie[0] or None,
                                                                 sortfunc=lambda e: e.type,
                                                                 vid='type_monnaie'),
                        'monnaie': RelatedEntityColRenderer(getrelated=lambda e: e.monnaie and e.monnaie[0] or None,
                                                            sortfunc=lambda e: e.nom),
                        }
    def call(self, *args, **kwargs):
        req = self._cw
        ## req.add_js('jquery.tablesorter.js')
        req.add_css(('cubicweb.tablesorter.css', 'cubicweb.tableview.css'))
        return super(PrixTableView, self).call(*args, **kwargs)

