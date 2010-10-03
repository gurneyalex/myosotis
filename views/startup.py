from cubicweb.view import StartupView


class CompteTimeline(StartupView):
    __regid__ = "myosotis.compte_timeline"
    title = "compte timeline"
    def call(self):
        rset = self._cw.execute('Any C WHERE C is Compte')
        self.wview('myosotis.timeline', rset)

class Parures(StartupView):
    pass
