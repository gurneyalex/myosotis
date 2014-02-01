# -*- coding: utf-8 -*-
from cubicweb.view import EntityView
from cubicweb.web.views import tabs, primary, basecontrollers
from cubicweb.predicates import is_instance, one_line_rset, multi_columns_rset
from cubicweb.web.views.tableview import EntityTableView, MainEntityColRenderer, RelationColRenderer

class TransactionPrimaryView(primary.PrimaryView):
    __select__ = primary.PrimaryView.__select__ & is_instance('Transaction')


class TransactionTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Transaction')
    title = 'table transaction'
    __regid__ = 'myosotis.transaction.attributestableview'
    columns = ('transaction', 'occasion', 'achat', 'destinataires', 'prix_ensemble', 'date', 'pagination', 'date_ordre', 'date_recette', )
    column_renderers = {'transaction': MainEntityColRenderer(),
                        'occasion': RelationColRenderer(),
                        'achat': RelationColRenderer(vid='list'),
                        'prix_ensemble': RelationColRenderer(),
                        'destinataires': RelationColRenderer(vid='list'),
                        }


class TransactionAchatsView(EntityView):
    __select__ = one_line_rset & EntityView.__select__ & is_instance('Transaction')
    __regid__ = 'transaction_achats'

    def entity_call(self, entity):
        return self.wview('list', entity.related('achat'), 'null')


class TransactionDestinatairesView(EntityView):
    __select__ = one_line_rset & EntityView.__select__ & is_instance('Transaction')
    __regid__ = 'transaction_destinataires'

    def entity_call(self, entity):
        return self.wview('list', entity.related('destinataires'), 'null')


class TransactionVendeursView(EntityView):
    __select__ = one_line_rset & EntityView.__select__ & is_instance('Transaction')
    __regid__ = 'transaction_vendeurs'

    def entity_call(self, entity):
        return self.wview('list', entity.related('vendeurs'), 'null')


class VendeurTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Vendeur') 
    __regid__ = 'attributestableview'
    columns = ('vendeur', 'expression')
    column_renderers = {'vendeur': RelationColRenderer(subvid='incontext'),
                        }

class TravauxTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Travail') 
    __regid__ = 'attributestableview'
    columns = ('artisan', 'tache', 'salaire_argent')
    column_renderers = {'tache': MainEntityColRenderer(),
                        'artisan': RelationColRenderer(subvid='incontext'),
                        'salaire_argent': RelationColRenderer(subvid='incontext'),
                        }



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


class IntervenantTableView(EntityTableView):
    __select__ = EntityTableView.__select__ & is_instance('Intervenant')
    title = _('attributes table view')
    __regid__ = 'attributestableview'
    columns = (u'intervenant',
               u'infos',
               u'indemnite',
               )
    column_renderers = {'intervenant': RelationColRenderer(vid='incontext'),
                        'infos': MainEntityColRenderer(vid='intervenant_flags'),
                        }

