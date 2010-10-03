# -*- coding: utf-8 -*-
from cubicweb.view import EntityView
from cubicweb.web.views import baseviews
from cubicweb.selectors import is_instance
from cubicweb.web.views import primary
from cubicweb.web.box import EntityBoxTemplate
from cubicweb.web.htmlwidgets import SideBoxWidget

class ParureOutOfContextView(baseviews.OutOfContextView):
    __select__ = is_instance('Parure')
    def cell_call(self, row, col):
        super(ParureOutOfContextView, self).cell_call(row, col)
        entity = self.cw_rset.get_entity(row, col)
        rset = self._cw.execute('Any Count(M) where P composee_de M, P eid %(eid)s', {'eid': entity.eid})
        if entity.reverse_parure:
            achat = entity.reverse_parure[0]
            if achat.__regid__ == 'AchatFabrication':
                orig = u'[F]'
            else:
                orig = u'[P]'
        else:
            orig = u'[?]'
                
    
        length = rset[0][0]
        rset2 = self._cw.execute('Any Count(M) where A parure P, A avec_mat M, P eid %(eid)s', {'eid': entity.eid})
        self.w(u' %s(%d)' % (orig, rset[0][0]+ rset2[0][0]))

class ParureLinkBox(EntityBoxTemplate):
    __regid__ = 'myosotis.similar_parures'
    __select__ = EntityBoxTemplate.__select__ & is_instance('Parure')
    title = _('Parures similaires')
    context="incontext"
    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        box = SideBoxWidget(self._cw._(self.title), self.__regid__)
        for label, rql in self._get_links(entity):
            box.append(self.mk_action(label,
                                      self._cw.build_url(rql=rql,
                                                         __force_display=1,
                                                         vid='myosotis.parure_summary')))
        box.render(self.w)

    def _get_links(self, entity):
        url = self._cw.build_url
        same_type = 'Any X WHERE X is Parure, X type T, P type T, P eid %s' % entity.eid
        same_nature = 'Any X WHERE X is Parure, X nature N, P nature N, P eid %s' % entity.eid
        same_carac = 'Any X WHERE X is Parure, X nature N, X caracteristique C, P nature N, P caracteristique C, P eid %s' % (entity.eid)
        links = [(_('Same type Parures'), same_type),
                 (_('Same nature Parures'), same_nature),
                 (_('Same caracteristique Parures'), same_carac)
                 ]
        return links


class MultiParureSummaryView(EntityView):
    __regid__ = 'myosotis.parure_summary'
    __select__ = is_instance('Parure')

    def call(self):
        parures = {}
        for p in self.cw_rset.entities():
            parures.setdefault(p.nature, []).append(p)
        for nature in parures:
            self.w(u'<h2>%s</h2>' % nature)
            self.w(u'<ul>')
            for p in parures[nature]:
                self.w(u'<li>')
                self.w(p.view('listitem'))
                self.w(u'</li>')
            
            self.w(u'</ul>')
                   
