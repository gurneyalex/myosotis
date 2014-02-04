# -*- coding: utf-8 -*-
from __future__ import division
import pprint
import codecs
import math
from datetime import timedelta

from logilab.common.decorators import cached
from cubicweb.entities import AnyEntity, fetch_config

from cubes.myosotis.graph import dijkstra

FIVE_YEARS = timedelta(365*5)

class Monnaie(AnyEntity):
    __regid__ = 'Monnaie'
    fetch_attrs, cw_fetch_order = fetch_config(['nom', 'type'])

_PRIX_TRANSACTIONS={}
def get_all_prix_transactions(cw):
    result = _PRIX_TRANSACTIONS
    if result:
        return result
    print 'get_all_prix_transactions'
    rql = '''(Any P, T WHERE T is Transaction, P is Prix, T prix_ensemble P)
             UNION
             (Any P, T WHERE T is Transaction, P is Prix, T achat A1, A1 prix_unitaire P)
             UNION
             (Any P, T WHERE T is Transaction, P is Prix, T achat A2, A2 prix_total P)
             UNION
             (Any P, T WHERE T is Transaction, P is Prix, T travaux TR1, TR1 salaire_argent P)
             UNION
             (Any P, T WHERE T is Transaction, P is Prix, T travaux TR2, TR2 salaire_aides P)
             UNION
             (Any P, T WHERE T is Transaction, P is Prix, T intervenants I1, I1 prix_valet P)
             UNION
             (Any P, T WHERE T is Transaction, P is Prix, T intervenants I2, I2 prix_transport P)'''
    rset = cw.execute(rql)
    print len(rset)
    for p_eid, t_eid in rset:
        if p_eid not in result:
            result[p_eid] = [t_eid]
        else:
            result[p_eid].append(t_eid)
    print len(result)
    return result

class Prix(AnyEntity):
    __regid__ = 'Prix'
    fetch_attrs, cw_fetch_order = fetch_config(('conversion',
                                                'livres', 'sous', 'deniers',
                                                'florins', 'gros', 'sous_florins', 'denier_florins',
                                                'monnaie'))

    def dc_title(self):
        if self.conversion:
            return u'%.2f' % self.conversion
        return self.raw_title()
    
    def raw_title(self):
#        self.complete()
        monnaie = self.monnaie[0]
