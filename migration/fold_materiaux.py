rset = rql('Any X WHERE X is Materiaux')

materiaux = {}

for i, mat in enumerate(rset.entities()):
    print i, len(materiaux)
    if mat.provenance:
        prov = mat.provenance[0].eid
    else:
        prov = None
    attrs = mat.nom, mat.type, mat.famille, mat.couleur, mat.carac_couleur, mat.carac_facture, prov

    materiaux.setdefault(attrs, []).append(mat)

print len(materiaux)
print sorted(len(m) for m in materiaux.itervalues())

for mat_attrs, mats in materiaux.iteritems():
    if len(mats) == 1:
        continue
    print "processing", mat_attrs
    refmat = mats[0]
    for mat in mats[1:]:
        for related in mat.reverse_materiaux:
            print "relinking %s to %s" % (related, mat)
            related.set_relations(materiaux=refmat)
        mat.cw_delete()

commit()

