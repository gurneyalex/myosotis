# -*- coding: utf-8 -*-
from cubicweb.entities import AnyEntity, fetch_config
_ = unicode
class Transaction(AnyEntity):
    __regid__ = 'Transaction'
    fetch_attrs, cw_fetch_order = fetch_config(('pagination','date', 'date_ordre', 'date_recette', 'occasion', 'lieu', 'prix_ensemble', ))

    @property
    def _date(self):
        if self.date is None:
            if self.date_ordre is None:
                if self.date_recette is None:
                    date = _('pas de date')
                else:
                    date = self.date_recette
            else:
                date = self.date_ordre
        else:
            date = self.date
        return date
    
    def dc_title(self):
        date = self._date
        return u'p. %s [n° %d, %s]' % (self.pagination, self.eid, date,)
    def dc_long_title(self):
        date = self._date
        return u'%s p. %s [n° %d, %s]' % ( self.compte[0].inventaire, self.pagination, self.eid, date,)

    def get_best_date(self):
        if self.date:
            return self.date
        if self.date_ordre:
            return self.date_ordre
        if self.date_recette:
            return self.date_recette
        compte = self.compte[0]
        return compte.debut

class Intervenant(AnyEntity):
    __regid__ = 'Intervenant'
    fetch_attrs, cw_fetch_order = fetch_config(('indemnite',
                                             #'nb_moyen_transport',
                                             #'moyen_transport',
                                             #'prix_transport',
                                             #'nombre_valets',
                                             #'prix_valet',
                                             #'duree',
                                             'payeur',
                                             'pris',
                                             'commandement',
                                             'relation_de',
                                             'donne_par',
                                             'par_la_main',
                                             'present',
                                             'delivre_a',
                                             'fait_compte_avec',
                                             'intervenant'))
    def dc_title(self):
        return self.intervenant[0].dc_title()

class Vendeur(AnyEntity):
    __regid__ = 'Vendeur'
    fetch_attrs, cw_fetch_order = fetch_config(('vendeur', 'expression'))
    def dc_title(self):
        return self.vendeur[0].dc_title()

class Travail(AnyEntity):
    __regid__ = 'Travail'
    fetch_attrs, cw_fetch_order = fetch_config(('tache', 'artisan', 'salaire_argent'))

    def dc_title(self):
        title = self.tache
        multi_artisans = self._cw.execute('Any COUNT(Y) WHERE X eid %(eid)s, T travaux X, T travaux Y',
                                          {'eid': self.eid})[0][0]
        if multi_artisans > 1:
            title += u' (+)'
        return title
        
