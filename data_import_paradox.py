# -*- coding: utf-8 -*-
"""
Example of use (run this with `cubicweb-ctl shell instance data_import_paradox.py`):
"""
from cubicweb.dataimport import *
import datetime
from locale import LC_NUMERIC, setlocale, atof

def date(value):
    return datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S').date()

setlocale(LC_NUMERIC, 'fr_FR.UTF-8')

CHK = []
GENERATORS = []

errors = []

def date(value):
    return datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S').date()


def monnaie_type(value):
    if value == '1':
        return u"Livre/Sous/Denier"
    elif value == '2':
        return u'Florin/Gros'
    elif value == '3':
        return u'Or'
    else:
        raise ValueError(value)


compte_id = {}
COMPTE = [('TypeCompte', 'type_compte', ()),
           ('Inventaire', 'inventaire', ()),
           ('AnneeDebut', 'debut', (optional, date)),
           ('AnneFin', 'fin', (optional, date)),
           ]
def gen_compte(ctl):
    for i, row in enumerate(ctl.iter_and_commit('COMPTE')):
        entity = mk_entity(row, COMPTE)
        entity.update({'inventaire': u'cf. maitrise',
                       'base_paradox': True})
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_compte, CHK),)


artisan_id = {}
ARTISAN = [('JoursTravail', 'duree', (optional, int)),
           ('Salaire', 'remarques', ()),
           ]
def gen_artisan(ctl):
    for i, row in enumerate(ctl.iter_and_commit('ARTISAN')):
        entity = mk_entity(row, ARTISAN)
        print entity
        entity.update({'nature': u'fabrication %s' % achat_fabrication_id[row['CodePFF']]})
        ctl.store.add('Travail', entity)
        ctl.store.relate(entity[eid], 'artisan', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[row['CodeCommande']], 'travaux', entity[eid])
GENERATORS.append((gen_artisan, CHK),)

transaction_id = {}
COMMANDE = [('DateOrdre', 'date_ordre', ()),
            ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)
xxx_id = {}
XXX = [('Col', 'attr', ()),
       ]
def gen_xxx(ctl):
    for i, row in enumerate(ctl.iter_and_commit('XXX')):
        entity = mk_entity(row, COMPTE)
        print entity
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_xxx, CHK),)


# create controller
if 'cnx' in locals():
    ctl = CWImportController(RQLObjectStore(cnx), askerror=True, commitevery=1000)
else:
    ctl = CWImportController(ObjectStore())
ctl.generators = GENERATORS



datasources = ['COMPTE',
               'PERSONNE',
               'COMMANDE',
               'ARTISAN',
               'MAT',
               'PBRUT',
               'PFACHETE',
               'PFFABRIK',
               'DESTPB',
               'DESTPFA',
               'INTRMEDR',
               'MATPACH',
               'MATPFAB',
               'PBPFAB',
               'TONDEUR',
               'VENDRPB',
               'VENDRPFA',
               ]
for data_name, data_file in datasources:
    data_file = 'recup/'+data_file+'.csv'
    ctl.data[data_name] = lazytable(ucsvreader_pb(open(data_file), encoding="cp1252", separator=";"))
# run
ctl.run()
import codecs
f = codecs.open('data_import.errors', 'w', encoding='utf-8')
for error in errors:
    print error
    f.write(error)
    f.write('\n')
f.close()
print '\n%d errors.' % len(errors)
sys.exit(0)