#        return u'%s %s' % (self.float_value, monnaie.nom)
        if monnaie.type == u'Livre/Sous/Denier':
            return u'%s£ %ss %.2fd %s' % (self.livres or 0 , self.sous or 0, self.deniers or 0, monnaie.nom)
        elif monnaie.type == u'Florin/Gros':
            if self.florin_ad:
                ad = u' ad %.1f' % (self.florin_ad or self.monnaie[0].nb_gros)
            else:
                ad = u''
            return u'%sf %sg %ss %.2fd %s%s' % (self.florins or 0,
                                                self.gros or 0,
                                                self.sous_florins or 0,
                                                self.denier_florins or 0,
                                                monnaie.nom,
                                                ad)
        else:
            return u'%.2f %s' % (self.monnaie_or, monnaie.nom)

    @property
    def float_value(self):
        monnaie = self.monnaie[0]
        if monnaie.type == u'Livre/Sous/Denier':
            return (self.deniers or 0.) + 12.*((self.sous or 0.) + 20.*(self.livres or 0))
        elif monnaie.type == u'Florin/Gros': # XXX
            if not (self.denier_florins or self.sous_florins or self.gros):
                return self.florins or 0.
            elif self.florin_ad:
                ad = self.florin_ad
            else:
                ad = self.monnaie[0].nb_gros
            return self.florins or 0. + ((self.gros or 0.) + (self.denier_florins or 0.) + (self.sous_florins or 0.)*12) / (ad or self.monnaie[0].nb_gros)
        else:
            return self.monnaie_or or 0.



    def get_transaction(self, allow_multi=False):
        prix_transactions = get_all_prix_transactions(self._cw)
        if self.eid not in prix_transactions:
            rql = '''Any T WHERE T is Transaction, P eid %(eid)s,
            EXISTS(T prix_ensemble P) OR EXISTS(T achat A1, A1 prix_unitaire P)
            OR EXISTS(T achat A2, A2 prix_total P)
            OR EXISTS(T travaux TR1, TR1 salaire_argent P) OR EXISTS(T travaux TR2, TR2 salaire_aides P)
            OR EXISTS(T intervenants I1, I1 prix_valet P) OR EXISTS(T intervenants I2, I2 prix_transport P)'''
            rset = self._cw.execute(rql, {'eid': self.eid})
            for eid, in rset:
                prix_transactions.setdefault(self.eid, []).append(eid)
        transaction_eids = prix_transactions.get(self.eid, [])
        if len(transaction_eids) == 0:
            with codecs.open('prix_transaction.err', 'a', 'utf-8') as f:
                f.write(u'no transaction found for prix %s\n' % (self.eid))
                self.set_attributes(source=u'no_transaction')
            if allow_multi:
                return []
            else:
                return None
        elif len(transaction_eids) == 1:
            if allow_multi:
                return [self._cw.entity_from_eid(transaction_eids[0])]
            else:
                return self._cw.entity_from_eid(transaction_eids[0])
        else:
            rset = self._cw.execute('Any T WHERE T is Transaction, T eid in (%s)' % (','.join(str(eid) for eid in transaction_eids)))
            transactions = [trans for trans in rset.entities()]
            comptes = set(trans.compte[0].eid for trans in transactions)
            if len(comptes) != 1:
                with codecs.open('prix_transaction.err', 'a', 'utf-8') as f:
                    f.write(u"multiple comptes found for prix %s:  %s\n" % (self.eid, list(comptes)))
            if allow_multi:
                return transactions
            else:
                return transactions[0]
             #raise ValueError('too many transactions found for prix %s: %s' % (self.eid, [t.eid for t in rset.entities()]))

    def calcule_conversion(self, monnaie_cible, update=False):
        mode = None
        conversion = None
        used_changes = []
        if self.monnaie[0].nom == monnaie_cible.nom:
            mode = u'direct'
            conversion = self.float_value
        else:
            path = None
            for mode, changes in self._search_changes():
                path = self._get_change_path(changes, monnaie_cible.eid)
                if path:
                    conversion = self.float_value
                    monnaie = self._get_monnaie()
                    for comp in path:
                        change = comp[-1][-1] # comp is (monn1_eid, monn2_eid, (monn1_eid, monn2_eid, change))
                        used_changes.append(change)
                        conversion, monnaie = change.change(conversion, monnaie)
                    break
            else:
                mode = None
                conversion = None
        if update:
            self.set_attributes(conversion=conversion, source=mode)
            if used_changes:
                self.set_relations(changes=used_changes)
            else:
                self.set_relations(changes=None)
        return mode, conversion

    def _search_changes(self):
        transaction = self.get_transaction()
        if transaction is None:
            return
        if transaction.change:
            yield u'conv_transaction', [change for change in transaction.change if change.is_valid]
        compte = transaction.compte[0]
        if compte.change:
            changes = [change for change in compte.change if change.is_valid]
            #print "compte\t", len(changes)
            yield u'conv_compte', changes
        rs = self._cw.execute('Any CH WHERE C is Compte, C change CH, C debut <= %(fin)s, C fin >= %(debut)s',
                              {'debut': compte.debut,
                               'fin': compte.fin})
        changes = [change for change in rs.entities() if change.is_valid]
        #print "voisins\t", len(changes)
        yield u'conv_voisin', changes
        rs = self._cw.execute('Any CH WHERE C is Compte, C change CH, C debut <= %(fin)s, C fin >= %(debut)s',
                              {'debut': compte.debut - FIVE_YEARS,
                               'fin': compte.fin + FIVE_YEARS})
        changes = [change for change in rs.entities() if change.is_valid]
        #print "voisins 2\t", len(changes)
        yield u'conv_voisin 2', changes
        rs = self._cw.execute('Any CH WHERE C is Compte, C historic False, C change CH')
        changes_externes = [change for change in rs.entities() if change.is_valid]
        changes_ids = frozenset([ch.set_eid_monnaies for ch in changes])
        for chg in changes_externes:
            if chg.set_eid_monnaies not in changes_ids:
                changes.append(chg)
        #print "externe\t", len(changes)
        yield u'conv_externe', changes

    def _get_change_path(self, changes, monnaie_cible):
        monnaie_depart = self._get_monnaie()
        arcs = [(change.eid_monnaie_depart, change.eid_monnaie_converti, change) for change in changes]
        arc_count = {}
        for eid1, eid2, change in arcs:
            if eid1 > eid2:
                eid1, eid2 = eid2, eid1
                ratio = change.ratio
            else:
                ratio = 1. / change.ratio
            arc_count.setdefault((eid1, eid2), {}).setdefault(ratio, []).append(change)
        #pprint.pprint(arc_count)
        path = dijkstra(arcs, monnaie_depart, monnaie_cible)
        for comp in path:
            eid1, eid2, change = comp[-1]# comp is (monn1_eid, monn2_eid, (monn1_eid, monn2_eid, change))
            if eid1 > eid2:
                eid1, eid2 = eid2, eid1
            changes = arc_count[(eid1, eid2)]
            if len(changes) > 1:
                change_list = []
                self.warning('different changes for %s -> %s : %s', eid1, eid2, changes)
                with codecs.open('multichanges.txt', 'a', 'utf-8') as f:
                    f.write(u'Prix %s:\n' % self.eid)
                    ratios = []
                    for ratio, _changes in sorted(changes.iteritems()):
                        for c in _changes:
                            change_list.append((ratio, c))
                            ratio, _eid = c.change(1., eid2)
                            monnaie1 = self._cw.entity_from_eid(eid1)
                            monnaie2 = self._cw.entity_from_eid(eid2)
                            msg = u'1 %s -> %f %s' % (monnaie1.dc_title(),
                                                     ratio,
                                                     monnaie2.dc_title())
                            f.write(u'%d %s\n' % (c.eid, msg))
                            ratios.append(ratio)
                    f.write(u'ratio max/min: %.2f\n\n' % (max(ratios) / min(ratios)))
                print 'Prix %d %.2f' % (self.eid, max(ratios) / min(ratios))
                # change_list contains the (ratio, change) sorted by increasing ratio
                # we want to use the median ratio.
                nb_changes = len(change_list)
                middle = nb_changes / 2.
                index = int(math.floor(middle))
                if index == middle:
                    r1 = change_list[index-1][0]
                    r2 = change_list[index][0]
                    if r1 != r2:
                        if len(changes[r2]) > len(changes[r1]):
                            index = index + 1
                        elif len(changes[r2]) == len(changes[r1]):
                            index = index # XXX we should do something smart here

        return path

    def _get_monnaie(self):
        return self.monnaie[0].eid

    def equal(self, other):
        if self._get_monnaie() == other._get_monnaie():
            for att in ('livres', 'sous', 'deniers', 'florins', 'gros', 'sous_florins', 'denier_florins'):
                val1 = getattr(self, att) or None
                val2 = getattr(other, att) or None
                if val1 != val2:
                    return False
            return True
        return False

