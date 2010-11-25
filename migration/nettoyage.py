query = 'SET X type_mesure NULL, X unite NULL, X provenance_mesure NULL WHERE X is %(etype)s, X quantite NULL'
for etype in (u'MateriauxParure', u'FabriqueAvecMat', u'AchatMateriaux',):
    print query % {'etype': etype}
    rql(query, {'etype': etype})



commit()
