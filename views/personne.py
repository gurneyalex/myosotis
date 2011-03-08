# -*- coding: utf-8
from cubicweb.view import EntityView
from cubicweb.web.views import tabs
from cubicweb.selectors import is_instance

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
            ]
    default_tab='tab_personne'

class PersonneTab(tabs.PrimaryTab):
    __regid__ = 'tab_personne'
    __select__ = is_instance('Personne')
    title = None
    def render_entity_relations(self, entity):
        _ = self._cw._
        super(PersonneTab, self).render_entity_relations(entity)
        subst = {'eid': entity.eid}
        rql = ('Any X, L, V, R, O, C, F WHERE '
               'X is Occupation, '
               'X personne P, '
               'P eid %(eid)s, '
               'X compte C, '
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

class TabPersonneIntervention(tabs.EntityRelationView):
    __regid__ = 'tab_personne_intervention'
    __select__ = tabs.EntityRelationView.__select__ & is_instance('Personne')
    rtype = 'intervenant'
    role = 'object'
    title = None
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = ('Any T, G, H, J, K, L, M, N, O, P  WHERE T intervenants I, I intervenant X, X eid %(eid)s, I payeur G, I pris H, I commandement J, I relation_de K, I donne_par L, I par_la_main M, I present N, I delivre_a O, I fait_compte_avec P')
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Intervient sur'),
                   )

class TabPersonneDestinataire(tabs.EntityRelationView):
    __regid__ = 'tab_personne_destinataire'
    __select__ = tabs.EntityRelationView.__select__ & is_instance('Personne')
    rtype = 'destinataire'
    role = 'object'
    title=None
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any D, T WHERE T destinataires D, D destinataire P, P eid %(eid)s'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Destinataire de'),)

class TabPersonneArtisan(tabs.EntityRelationView):
    __regid__ = 'tab_personne_artisan'
    __select__ = tabs.EntityRelationView.__select__ & is_instance('Personne')
    title=None
    rtype = 'artisan'
    role = 'object'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any D, T WHERE T travaux D, D tache I, D artisan P, P eid %(eid)s'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Artisan pour'),)

class TabPersonneVendeur(tabs.EntityRelationView):
    __regid__ = 'tab_personne_vendeur'
    __select__ = tabs.EntityRelationView.__select__ & is_instance('Personne')
    title=None
    rtype = 'vendeur'
    role = 'object'
    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        subst = {'eid': entity.eid}
        rql = 'Any V, T WHERE T vendeurs V, V vendeur P, P eid %(eid)s'
        rset = self._cw.execute(rql, subst)
        self.wview('table', rset, 'null', title=_('Vendeur'),)


class TabPersonneRattachement(tabs.EntityRelationView):
    __regid__ = 'tab_personne_rattachement'
    __select__ = tabs.EntityRelationView.__select__ & is_instance('Personne')
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
                    #print 'occ', occupation.eid
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
