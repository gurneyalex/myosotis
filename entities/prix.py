# -*- coding: utf-8 -*-
import pprint

from cubicweb.entities import AnyEntity, fetch_config

from cubes.myosotis.graph import dijkstra

class Monnaie(AnyEntity):
    __regid__ = 'Monnaie'
    fetch_attrs, fetch_order = fetch_config(['nom', 'type'])

class Prix(AnyEntity):
    __regid__ = 'Prix'
    fetch_attrs, fetch_order = fetch_config(('livres', 'sous', 'deniers', 'florins', 'gros', 'sous_florins', 'denier_florins', 'monnaie'))

    def dc_title(self):
#        self.complete()
        monnaie = self.monnaie[0]
#        return u'%s %s' % (self.float_value, monnaie.nom)
        if monnaie.type == u'Livre/Sous/Denier':
            return u'%s£ %ss %sd %s' % (self.livres or 0 , self.sous or 0, self.deniers or 0, monnaie.nom)
        elif monnaie.type == u'Florin/Gros':
            return u'%sf %sg %ss %sd %s' % (self.florins or 0, self.gros or 0, self.sous_florins or 0, self.denier_florins or 0, monnaie.nom)
        else:
            return u'%s %s' % (self.monnaie_or, monnaie.nom)

    @property
    def float_value(self):
        monnaie = self.monnaie[0]
        if monnaie.type == u'Livre/Sous/Denier':
            return (self.deniers or 0) + 12*((self.sous or 0) + 20*(self.livres or 0))
        elif monnaie.type == u'Florin/Gros': # XXX
            return ((self.denier_florins or 0)/20. + (self.sous_florins or 0) + (self.gros or 0))/12. + (self.florins or 0)
        else:
            return self.monnaie_or or 0

    def get_transaction(self):
        rql = '''Any T WHERE T is Transaction, P eid %(eid)s,
        EXISTS(T prix_ensemble P) OR EXISTS(T achat A1, A1 prix_unitaire P)
        OR EXISTS(T achat A2, A2 prix_total P)
        OR EXISTS(T travaux TR1, TR1 salaire_argent P) OR EXISTS(T travaux TR2, TR2 salaire_aides P)
        OR EXISTS(T intervenants I1, I1 prix_valet P) OR EXISTS(T intervenants I2, I2 prix_transport P)'''
        rset = self._cw.execute(rql, {'eid': self.eid})
        if len(rset) == 0:
            with open('prix_transaction.err', 'a') as f:
                f.write('no transaction found for prix %s\n' % (self.eid))
            return None
        elif len(rset) == 1:
            return rset.get_entity(0, 0)
        else:
            transactions = list(rset.entities())
            comptes = set(trans.compte[0].eid for trans in transactions)
            if len(comptes) != 1:
                with open('prix_transaction.err', 'a') as f:
                    f.write("multiple comptes found for prix %s:  %s\n" % (self.eid, list(comptes)))
            return transactions[0]
             #raise ValueError('too many transactions found for prix %s: %s' % (self.eid, [t.eid for t in rset.entities()]))

    def calcule_conversion(self, monnaie_cible, update=False):
        mode = None
        conversion = None
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
                        conversion, monnaie = change.change(conversion, monnaie)
                    break
            else:
                mode = None
                conversion = None
        if update:
            self.set_attributes(conversion=conversion, source=mode)
        return mode, conversion

    def _search_changes(self):
        transaction = self.get_transaction()
        if transaction is None:
            return
        if transaction.change:
            yield u'conv_transaction', [change for change in transaction.change if change.is_valid]
        compte = transaction.compte[0]
        if compte.change:
            yield u'conv_compte', [change for change in compte.change if change.is_valid]
        rs = self._cw.execute('Any CH WHERE C is Compte, C change CH, C debut <= %(fin)s, C fin >= %(debut)s', {'debut': compte.debut, 'fin': compte.fin})
        changes = [change for change in rs.entities() if change.is_valid]
        yield u'conv_voisin', changes

    def _get_change_path(self, changes, monnaie_cible):
        monnaie_depart = self._get_monnaie()
        arcs = [(change.eid_monnaie_depart, change.eid_monnaie_converti, change) for change in changes]
        path = dijkstra(arcs, monnaie_depart, monnaie_cible)
        return path
    def _get_monnaie(self):
        return self.monnaie[0].eid


class Change(AnyEntity):
    __regid__ = 'Change'
    def dc_title(self):
        prix_depart = self.prix_depart[0]
        prix_converti = self.prix_converti[0]
        return u"%s -> %s" % (prix_depart.monnaie[0].dc_title(), prix_converti.monnaie[0].dc_title())

    @property
    def eid_monnaie_depart(self):
        return self.prix_depart[0]._get_monnaie()
    @property
    def eid_monnaie_converti(self):
        return self.prix_converti[0]._get_monnaie()

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