class Change(AnyEntity):
    __regid__ = 'Change'
    def dc_title(self):
        prix_depart = self.prix_depart[0]
        prix_converti = self.prix_converti[0]
        return u"%s -> %s" % (prix_depart.monnaie[0].dc_title(), prix_converti.monnaie[0].dc_title())

    def dc_long_title(self):
        prix_depart = self.prix_depart[0]
        prix_converti = self.prix_converti[0]
        return u"1 %s -> %.2f %s" % (prix_depart.monnaie[0].dc_title(), self.ratio, prix_converti.monnaie[0].dc_title())

    def dc_long_title2(self):
        prix_depart = self.prix_depart[0]
        prix_converti = self.prix_converti[0]
        return u"%s -> %s" % (prix_depart.dc_title(), prix_converti.dc_title())

    @property
    def date(self):
        rql = 'Any X WHERE X change C, C eid %(eid)s'
        rset = self._cw.execute(rql, {'eid': self.eid})
        if rset:
            entity = rset.get_entity(0, 0)
            if entity.__regid__ == 'Transaction':
                return entity._date
            elif entity.__regid__ == 'Compte':
                return entity.fin
        return None


    @property
    def eid_monnaie_depart(self):
        return self.prix_depart[0]._get_monnaie()
    @property
    def eid_monnaie_converti(self):
        return self.prix_converti[0]._get_monnaie()
    @property
    def set_eid_monnaies(self):
        return frozenset([self.eid_monnaie_depart, self.eid_monnaie_converti])

    @property
    def is_valid(self):
        p1 = self.prix_converti[0].float_value
        p2 = self.prix_depart[0].float_value
        return p1 != 0 and p2 != 0

    def change(self, prix_float, monnaie):
        assert self.is_valid, "invalid change"
        p1 = self.prix_converti[0].float_value
        p2 = self.prix_depart[0].float_value
        ratio = p1 / p2
        if monnaie == self.eid_monnaie_depart:
            return prix_float * ratio, self.eid_monnaie_converti
        elif monnaie == self.eid_monnaie_converti:
            return prix_float / ratio, self.eid_monnaie_depart
        else:
            raise ValueError(u'Bad Monnaie %s' % monnaie)

    @property
    def ratio(self):
        p1 = self.prix_converti[0].float_value
        p2 = self.prix_depart[0].float_value
        if p2 == 0:
            return -1
        ratio = p1 / p2
        return ratio
