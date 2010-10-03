from cubicweb.web.views import baseviews
from cubicweb.selectors import is_instance

class ParureOutOfContextView(baseviews.OutOfContextView):
    __select__ = is_instance('Parure')
    def cell_call(self, row, col):
        super(ParureOutOfContextView, self).cell_call(row, col)
        entity = self.cw_rset.get_entity(row, col)
        rset = self._cw.execute('Any Count(T) where T is MateriauxParure, C composee_de T, C eid %(eid)s', {'eid': entity.eid})
        length = rset[0][0]

        self.w(u' (%d)' % length)
