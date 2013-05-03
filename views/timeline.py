# -*- coding: utf-8 -*-
from logilab.mtconverter import xml_escape

from cubicweb.web.views import timeline
from cubicweb.predicates import is_instance, adaptable

class MyosotisTimeline(timeline.TimelineView):
    __regid__ = 'myosotis.timeline'
    __select__ =  adaptable('ICalendarable')
    widget_class = 'MyosotisTimelineWidget'
    jsfiles = timeline.TimelineView.jsfiles + ('cubicweb.myosotis.js',)

    def render_url(self, loadurl, tlunit=None): # copied to avoid loadtype=auto
        tlunit = tlunit or self._cw.form.get('tlunit')
        self._cw.add_js(self.jsfiles)
        self._cw.add_css('timeline-bundle.css')
        if tlunit:
            additional = u' cubicweb:tlunit="%s"' % tlunit
        else:
            additional = u''
        self.w(u'<div class="widget" cubicweb:wdgtype="%s" '
               u'cubicweb:loadurl="%s" style="height:400px;" %s >' %
               (self.widget_class, xml_escape(loadurl),
                additional))
        self.w(u'</div>')

    def call(self, tlunit=None):
        super(MyosotisTimeline, self).call(tlunit)
        min_start_date = min(entity.cw_adapt_to('ICalendarable').start
                             for entity in self.cw_rset.entities())
        year, month, day = min_start_date.year, min_start_date.month-1, min_start_date.day
        self.w(u'<script type="text/javascript">jQuery(document).ready(function(){setMinVisibleDate(new Date(%d, %d, %d));});</script>' % (year, month, day))

class MyosotisTimelineJson(timeline.TimelineJsonView):
    __select__ = adaptable('ICalendarable') & is_instance('Compte')
    colors = {u'trésorerie': 'gold',
              u'hôtel du comte': 'skyblue',
              u'hôtel de la comtesse': 'deeppink',
              u'compte de voyage': 'green',
              u'nul': 'grey',
              }
    def build_event(self, entity):
        event =  super(MyosotisTimelineJson, self).build_event(entity)
        event['color'] = self.colors.get(entity.type_compte.lower(), 'red')
        return event
