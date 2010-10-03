from cubicweb.view import EntityAdapter
from cubicweb.selectors import is_instance

class OccupationICalendarableAdapter(EntityAdapter):
    __regid__ = 'ICalendarable'
    __select__ = is_instance('Occupation')

    @property
    def start(self):
        return self.entity.compte[0].debut

    @property
    def stop(self):
        return self.entity.compte[0].fin
