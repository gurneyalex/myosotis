# -*- coding: utf-8
from cubicweb.view import EntityView
from cubicweb.web.views import baseviews
from cubicweb.predicates import is_instance

class AchatWithNbDest(EntityView):
    __select__ = is_instance('AchatPretPorter', 'AchatMateriaux', 'AchatFabrication')
    __regid__ = 'achat_nbdest'
    title = _('achat nb dest')

    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        self.wview('outofcontext', self.cw_rset, row=row, col=col, **kwargs)
        self.w(u' [%d dest]' % entity.nb_dest)
        
