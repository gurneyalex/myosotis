drop_attribute('Personne', 'occupation')
rename_attribute('Compte', 'change', 'change_str')
drop_attribute('Personne', 'maj_occupation')
add_relation_definition('Compte', 'change', 'Change')
add_relation_definition('Transaction', 'change', 'Change')
rql('SET X change Y WHERE X is Compte, Y is Change, Y compte X')
drop_relation_definition('Change', 'compte', 'Compte')
drop_attribute('Change', 'dans_compte')

print "Nettoyage"
query = 'SET X type_mesure NULL, X unite NULL, X provenance_mesure NULL WHERE X is %(etype)s, X quantite NULL'
for etype in (u'MateriauxParure', u'FabriqueAvecMat', u'AchatMateriaux',):
    print query % {'etype': etype}
    rql(query, {'etype': etype})



commit()


#add_cube('simile_timeline')

