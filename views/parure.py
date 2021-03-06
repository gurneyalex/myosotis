# -*- coding: utf-8 -*-
from cubicweb.view import EntityView
from cubicweb.web.views import baseviews
from cubicweb.predicates import is_instance
from cubicweb.web.views import primary
from cubicweb.web.box import EntityBoxTemplate
from cubicweb.web.htmlwidgets import SideBoxWidget

class ParureOutOfContextView(baseviews.OutOfContextView):
    __select__ = is_instance('Parure')
    def cell_call(self, row, col):
        super(ParureOutOfContextView, self).cell_call(row, col)
        entity = self.cw_rset.get_entity(row, col)
        rset = self._cw.execute('Any Count(M) where P composee_de M, P eid %(eid)s', {'eid': entity.eid})
        if entity.reverse_parure:
            achat = entity.reverse_parure[0]
            if achat.__regid__ == 'AchatFabrication':
                orig = u'[F]'
            else:
                orig = u'[P]'
        else:
            orig = u'[?]'


        length = rset[0][0]
        rset2 = self._cw.execute('Any Count(M) where A parure P, A avec_mat M, P eid %(eid)s', {'eid': entity.eid})
        self.w(u' %s(%d) %s' % (orig, rset[0][0]+ rset2[0][0], entity.date()))


class ParurePrimaryView(primary.PrimaryView):
    __select__ = is_instance('Parure')

    def summary(self, entity):
        return u'%s' % entity.date()
    def render_entity_relations(self, entity):
        super(ParurePrimaryView, self).render_entity_relations(entity)

        self.render_materiaux(entity)
    def render_materiaux(self, entity):
        self.w(u'<table class="listing">\n')
        self.w(u'<thead><tr><th>Matériaux</th><th>acheté</th><th>partagé</th><th>quantité</th><th>usage</th></tr></thead>\n')
        self.w(u'<tbody>\n')
        for mat, achete, partage, quantite, usage in entity.materiaux():
            self.w('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n'%(mat.dc_title(), achete, partage, quantite, usage))
        self.w(u'</tbody></table>\n')


class ParureLinkBox(EntityBoxTemplate):
    __regid__ = 'myosotis.similar_parures'
    __select__ = EntityBoxTemplate.__select__ & is_instance('Parure')
    title = _('Parures similaires')
    context="incontext"
    def cell_call(self, row, col, **kwargs):
        entity = self.cw_rset.get_entity(row, col)
        box = SideBoxWidget(self._cw._(self.title), self.__regid__)
        for label, rql in self._get_links(entity):
            box.append(self.mk_action(label,
                                      self._cw.build_url(rql=rql,
                                                         __force_display=1,
                                                         vid='myosotis.parure_summary')))
        box.render(self.w)

    def _get_links(self, entity):
        url = self._cw.build_url
        same_type = 'Any X WHERE X is Parure, X type T, P type T, P eid %s' % entity.eid
        same_nature = 'Any X WHERE X is Parure, X nature N, P nature N, P eid %s' % entity.eid
        same_carac = 'Any X WHERE X is Parure, X nature N, X caracteristique C, P nature N, P caracteristique C, P eid %s' % (entity.eid)
        links = [(_('Same type Parures'), same_type),
                 (_('Same nature Parures'), same_nature),
                 (_('Same caracteristique Parures'), same_carac)
                 ]
        return links


