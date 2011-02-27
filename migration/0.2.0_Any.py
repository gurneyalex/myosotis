drop_attribute('Personne', 'occupation')
rename_attribute('Compte', 'change', 'change_str')
drop_attribute('Personne', 'maj_occupation')
add_relation_definition('Compte', 'change', 'Change')
add_relation_definition('Transaction', 'change', 'Change')
rql('SET X change Y WHERE X is Compte, Y is Change, Y compte X')
drop_relation_definition('Change', 'compte', 'Compte')
drop_attribute('Change', 'dans_compte')

for etype in ('Personne', 'Compte', 'Transaction'):
    add_attribute(etype, 'base_paradox')

for etype in ('AchatMateriaux', 'AchatPretPorter', 'AchatFabrication'):
    add_attribute(etype, 'remarques')


print "Nettoyage"
query = 'SET X type_mesure NULL, X unite NULL, X provenance_mesure NULL WHERE X is %(etype)s, X quantite NULL'
for etype in (u'MateriauxParure', u'FabriqueAvecMat', u'AchatMateriaux',):
    print query % {'etype': etype}
    rql(query, {'etype': etype})


rql ('DELETE Monnaie M WHERE  NOT P monnaie M')

commit()

sync_schema_props_perms()
#add_cube('simile_timeline')

