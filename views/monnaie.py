# -*- coding: utf-8
from cubicweb.view import EntityView
from cubicweb.web.views import tabs, primary, basecontrollers, baseviews
from cubicweb.web import uicfg, stdmsgs, component, box, facet
from cubicweb.selectors import is_instance, one_line_rset
from cubicweb.web import action, component
from logilab.common.decorators import monkeypatch
from logilab.mtconverter import xml_escape

_ = unicode
class MonnaiePrimaryView(tabs.TabbedPrimaryView):
    __select__ = tabs.PrimaryTab.__select__ & is_instance('Monnaie')
    tabs = [_('tab_monnaie'),
            _('tab_changes'),
            ]
    default_tab='tab_monnaie'

class MonnaieTab(tabs.PrimaryTab):
    __regid__ = 'tab_monnaie'
    __select__ = one_line_rset() & is_instance('Monnaie')
    title = None
    

class TabChanges(EntityView):
    __regid__ = 'tab_changes'
    __select__ = one_line_rset & is_instance('Monnaie')
    def entity_call(self, entity):
        rql = ('Any C WHERE C is Change, '
               'EXISTS (C prix_depart P1, P1 monnaie M1, M1 eid %(eid)s) '
               'OR '
               'EXISTS (C prix_converti P2, P2 monnaie M2, M2 eid %(eid)s)')
        rset = self._cw.execute(rql, {'eid': entity.eid})
        changed = {}
        for change in rset.entities():
            m1 = change.prix_depart[0].monnaie[0]
            m2 = change.prix_converti[0].monnaie[0]
            if m2.eid == entity.eid:
                m1, m2 = m2, m1
            changed.setdefault((m2.nom, m2.eid), []).append(change)
        import pprint
        #pprint.pprint(changed)
        all_values = []
        for (name, other_monnaie_eid), changes in sorted(changed.items()):
            monnaie = self._cw.entity_from_eid(other_monnaie_eid)
            all_values.append(("<h2>%s</h2>" % monnaie.view('incontext'), '', ''))
            values = []
            for change in changes:
                try:
                    val = u'%.4f' % (change.change(1, other_monnaie_eid)[0],)
                except AssertionError:
                    val = u'invalid'
                values.append((change.date, val,
                               change.view('outofcontext2')))

            values.sort()
            all_values += values
        self.wview('pyvaltable', None, 'null', pyvalue=all_values)

# TODO
# class ChangesPlotView(baseviews.AnyRsetView):
#     __regid__ = 'plot'
#     title = _('generic plot')
#     __select__ = multi_columns_rset() & all_columns_are_numbers()
#     timemode = False
#     paginable = False

#     def call(self, width=500, height=400):
#         # prepare data
#         rqlst = self.cw_rset.syntax_tree()
#         # XXX try to make it work with unions
#         varnames = [var.name for var in rqlst.children[0].get_selected_variables()][1:]
#         abscissa = [row[0] for row in self.cw_rset]
#         plots = []
#         nbcols = len(self.cw_rset.rows[0])
#         for col in xrange(1, nbcols):
#             data = [row[col] for row in self.cw_rset]
#             plots.append(filterout_nulls(abscissa, data))
#         plotwidget = FlotPlotWidget(varnames, plots, timemode=self.timemode)
#         plotwidget.render(self._cw, width, height, w=self.w)


class ChangeOOCView(baseviews.OutOfContextView):
    __regid__ = 'outofcontext2'
    __select__ = baseviews.OutOfContextView.__select__ & is_instance('Change')
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        desc = entity.dc_description()
        self.w(u'<a href="%s" title="%s">' % (
            xml_escape(entity.absolute_url()), xml_escape(desc)))
        self.w(xml_escape(self._cw.view('textoutofcontext2', self.cw_rset,
                                        row=row, col=col)))
        self.w(u'</a>')

class ChangeOOCTView(baseviews.OutOfContextTextView):
    """:__regid__: *textoutofcontext*

    Similar to the `text` view, but called when an entity is considered out of
    context (see description of outofcontext HTML view for more information on
    this). By default it displays what's returned by the `dc_long_title()`
    method of the entity.
    """
    __regid__ = 'textoutofcontext2'
    __select__ = baseviews.OutOfContextTextView.__select__ & is_instance('Change')
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(entity.dc_long_title2())