class MultiParureSummaryView(EntityView):
    __regid__ = 'myosotis.parure_summary'
    __select__ = is_instance('Parure')
    title = _('Parure summary')
    def call(self):

        parures = {}
        for p in self.cw_rset.entities():
            parures.setdefault(p.nature, []).append(p)
        for nature in parures:
            #print 'processing', nature, len(parures[nature])
            self.w(u'<h2>%s</h2>' % nature)
            self.display_parures_table(parures[nature])
    def display_parures_table(self, parures):
        materiaux = {}
        for p in parures:
            for mat, achete, partage, quantite, usage in p.materiaux():
                materiaux.setdefault(mat.long_famille, {}).setdefault(p.eid, []).append((mat, achete, partage, quantite, usage))
        mat_names = sorted(materiaux)
        self.w(u'<table class="listing evenoddcol">')
        self.w(u'<col span="3" class="even" />')
        for i, name in enumerate(mat_names):
            self.w(u'<col span="7" class="%s" />' % ((['odd', 'even'])[i%2]))
        self.w(u'<thead><tr><th colspan="3">Parure</th>')
        for name in mat_names:
            self.w(u'<th colspan="7">%s</th>\n' % name)
        self.w(u'</tr>')
        self.w(u'<tr><th>parure</th><th>carac</th><th>quantite</th>')
        for name in mat_names:
            self.w(u'<th>mat</th><th>coul.</th><th>prov.</th><th>qté</th><th>usage</th><th>Ach?</th><th>Part?</th>\n')
        self.w(u'</tr></thead><tbody>')
        for p in parures:
            self.w(u'<tr>')
            for val in (p.view('listitem'), p.caracteristique, p.quantite()):
                self.w(u'<td>')
                self.w(unicode(val or ''))
                self.w(u'</td>\n')
            for name in mat_names:
                parure_lines = materiaux[name].get(p.eid, [(None, u'', u'', u'', u'')])
                mats, achs, parts, qtes, uses = zip(*parure_lines)
                mat_views = []
                couls = []
                provs = []
                qtes = [q or '' for q in qtes]
                for mat in mats:
                    if mat is None:
                        mat_views.append(u'')
                        couls.append(u'')
                        provs.append(u'')
                    else:
                        mat_views.append(mat.nom or '')
                        couls.append(mat.couleur or '')
                        provs.append(mat.get_provenance() or '')
                for values in mat_views, couls, provs, qtes, uses, achs, parts:
                    self.w(u'<td>')
                    if len(values) > 1:
                        self.wview('pyvallist', pyvalue=values)
                    else:
                        self.w(unicode(values[0]))
                    self.w(u'</td>\n')
            self.w(u'</tr>')
        self.w(u'</tbody></table>')

import xlwt

class ExcelView(EntityView):
    __regid__ = 'excelexport'
    title = _('excel entities export')
    __select__ = is_instance('Parure')
    content_type = "application/vnd.ms-excel"
    templatable = False
    binary = True

    def compute_filename(self):
        return "parure.xls"

    def set_request_content_type(self):
        """overriden to set a .xls filename"""
        self._cw.set_content_type(self.content_type,
                                  filename=self.compute_filename())

    def call(self, written_eid=None, etype_dict=None):
        wb = xlwt.Workbook(encoding='utf-8')
        parures = {}
        for p in self.cw_rset.entities():
            parures.setdefault(p.nature, []).append(p)
        for nature in parures:
            #print 'processing', nature, len(parures[nature])
            sheet = wb.add_sheet(nature)
            self.write_sheet(sheet, parures[nature])
        wb.save(self)


    def write_sheet(self, sheet, parures):
        materiaux = {}
        for p in parures:
            for mat, achete, partage, quantite, usage in p.materiaux():
                materiaux.setdefault(mat.long_famille, {}).setdefault(p.eid, []).append((mat, achete, partage, quantite, usage))
        mat_names = sorted(materiaux)
        self.write_headers(sheet, mat_names)
        entity_row = 2
        for p in parures:
            col = 0
            row_incr = 1
            for val in (p.dc_title(), p.caracteristique, p.quantite()):
                sheet.write(entity_row, col, unicode(val or ''))
                col += 1
            for name in mat_names:
                parure_lines = materiaux[name].get(p.eid, [(None, u'', u'', u'', u'')])
                mats, achs, parts, qtes, uses = zip(*parure_lines)
                mat_views = []
                couls = []
                provs = []
                qtes = [q or '' for q in qtes]
                for mat in mats:
                    if mat is None:
                        mat_views.append(u'')
                        couls.append(u'')
                        provs.append(u'')
                    else:
                        mat_views.append(mat.nom or '')
                        couls.append(mat.couleur or '')
                        provs.append(mat.get_provenance() or '')
                for values in mat_views, couls, provs, qtes, uses, achs, parts:
                    row_incr = max(row_incr, len(values))
                    for i, val in enumerate(values):
                        sheet.write(entity_row+i, col, unicode(values[0]))
                    col += 1
            if row_incr > 1:
                sheet.merge(entity_row, 0, entity_row+row_incr-1, 0)
            entity_row += row_incr

    def write_headers(self, sheet, mat_names):
        headers = [('Parure', ('parure', 'carac', 'quantite'))] + \
                  [(name, ('mat', 'coul', 'prov.', 'qté', 'usage', 'ach?', 'part?')) for name in mat_names]
        col = 0
        for header, subheaders in headers:
            sheet.write(0, col, header)
            #print 0, col, 0, col+len(subheaders)-1
            sheet.merge(0, 0, col, col+len(subheaders)-1)
            for i, subheader in enumerate(subheaders):
                sheet.write(1, i+col, subheader)
            col += len(subheaders)
    
    def write(self, data):
        """
        implement writable interface to be able to pass self to
        Workbook.save()
        """
        self.w(data)
