# -*- coding: utf-8
from cubicweb.view import EntityView
from cubicweb.web.views import uicfg, tabs, primary, basecontrollers, ajaxcontroller
from cubicweb.web import stdmsgs, component, box, facet
from cubicweb.predicates import is_instance, one_line_rset
from cubicweb.web import action, component
from logilab.common.decorators import monkeypatch
from logilab.mtconverter import xml_escape

_ = unicode
class PersonnePrimaryView(tabs.TabbedPrimaryView):
    __select__ = tabs.PrimaryTab.__select__ & is_instance('Personne')
    tabs = [_('tab_personne'),
            _('tab_personne_intervention'),
            _('tab_personne_artisan'),
            _('tab_personne_destinataire'),
            _('tab_personne_vendeur'),
            _('tab_personne_rattachement'),
            _('personne_relations'),
            _('tab_personne_codest'),
            ]
    default_tab='tab_personne'

class PersonneTab(tabs.PrimaryTab):
    __regid__ = 'tab_personne'
    __select__ = one_line_rset() & is_instance('Personne')
    title = None
    def render_entity_relations(self, entity):
        _ = self._cw._
        super(PersonneTab, self).render_entity_relations(entity)
        subst = {'eid': entity.eid}
        rql = ('Any X, L, V, R, O, C, F ORDERBY C WHERE '
               'X is Occupation, '
               'X personne P, '
               'P eid %(eid)s, '
               'X compte C?, '
               'X pagination F, '
               'X libelle L, '
               'X valeur V, '
               'X rattache_a R?, '
               'X occupation O'
               )
        rset = self._cw.execute(rql, subst)
        self.wview('editable-table', rset, 'null', title=_('Occupations'),
                   headers=[_('Occupation'), _('libelle'), _('valeur'), _('rattache_a'),
                            _('occupation'), _('compte'), _('pagination')])
        if len(rset) > 1:
            self.w('<p>voir <a href="%s"> dans le temps</a></p>' % (entity.absolute_url(vid='occupation_timeline')))

class PersonneOccupationTimeline(EntityView):
    __regid__ = 'occupation_timeline'
    __select__ = is_instance('Personne')
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        self.wview('myosotis.timeline', self._cw.execute('Any X where X is Occupation, X personne P, P eid %(eid)s', subst))

class TabPersonneCodest(EntityView):
    __regid__ = 'tab_personne_codest'
    __select__ = one_line_rset & is_instance('Personne')

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        rql = 'Any P, COUNT(T) GROUPBY P ORDERBY 2 DESC WHERE T destinataires D, D destinataire P1, T destinataires D2, D2 destinataire P, NOT P identity P1, P1 eid %(eid)s'
        rset = self._cw.execute(rql, {'eid': entity.eid})
        self.wview('table', rset, 'null')


class TabPersonneIntervention(tabs.EntityRelationView):
    __regid__ = 'tab_personne_intervention'
    __select__ = one_line_rset() & tabs.EntityRelationView.__select__ & is_instance('Personne')
    rtype = 'intervenant'
    role = 'object'
    title = None
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = ('Any T, I, T ORDERBY CI, T WHERE T intervenants I, I intervenant X, X eid %(eid)s, T compte C, C inventaire CI')
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', cellvids={0:'outofcontext', 1:'intervenant_flags', 2: 'transaction_vendeurs'}, title=_('Intervient sur'),
                   )

class TabPersonneDestinataire(tabs.EntityRelationView):
    __regid__ = 'tab_personne_destinataire'
    __select__ = one_line_rset() & tabs.EntityRelationView.__select__ & is_instance('Personne')
    rtype = 'destinataire'
    role = 'object'
    title=None
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any T, A ORDERBY CI, T WHERE T destinataires D, T achat A, D destinataire P, P eid %(eid)s, T compte C, C inventaire CI'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null',
                   title=_('Destinataire de'),
                   cellvids={0: 'outofcontext',
                             1: 'achat_nbdest'})

