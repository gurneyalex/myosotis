
import pprint
import codecs

query = 'DELETE P changes C WHERE P is Prix'
rql(query)
commit()

rql('DELETE Change C WHERE NOT EXISTS (C prix_depart P1)')

def find_invalid_changes(logfile_name):
    changes = rql('Any C WHERE C is Change')
    with codecs.open(logfile_name, 'w', 'utf-8') as log:
        for change in changes.entities():
            if not change.is_valid:
                print (u'%s %s' % (change.eid, change.dc_title())).encode('utf-8')
                log.write(u'%s %s\n' % (change.eid, change.dc_title()))

find_invalid_changes('invalid_changes.txt')
print "done finding invalid changes"

target = rql('Any M WHERE M is Monnaie, M nom "g. t. p. p."').get_entity(0, 0)
query = 'Any P ORDERBY P WHERE P is Prix, NOT EXISTS(C prix_depart P), NOT EXISTS (C2 prix_converti P)'
args = {}

#query = 'Any P ORDERBY P WHERE C is Compte, EXISTS(C change CH), T compte C, T achat A, A prix_unitaire P'
result = {}
i = 0
for prix in list(rql(query, args).entities()):
    mode, path = prix.calcule_conversion(target, update=True)
    if mode not in result:
        result[mode] = 1
    else:
        result[mode] += 1
    i += 1
    if i % 500 == 0:
        print
        pprint.pprint(result)
        print
        commit()

print
pprint.pprint(result)
commit()
