from cubicweb.selectors import is_instance
from cubicweb.web.box import EntityBoxTemplate
from cubicweb.web.htmlwidgets import SideBoxWidget
_ = unicode

class MateriauxLinkBox(EntityBoxTemplate):
    __regid__ = 'myosotis.similar_materiaux'
    __select__ = EntityBoxTemplate.__select__ & is_instance('Materiaux')
    title = _('Materiaux similaires')
    context="incontext"
    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        box = SideBoxWidget(self._cw._(self.title), self.__regid__)
        for label, rql in self._get_links(entity):
            box.append(self.mk_action(label,
                                      self._cw.build_url(rql=rql,
                                                         __force_display=1,
                                                         vid='list')))
        box.render(self.w)

    def _get_links(self, entity):
        url = self._cw.build_url
        same_type = 'Any X WHERE X is Materiaux, X type T, P type T, P eid %s' % entity.eid
        same_nature = 'Any X WHERE X is Materiaux, X nom N, P nom N, P eid %s' % entity.eid
        same_couleur = 'Any X WHERE X is Materiaux, X nom C, X couleur C, P nom N, P couleur C, P eid %s' % (entity.eid)
        same_provenance = 'Any X WHERE X is Materiaux, X provenance Y, P provenance Y, P eid %s' % (entity.eid)
        links = [(_('Same type Materiaux'), same_type),
                 (_('Same nature Materiaux'), same_nature),
                 (_('Same couleur Materiaux'), same_couleur),
                 (_('Same provenance Materiaux'), same_provenance),
                 ]
        return links
