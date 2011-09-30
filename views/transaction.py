# -*- coding: utf-8 -*-
from cubicweb.view import EntityView
from cubicweb.web.views import tabs, primary, basecontrollers
from cubicweb.selectors import is_instance, one_line_rset
from cubicweb.web.views.tableview import EntityAttributesTableView

class TransactionPrimaryView(primary.PrimaryView):
    __select__ = primary.PrimaryView.__select__ & is_instance('Transaction')

class TransactionTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Transaction')
    title = 'table transaction'
    __regid__ = 'myosotis.transaction.attributestableview'
    columns = ('transaction', 'achats', 'destinataires', 'prix', 'date', 'pagination', 'date_ordre', 'date_recette', )

    def build_transaction_cell(self, entity):
        return entity.view('incontext')

    def build_achats_cell(self, entity):
        return self._cw.view('list', entity.related('achat'), 'null')
        #return u', '.join([e.view('incontext') for e in entity.achat])

    def build_prix_cell(self, entity):
        prix = entity.prix_ensemble
        if prix:
            return prix[0].dc_title()
        return u''

    def build_destinataires_cell(self, entity):
        return self._cw.view('list', entity.related('destinataires'), 'null')

class VendeurTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Vendeur')
    __regid__ = 'attributestableview'
    columns = ('vendeur', 'expression')

    def build_vendeur_cell(self, entity):
        return entity.vendeur[0].view('incontext')

class IntervenantFlagsView(EntityView):
    __regid__ = 'intervenant_flags'
    __select__ = is_instance('Intervenant')
    def entity_call(self, entity):
        infos = []
        for attr in ('payeur', 'pris', 'commandement', 'relation_de', 'donne_par', 'par_la_main',
               'present', 'delivre_a', 'fait_compte_avec'):
            if getattr(entity, attr):
                infos.append(self._cw._(attr))
        self.w(u', '.join(infos))

class IntervenantTableView(EntityAttributesTableView):
    __select__ = EntityAttributesTableView.__select__ & is_instance('Intervenant')
    title = _('attributes table view')
    __regid__ = 'attributestableview'
    columns = (u'intervenant', u'infos',
               u'indemnite',
               #u'moyen_transport', u'prix_transport',
               #u'nombre_valets', u'prix_valet',
               #u'duree',
               )

    def build_intervenant_cell(self, entity):
        return entity.intervenant[0].view('incontext')

    def build_prix_transport_cell(self, entity):
        if entity.prix_transport:
            return entity.prix_transport[0].view('incontext')
        else:
            return u''
    def build_prix_valet_cell(self, entity):
        if entity.prix_valet:
            return entity.prix_valet[0].view('incontext')
        else:
            return u''
    def build_moyen_transport_cell(self, entity):
        nb = entity.nb_moyen_transport or u''
        moyen = entity.moyen_transport or u''
        return nb + u' ' + moyen

    def build_infos_cell(self, entity):
        return entity.view('intervenant_flags')

    def header_for_moyen_transport(self, sample):
        return u'moyen transp.'
    def header_for_prix_transport(self, sample):
        return u'prix transp.'
    def header_for_nombre_valets(self, sample):
        return u'valets'
    def header_for_prix_valet(self, sample):
        return u'prix valets'

