#-*- coding: utf-8 -*-

from cubicweb.entities import AnyEntity, fetch_config

class Parure(AnyEntity):
    __regid__ = 'Parure'
    fetch_attrs, fetch_order = fetch_config(['nature', 'type', 'caracteristique'])
    def dc_title(self):
        #self.complete()
        return u'%s %s'% (self.nature, self.caracteristique or '')

    def quantite(self):
        if self.reverse_parure:
            return self.reverse_parure[0].quantite

    def materiaux(self):
        materiaux = []
        for mp in self.composee_de:
            if mp.materiaux:
                if mp.quantite is None:
                    quantite = None
                else:
                    quantite = u"%s %s" % (mp.quantite, mp.unite)
                materiaux.append((mp.materiaux[0],
                                  mp.materiaux_achete,
                                  False,
                                  quantite,
                                  mp.usage) )
            else:
                print u'warning : pas de materiaux lié à ', mp.eid

        for achat in self.reverse_parure:
            materiaux_achete = True
            if not hasattr(achat, 'avec_mat'):
                continue
            for avecmat in achat.avec_mat:
                for achatmat in avecmat.achat_matiere:
                    quantite = avecmat.conversion
                    usage = avecmat.usage or ''
                    quantite_partagee = False

                    if avecmat.quantite is None:
                        if achatmat.quantite:
                            quantite = u'%s %s' % (achatmat.quantite, achatmat.unite)
                            quantite_partagee = True
                        else:
                            quantite = None
                    else:
                        quantite = u'%s %s' % (avecmat.quantite, avecmat.unite)
                    #print quantite
                    materiaux.append((achatmat.materiaux[0],
                                     materiaux_achete,
                                     quantite_partagee,
                                     quantite,
                                     usage))
        return materiaux
    def date(self):
        try:
            achat = self.reverse_parure[0]
        except IndexError:
            #print "pas d'achat pour parure", self.eid
            return u'null'
        if achat.date_achat:
            return achat.date_achat
        transaction = achat.reverse_achat[0]
        return transaction.get_best_date()
