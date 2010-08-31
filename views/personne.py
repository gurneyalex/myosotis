# -*- coding: utf-8
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
            _('tab_personne_rattachement')
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


