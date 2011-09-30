from logilab.mtconverter import xml_escape

from cubicweb.view import EntityView
from cubicweb.web.views import primary
from cubicweb.web.views import baseviews
from cubicweb.selectors import is_instance, rql_condition
from cubicweb.web.views.tableview import EntityAttributesTableView
from cubicweb.web.views.tabs import TabbedPrimaryView, PrimaryTab

_ = unicode
class ComptePrimaryView(TabbedPrimaryView):
    tabs = ['main_tab', 'commandes_tab', 'transactions_tab', 'occasions_tab', 'changes_tab']
    __select__ = is_instance('Compte')

class CompteMainTab(PrimaryTab):
    __select__ = primary.PrimaryView.__select__ & is_instance('Compte')
    title = _('Compte')

class CompteTransactionTab(EntityView):
    __select__ = is_instance('Compte') & rql_condition('T compte X, T is Transaction')
    __regid__ = _('transactions_tab')
    title = _('Transactions')
    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        rql = entity.cw_related_rql('compte', 'object', ('Transaction',),)
        rset = self._cw.execute(rql, {'x': entity.eid})
        self.wview('myosotis.transaction.attributestableview', rset)

class CompteCommandesTab(EntityView):
    __select__ = is_instance('Compte') & rql_condition('T compte X, T is Commande')
    __regid__ = _('commandes_tab')
    title = _('Commandes')
    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        rset = self._cw.execute('Any T ORDERBY P where T is Commande, T numero P,  T compte C, C eid %(eid)s', {'eid': entity.eid})
        self.wview('myosotis.commande.attributestableview', rset)

class CompteChangeTab(EntityView):
    __select__ = is_instance('Compte') & rql_condition('C is Change, X change C')
    __regid__ = _('changes_tab')
    title = _('Changes')
    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        rset = self._cw.execute('Any T where T is Change, C change T, C eid %(eid)s', {'eid': entity.eid})
        print len(rset)
        self.wview('myosotis.change.attributestableview', rset)

class CompteOccasionTab(EntityView):
    __select__ = is_instance('Compte') & rql_condition('T compte X, T occasion O')
    __regid__ = _('occasions_tab')
    title = _('Occasion')
    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        rset = self._cw.execute('Any O where O is Occasion, EXISTS (T occasion O, T compte C, C eid %(eid)s)', {'eid': entity.eid})
        self.wview('myosotis.occasion.attributestableview', rset)


class CompteOutOfContextView(baseviews.OutOfContextView):
    __select__ = is_instance('Compte')
    def cell_call(self, row, col):
        super(CompteOutOfContextView, self).cell_call(row, col)
        entity = self.cw_rset.get_entity(row, col)
        rset = self._cw.execute('Any Count(T) where T is Transaction, T compte C, C eid %(eid)s', {'eid': entity.eid})
        length = rset[0][0]

        self.w(u' (%d)' % length)

from cubicweb.view import EntityAdapter
class CompteICalendarableAdapter(EntityAdapter):
    __regid__ = 'ICalendarable'
    __select__ = is_instance('Compte')

    @property
    def start(self):
        return self.entity.debut

    @property
    def stop(self):
        return self.entity.fin

## class CompteTimeline(timeline.TimelineView):
##     __regid__ = 'compte.timeline'
##     __select__ = is_instance('Compte')
##     jsfiles = timeline.TimelineView.jsfiles + ('cubicweb.myosotis.js',)

##     def render_url(self, loadurl, tlunit=None): # copied to avoid loadtype=auto
##         tlunit = tlunit or self._cw.form.get('tlunit')
##         self._cw.add_js(self.jsfiles)
##         self._cw.add_css('timeline-bundle.css')
##         if tlunit:
##             additional = u' cubicweb:tlunit="%s"' % tlunit
##         else:
##             additional = u''
##         self.w(u'<div class="widget" cubicweb:wdgtype="%s" '
##                u'cubicweb:loadurl="%s" %s >' %
##                (self.widget_class, xml_escape(loadurl),
##                 additional))
##         self.w(u'</div>')

##     def call(self, tlunit=None):
##         super(CompteTimeline, self).call(tlunit)
##         min_start_date = min(entity.debut for entity in self.cw_rset.entities())
##         year, month, day = min_start_date.year, min_start_date.month-1, min_start_date.day
##         self.w(u'<script type="text/javascript">jQuery(document).ready(function(){setMinVisibleDate(new Date(%d, %d, %d));});</script>' % (year, month, day))