class TabPersonneArtisan(tabs.EntityRelationView):
    __regid__ = 'tab_personne_artisan'
    __select__ = one_line_rset() & tabs.EntityRelationView.__select__ & is_instance('Personne')
    title=None
    rtype = 'artisan'
    role = 'object'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any T, I, PRIX, T  ORDERBY CI, T WHERE T travaux D, D tache I, D salaire_argent PRIX?, D artisan P, P eid %(eid)s, T compte C, C inventaire CI'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Artisan pour'), cellvids={0: 'outofcontext', 3: 'transaction_achats'})

class TabPersonneVendeur(tabs.EntityRelationView):
    __regid__ = 'tab_personne_vendeur'
    __select__ = one_line_rset() & tabs.EntityRelationView.__select__ & is_instance('Personne')
    title=None
    rtype = 'vendeur'
    role = 'object'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any T, A ORDERBY CI, T WHERE T vendeurs V, V vendeur P, P eid %(eid)s, T achat A, T compte C, C inventaire CI'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Vendeur'), cellvids={0: 'outofcontext'})


class TabPersonneRattachement(tabs.EntityRelationView):
    __regid__ = 'tab_personne_rattachement'
    __select__ = one_line_rset() & tabs.EntityRelationView.__select__ & is_instance('Personne')
    title=None
    rtype = 'rattache_a'
    role = 'object'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any O, P ORDERBY N WHERE O personne P, O rattache_a X, X eid %(eid)s, P identite N'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Rattachements'),)


from cubicweb.web.views import dotgraphview

class PersonneRelationsView(dotgraphview.DotGraphView):
    __regid__ = 'personne_relations'
    __select__ = is_instance('Personne')
    title = 'Personne : relations'
    backend_kwargs = {'ratio': 'auto',
                      'additionnal_param': {
                          #'overlap': 'scale',
                          'rankdir':'LR'
                          },
                      'renderer': 'dot',

        }
    def build_visitor(self, entity):
        return PersonneRelationVisitor(self._cw, [entity])
    def build_dotpropshandler(self):
        return PersonnePropsHandler(self._cw)

class PersonneRelationVisitor(object):
    def __init__(self, cw, personnes):
        self._cw = cw
        if isinstance(personnes, list):
            self.personnes = personnes
        else:
            self.personnes = [personnes]
        self._edges = []

    def nodes(self):
        for personne in self.personnes:
            for occupation in personne.reverse_rattache_a:
                try:
                    p = occupation.personne[0]
                    self._edges.append((occupation, p, personne))
                    yield p.eid, p
                except IndexError:
                    continue
            yield personne.eid, personne
            related_to_rql = 'Any O WHERE O personne P, O rattache_a X, P eid %(eid)s'
            for o in self._cw.execute(related_to_rql, {'eid': personne.eid}).entities():
                p = o.rattache_a[0]
                self._edges.append((o, personne, p))
                yield p.eid, p

    def edges(self):
        known = set()
        all_persons = set(p.eid for p in self.personnes)
        for _occupation, p1, p2 in self._edges:
            all_persons.add(p1.eid)
            all_persons.add(p2.eid)
        eids = ','.join(str(e) for e in all_persons)
        rql = 'Any O WHERE O is Occupation, O personne X, X eid IN (%s), O rattache_a Y, Y eid IN (%s)'
        rql = rql % (eids, eids)
        for occupation in self._cw.execute(rql).entities():
            p1 = occupation.personne[0]
            p2 = occupation.rattache_a[0]
            title = occupation.dc_title()
            if (p1.eid, title, p2.eid) not in known:
                known.add((p1.eid, title, p2.eid))
                if title.strip():
                    yield p1.eid, p2.eid, occupation

        ## for occupation, p1, p2 in self._edges:
        ##     current = (p1.eid, p2.eid, occupation.dc_title())
        ##     if current not in known:
        ##         known.add(current)
        ##         yield p1.eid, p2.eid, occupation

class PersonnePropsHandler(dotgraphview.DotPropsHandler):
    def node_properties(self, personne):
        """return default DOT drawing options for a personne"""
        props = super(PersonnePropsHandler, self).node_properties(personne)
        props.update({'fontname': 'sans',
                      #'href': personne.absolute_url(vid='personne_liens'),
                      })
        return props

    def edge_properties(self, occupation, from_, to):
        props = super(PersonnePropsHandler, self).edge_properties(occupation, from_, to)
        props.update({'label': occupation.dc_title(),
                      'fontname': 'sans', 'fontsize': 10})
        return props


