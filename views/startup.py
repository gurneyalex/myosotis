from logilab.mtconverter import xml_escape
from cubicweb.view import StartupView

_ = unicode

class CompteTimeline(StartupView):
    __regid__ = "myosotis.compte_timeline"
    title = "compte timeline"
    def call(self):
        rset = self._cw.execute('Any C WHERE C is Compte')
        self.wview('myosotis.timeline', rset)

class Parures(StartupView):
    __regid__ = 'myosotis.type_parure'
    title = 'Types de parure'
    def call(self):
        rset = self._cw.execute('Any N, COUNT(P) GROUPBY N ORDERBY N ASC WHERE P is Parure, P nature N')
        rows = []
        for nature, count in rset:
            rql = u'Any P WHERE P is Parure, P nature "%s"' % nature # XXX injection ? 
            url = self._cw.build_url(rql=rql,
                                     __force_display=1,
                                     vid='myosotis.parure_summary')
            rows.append((u"<a href='%s'>%s</a>" % (xml_escape(url), xml_escape(nature)), count))
        self.wview('pyvaltable', pyvalue=rows, headers = [_('nature'), _('nombre')])
                      
        