class MergeComponent(component.EntityCtxComponent):
    __regid__ = 'mergepersonne'
    __select__ = (one_line_rset() & component.EntityCtxComponent.__select__ &
                  is_instance('Personne'))
    context = 'navcontentbottom'
    title = _('merge personnes')

    def render_body(self, w):
        self._cw.add_js(('cubes.myosotis.merge.js',
                         'cubicweb.widgets.js',
                         #'jquery.autocomplete.js',
                         'jquery.js',))
        self._cw.add_onload('initMergePersonnes();')
        #self._cw.add_css('jquery.autocomplete.css')
        entity = self.entity
        w(u'<div id="personnemergeformholder%s">' % entity.eid)
        w(u'<h5>%s</h5>' % self._cw._('Identity of the Personne to merge'))
        w(u'<input  type="hidden" id="personneeid" value="%s"/>' % entity.eid)
        w(u'<input id="acmergepersonne" type="text" class="widget" cubicweb:dataurl="%s" '
          u'cubicweb:loadtype="auto" cubicweb:wdgtype="LazySuggestField" name="selected-personne"/>'
          % xml_escape(self._cw.build_url('json', fname='unrelated_merge_personnes',
                                          arg=entity.eid)))
        w(u'<div id="personne_entities_holder"></div>')
        w(u'<div id="sgformbuttons" class="hidden">')
        w(u'<input class="validateButton" type="button" value="%s" onclick="javascript:mergePersonnes(%s);"/>'
               % ( self._cw._('merge (keeping %s)') % xml_escape(entity.dc_title()), entity.eid))
        w(u'<input class="validateButton" type="button" value="%s" onclick="javascript:cancelSelectedMergePersonne(%s)"/>'
               % ( self._cw._(stdmsgs.BUTTON_CANCEL[0]), entity.eid))
        w(u'</div>')
        w(u'</div>')

#XXX the following needs updating

@ajaxcontroller.ajaxfunc(output_type='json')
def unrelated_merge_personnes(self, eid):
    """return personne unrelated to an entity"""
    rql = 'Any T, N ORDERBY N WHERE T is Personne, T identite N, NOT T eid %(x)s'
    return [{'value': eid, 'label': identite}  for (eid, identite) in self._cw.execute(rql, {'x' : eid})]

@ajaxcontroller.ajaxfunc(output_type='xhtml')
def personne_entity_html(self, eid, name):
    rset = self._cw.execute('Any P WHERE P is Personne, P identite %(x)s, NOT P eid %(eid)s',
                            {'x': name, 'eid': eid})
    html = []
    if rset:
        html.append('<div id="personneEntities">')
        #FIXME - add test to go through select_view
        view = self._cw.vreg['views'].select('list', self._cw, rset=rset)
        html.append(view.render(title=self._cw._('Candidates:')))
        html.append(u'</div>')
        # html.append(self._cw.view('list', rset))
    else:
        html.append('<div>%s</div>' %_('no personne found'))
        view = self._cw.vreg['views'].select('null', self._cw, rset=rset)
    return u' '.join(html)


@ajaxcontroller.ajaxfunc()
def merge_personnes(self, eid, other_eid):
    other_eid = int(other_eid)
    relations = ['receveur',
                 'rattache_a',
                 'personne',
                 'artisan',
                 'vendeur',
                 'destinataire',
                 'intervenant',
                 ]
    p1= self._cw.entity_from_eid(eid)
    p2 = self._cw.entity_from_eid(other_eid)
    self.info('merging %s with %s (keeping %s)', p1.identite, p2.identite, p1.identite)
    for rtype in relations:
        rql = 'SET X %s P1 WHERE X %s P2, P1 eid %%(p1)s, P2 eid %%(p2)s' % (rtype, rtype)
        rset = self._cw.execute(rql, {'p1': eid, 'p2': other_eid})
        self.info('merged %d relations %s', len(rset), rtype)
    self.info('delete %s (%s)', p2.identite, p2.eid)
    self._cw.execute('DELETE Personne P WHERE P eid %(eid)s', {'eid': p2.eid})
    return
