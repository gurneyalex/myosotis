# -*- coding: utf-8 -*-
"""
Example of use (run this with `cubicweb-ctl shell instance data_import_paradox.py`):
"""


import warnings
warnings.simplefilter('ignore', DeprecationWarning)

from cubicweb.dataimport import *
import datetime
from locale import LC_NUMERIC, setlocale, atof

def date(value):
    return datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S').date()
def annee_date(value):
    return datetime.date(int(value), 1, 1)

setlocale(LC_NUMERIC, 'fr_FR.UTF-8')

CHK = []
GENERATORS = []

errors = []

monnaies = {}

def create_monnaies():
    missing = [u'viennois de Lyon',
               u'viennois de Savoie',
               u'viennois courant de Savoie',
               u'lyonnais',
               u'viennois courant',
               u'tournois',
               u'sterling',
               u'petit tournois bon',
               u'impérial',
               u'viennois courant de la vallée de Suze',
               u"viennois d'Aoste",
               u"viennois du prince",
               u"monnaie du prince",
               u'fort blanc',
               ]
    for name in missing:
        ctl.store.add('Monnaie', {'nom': name, 'type': u'Livre/Sous/Denier'})
    missing_gold = [u"florin d'or de France",
                    u"florin d'or de Florence",
                    u"franc or bon poids",
                    ]
    for name in missing_gold:
        ctl.store.add('Monnaie', {'nom': name,
                                  'type': u'Or'})

def load_monnaies():
    data_file = 'recup/pdox/monnaies.csv'
    reader = ucsvreader_pb(open(data_file), encoding="utf-8",
                           separator=',')
    reader.next()
    pdox2cw = {}
    cw2pdox = {}
    for line in reader:
        cw2pdox.setdefault(line[0], []).append(line[1])
    rset = rql('Any M WHERE M is Monnaie')
    for monnaie in rset.entities():
        pdox = cw2pdox[monnaie.nom]
        for name in pdox:
            pdox2cw[name.lower()] = (monnaie.eid, monnaie.type)
    import pprint
    pprint.pprint(pdox2cw)
    return pdox2cw

def date(value):
    return datetime.datetime.strptime(value, '%d/%m/%Y %H:%M:%S').date()

def qty_float(value):
    if value == "plusieurs":
        return None
    else:
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            print "%r" % value
            raise
def qty_plusieurs(value):
    if value == 'plusieurs':
        return True
    return False

COLUMNS = {'ARTISAN': 'CodeCommande CodePFF CodePersonne Salaire JoursTravail',
           'COMMANDE':'CodeCompte CodeCommande CodePersonne Numero Prix DateOrdre',
           'COMPTE':  'CodeCompte TypeCompte AnneeDebut AnneeFin',
           'DESTPB':  'CodeCommande CodePB CodePersonne',
           'DESTPFA': 'CodeCommande CodePFA CodePersonne',
           'DESTPFF': 'CodeCommande CodePFF CodePersonne',
           'INTRMEDR': 'CodeCommande CodePersonne',
           'MAT':     'CodeMateriaux Matiere Couleur',
           'MATPACH': 'CodeCommande CodePFA CodeMateriaux',
           'MATPFAB': 'CodeCommande CodePFF CodeMateriaux',
           'PBPFAB':  'CodeCommande CodePFF CodeCommandePB CodePB',
           'PBRUT':   'CodeCommande CodePB CodeMateriaux BProvenance '
                      'BLieuAchat BQuantite BPrixUnitaire BPrixGlobal BOccasion',
           'PERSONNE':'CodePersonne Nom Qualite',
           'PFACHETE':'CodeCommande CodePFA AProvenance ANature '
                      'ALieuAchat AQuantite APrixUnitaire APrixGlobal AOccasion',
           'PFFABRIK':'CodeCommande CodePFF FNature FLieuAchat '
                      'FQuantite FPrixUnitaire FPrixGlobal FOccasion',
           'TONDEUR': 'CodeCommande CodePB CodePersonne Salaire JoursTravail',
           'VENDRPB': 'CodeCommande CodePB CodePersonne',
           'VENDRPFA':'CodeCommande CodePFA CodePersonne',
           }


mat_id = {}
MAT = [('nom', 'nom', ()),
       ('couleur', 'couleur', ()),
       ('carac_couleur', 'carac_couleur', ()),
       ('carac_facture', 'carac_facture', ()),
       ('type', 'type', ()),
       ('famille', 'famille', ()),
       ]
def gen_mat(ctl):
    for i, row in enumerate(ctl.iter_and_commit('MAT')):
        entity = mk_entity(row, MAT)
        ctl.store.add('Materiaux', entity)
        mat_id[row['CodeMateriaux']] = entity['eid']
GENERATORS.append((gen_mat, CHK),)

preexisting_personnes = {}
occupations = []
personne_id = {}
PERSONNE = [(u'Identité', 'identite', ()),
            (u'Nom', 'nom', ()),
            #('Qualite', 'titre', ()),
            (u'occupation', 'occupation', (optional,)),
            (u'rattachement', 'rattachement', (optional,)),
            (u'Surnom', 'surnom', (optional,)),
            (u'Diminutif', 'diminutif', (optional,)),
            (u'titre', 'titre', (optional,)),
            (u'sexe', 'sexe', ()),
            ]
def gen_personne(ctl):
    for i, row in enumerate(ctl.iter_and_commit('PERSONNE')):
        read_identite = row[u'Identité'].lower()
        if read_identite in preexisting_personnes:
            personne_id[row['CodePersonne']] = preexisting_personnes[read_identite]
            continue
        entity = mk_entity(row, PERSONNE)
        if not entity['sexe']:
            entity['sexe'] = u'?'
        entity.update({'base_paradox': True})
        if 'occupation' in entity:
            if entity['occupation']:
                occupation = (entity['occupation'], entity.get('rattachement'))
            else:
                occupation = None
            del entity['occupation']
            del entity['rattachement']
        else:
            occupation = None
        ctl.store.add('Personne', entity)
        if occupation is not None:
            occupations.append((entity['eid'],)+occupation)
        personne_id[row['CodePersonne']] = entity['eid']
        preexisting_personnes[entity['identite'].lower()] = entity['eid']
    for eid, valeur, rattachement in occupations:
        occupation = {'valeur': valeur}
        if rattachement:
            occupation['libelle'] = u'identité'
        else:
            occupation['libelle'] = u'occupation'
        entity = ctl.store.add('Occupation', occupation)
        ctl.store.relate(entity['eid'], 'personne', eid)
        if rattachement and 'cnx' in globals():
            if rattachement.lower() not in preexisting_personnes:
                errors.append('preexisting person %s not found (related to %s)' % (rattachement, entity['eid']))
            else:
                ctl.store.relate(entity['eid'], 'rattache_a', preexisting_personnes[rattachement.lower()])
GENERATORS.append((gen_personne, CHK),)


compte_id = {}
COMPTE = [('TypeCompte', 'type_compte', ()),
           ('AnneeDebut', 'debut', (optional, annee_date)),
           ('AnneeFin', 'fin', (optional, annee_date)),
           ]
def gen_compte(ctl):
    for i, row in enumerate(ctl.iter_and_commit('COMPTE')):
        entity = mk_entity(row, COMPTE)
        entity.update({'inventaire': u'compte de %s %s-%s' % (entity['type_compte'], row['AnneeDebut'], row['AnneeFin']),
                       'base_paradox': True})
        ctl.store.add('Compte', entity)
        compte_id[row['CodeCompte']] = entity['eid']
GENERATORS.append((gen_compte, CHK),)

commande_id = {}
commande_info = {}
COMMANDE = [('Numero', 'numero', (int,)),
           ('DateOrdre', 'date_ordre_str', (optional,)),
           ('Prix', 'prix_str', (optional, )),
           ]
def gen_commande(ctl):
    for i, row in enumerate(ctl.iter_and_commit('COMMANDE')):
        if row['CodeCompte'] not in compte_id:
            continue
        entity = mk_entity(row, COMMANDE)
        ctl.store.add('Commande', entity)

        ctl.store.relate(entity['eid'], 'compte', compte_id[row['CodeCompte']])
        commande_info[row['CodeCommande']] = (personne_id.get(row['CodePersonne']),
                                              compte_id[row['CodeCompte']])
        commande_id[row['CodeCommande']] = entity['eid']
GENERATORS.append((gen_commande, CHK),)

def make_prix(prix, monnaie):
    if not (prix and monnaie):
        return None
    values = [float(a.replace(',', '.')) for a in prix.split()]
    #print "%r" % monnaie
    monnaie_eid, monnaie_type = monnaies.get(monnaie.lower(), (0, 'Livre/Sous/Denier'))
    if not monnaie_eid:
        errors.append('unkown monnaie %r' % monnaie)
        raise ValueError('unknown monnaie %s' % monnaie)
        if  'florin' in monnaie.lower():
            monnaie_type = 'Florin/Gros'
        elif ' or' in monnaie.lower():
            monnaie_type = 'Or'
    if monnaie_type == 'Livre/Sous/Denier':
        assert len(values) == 3, '%s: %s' % (monnaie, values)
        entity = dict(livres=values[0], sous=values[1], deniers=values[2],
                      monnaie=monnaie_eid)
    elif monnaie_type == 'Florin/Gros':
        assert len(values) in (1,2), '%s: %s' % (monnaie, values)
        if len(values) == 1:
            values.append(0)
        entity = dict(florins=values[0], gros=values[1], monnaie=monnaie_eid)
    elif monnaie_type == 'Or':
        assert len(values) == 1, '%s: %s' % (monnaie, values)
        entity = dict(monnaie_or=values[0], monnaie=monnaie_eid)
    else:
        raise ValueError(monnaie_type)
    return entity

transaction_id = {}
commande_transactions = {}
pbrut_id = {}
PBRUT = [(u'unité', 'unite', (optional,)),
         (u'quantité', 'quantite', (optional, qty_float)),
         (u'quantité', 'quantite_plusieurs', (qty_plusieurs,)),
         ]
def gen_pbrut(ctl):
    for i, row in enumerate(ctl.iter_and_commit('PBRUT')):
        if row['CodeCommande'] not in commande_id:
            continue
        entity = mk_entity(row, PBRUT)
        remarks = [u'Provenance Materiaux: %s'%row['BProvenance'],
                   u'LieuAchat: %s' % row['BLieuAchat'],
                   u'Occasion: %s' % row['BOccasion'],
                   u'\n',
                   u'Quantite: %s' % row['BQuantite'],
                   u'PrixUnitaire: %s' % row['BPrixUnitaire'],
                   u'PrixGlobal: %s' % row['BPrixGlobal'],
                   ]
        entity['remarques'] = u'\n\n'.join(remarks)
        ctl.store.add('AchatMateriaux', entity)
        try:
            prix_unitaire = make_prix(row['prix unitaire'], row['monnaie prix unitaire'])
        except ValueError, exc:
            print repr(exc)
            continue
        if prix_unitaire is not None:
            ctl.store.add('Prix', prix_unitaire)
            ctl.store.relate(entity['eid'], 'prix_unitaire', prix_unitaire['eid'])
        try:
            prix_global = make_prix(row['prix global'], row['monnaie prix global'])
        except ValueError, exc:
            print repr(exc)
            continue
        if prix_global is not None:
            #print prix_global
            ctl.store.add('Prix', prix_global)
            ctl.store.relate(entity['eid'], 'prix_total', prix_global['eid'])
        transaction = {'base_paradox': True}
        ctl.store.add('Transaction', transaction)
        ctl.store.relate(commande_id[row['CodeCommande']], 'transactions', transaction['eid'])
        commanditaire, compte = commande_info[row['CodeCommande']]
        ctl.store.relate(transaction['eid'], 'compte', compte)
        if commanditaire:
            commanditaire_data = {'commandement': True}
            ctl.store.add('Intervenant', commanditaire_data)
            ctl.store.relate(transaction['eid'], 'intervenants', commanditaire_data['eid'])
            ctl.store.relate(commanditaire_data['eid'], 'intervenant', commanditaire)
        ctl.store.relate(transaction['eid'], 'achat', entity['eid'])
        ctl.store.relate(entity['eid'], 'materiaux', mat_id[row['CodeMateriaux']])
        transaction_id[('pb', row['CodePB'])] = transaction['eid']
        commande_transactions.setdefault(row['CodeCommande'], []).append(transaction['eid'])
        pbrut_id[row['CodePB']] = entity['eid']
GENERATORS.append((gen_pbrut, CHK),)


pfachete_id = {}
pfachete_parure = {}
PFACHETE = [
         (u'quantite', 'quantite', (optional, qty_float)),
         (u'quantite', 'quantite_plusieurs', (qty_plusieurs,)),
    ]
def gen_pfachete(ctl):
    for i, row in enumerate(ctl.iter_and_commit('PFACHETE')):
        if row['CodeCommande'] not in commande_id:
            continue
        parure = {'type': row['Type Parure'],
                  'nature': row['Nature Parure'],
                  'caracteristique': row['Carac Parure'],
                  }
        ctl.store.add('Parure', parure)
        entity = mk_entity(row, PFACHETE)
        remarks = [u'LieuAchat: %s' % row['ALieuAchat'],
                   u'Quantite: %s' % row['AQuantite'],
                   u'PrixUnitaire: %s' % row['APrixUnitaire'],
                   u'PrixGlobal: %s' % row['APrixGlobal'],
                   u'Occasion: %s' % row['AOccasion'],
                   ]
        entity['remarques'] = u'\n\n'.join(remarks)
        ctl.store.add('AchatPretPorter', entity)
        try:
            prix_unitaire = make_prix(row['prix unitaire'], row['monnaie prix unitaire'])
        except ValueError, exc:
            print repr(exc)
            continue
        if prix_unitaire is not None:
            ctl.store.add('Prix', prix_unitaire)
            ctl.store.relate(entity['eid'], 'prix_unitaire', prix_unitaire['eid'])
        try:
            prix_global = make_prix(row['prix global'], row['monnaie prix global'])
        except ValueError, exc:
            print repr(exc)
            continue
        if prix_global is not None:
            #print prix_global
            ctl.store.add('Prix', prix_global)
            ctl.store.relate(entity['eid'], 'prix_total', prix_global['eid'])
        transaction = {'base_paradox': True}
        ctl.store.add('Transaction', transaction)
        ctl.store.relate(commande_id[row['CodeCommande']], 'transactions', transaction['eid'])
        commanditaire, compte = commande_info[row['CodeCommande']]
        ctl.store.relate(transaction['eid'], 'compte', compte)
        if commanditaire:
            commanditaire_data = {'commandement': True}
            ctl.store.add('Intervenant', commanditaire_data)
            ctl.store.relate(transaction['eid'], 'intervenants', commanditaire_data['eid'])
            ctl.store.relate(commanditaire_data['eid'], 'intervenant', commanditaire)
        ctl.store.relate(transaction['eid'], 'achat', entity['eid'])
        ctl.store.relate(entity['eid'], 'parure', parure['eid'])
        pfachete_id[row['CodePFA']] = entity['eid']
        transaction_id[('pfa', row['CodePFA'])] = transaction['eid']
        commande_transactions.setdefault(row['CodeCommande'], []).append(transaction['eid'])
        pfachete_parure[row['CodePFA']] = parure['eid']
GENERATORS.append((gen_pfachete, CHK),)

pffabrik_id = {}
pffabrik_parure = {}
PFFABRIK = [
         (u'quantite', 'quantite', (optional, qty_float)),
         (u'quantite', 'quantite_plusieurs', (qty_plusieurs,)),
    ]
def gen_pffabrik(ctl):
    for i, row in enumerate(ctl.iter_and_commit('PFFABRIK')):
        if row['CodeCommande'] not in commande_id:
            continue
        parure = {'type': u'???',
                  'nature': row['FNature']}
        ctl.store.add('Parure', parure)
        entity = mk_entity(row, PFFABRIK)
        remarks = [u'LieuAchat: %s' % row['FLieuAchat'],
                   u'Quantite: %s' % row['FQuantite'],
                   u'PrixUnitaire: %s' % row['FPrixUnitaire'],
                   u'PrixGlobal: %s' % row['FPrixGlobal'],
                   u'Occasion: %s' % row['FOccasion'],
                   ]
        entity['remarques'] = u'\n\n'.join(remarks)
        ctl.store.add('AchatFabrication', entity)
        try:
            prix_unitaire = make_prix(row['prix unitaire'], row['monnaie prix unitaire'])
        except ValueError, exc:
            print repr(exc)
            continue
        if prix_unitaire is not None:
            ctl.store.add('Prix', prix_unitaire)
            ctl.store.relate(entity['eid'], 'prix_unitaire', prix_unitaire['eid'])
        try:
            prix_global = make_prix(row['prix global'], row['monnaie prix global'])
        except ValueError, exc:
            print repr(exc)
            continue
        if prix_global is not None:
            #print prix_global
            ctl.store.add('Prix', prix_global)
            ctl.store.relate(entity['eid'], 'prix_total', prix_global['eid'])
        transaction = {'base_paradox': True}
        ctl.store.add('Transaction', transaction)
        ctl.store.relate(commande_id[row['CodeCommande']], 'transactions', transaction['eid'])
        commanditaire, compte = commande_info[row['CodeCommande']]
        ctl.store.relate(transaction['eid'], 'compte', compte)
        if commanditaire:
            commanditaire_data = {'commandement': True}
            ctl.store.add('Intervenant', commanditaire_data)
            ctl.store.relate(transaction['eid'], 'intervenants', commanditaire_data['eid'])
            ctl.store.relate(commanditaire_data['eid'], 'intervenant', commanditaire)
        ctl.store.relate(transaction['eid'], 'achat', entity['eid'])
        ctl.store.relate(entity['eid'], 'parure', parure['eid'])
        pffabrik_id[row['CodePFF']] = entity['eid']
        transaction_id[('pff', row['CodePFF'])] = transaction['eid']
        commande_transactions.setdefault(row['CodeCommande'], []).append(transaction['eid'])
        pffabrik_parure[row['CodePFF']] = parure['eid']
GENERATORS.append((gen_pffabrik, CHK),)


DESTPB = []
def gen_destpb(ctl):
    for i, row in enumerate(ctl.iter_and_commit('DESTPB')):
        if ('pb',row['CodePB']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = mk_entity(row, DESTPB)
        entity['nombre'] = u'1'
        ctl.store.add('Destinataire', entity)
        ctl.store.relate(entity['eid'], 'destinataire', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pb',row['CodePB'])], 'destinataires', entity['eid'])
GENERATORS.append((gen_destpb, CHK),)

DESTPFA = []
def gen_destpfa(ctl):
    for i, row in enumerate(ctl.iter_and_commit('DESTPFA')):
        if ('pfa',row['CodePFA']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = mk_entity(row, DESTPFA)
        entity['nombre'] = u'1'
        ctl.store.add('Destinataire', entity)
        ctl.store.relate(entity['eid'], 'destinataire', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pfa', row['CodePFA'])], 'destinataires', entity['eid'])
GENERATORS.append((gen_destpfa, CHK),)

def gen_destpff(ctl):
    for i, row in enumerate(ctl.iter_and_commit('DESTPFF')):
        if ('pff',row['CodePFF']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = {}
        entity['nombre'] = u'1'
        ctl.store.add('Destinataire', entity)
        ctl.store.relate(entity['eid'], 'destinataire', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pff', row['CodePFF'])], 'destinataires', entity['eid'])
GENERATORS.append((gen_destpff, CHK),)



intrmdr_id = {}
def gen_intrmdr(ctl):
    for i, row in enumerate(ctl.iter_and_commit('INTRMEDR')):
        if row['CodeCommande'] not in commande_id or row['CodePersonne'] not in personne_id:
            continue
        for transaction in commande_transactions.get(row['CodeCommande'], ()):
            entity = {}
            ctl.store.add('Intervenant', entity)
            ctl.store.relate(entity['eid'], 'intervenant', personne_id[row['CodePersonne']])
            ctl.store.relate(transaction, 'intervenants', entity['eid'])
GENERATORS.append((gen_intrmdr, CHK),)

def gen_vendrpb(ctl):
    for i, row in enumerate(ctl.iter_and_commit('VENDRPB')):
        if ('pb',row['CodePB']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = {}
        ctl.store.add('Vendeur', entity)
        ctl.store.relate(entity['eid'], 'vendeur', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pb', row['CodePB'])], 'vendeurs', entity['eid'])
GENERATORS.append((gen_vendrpb, CHK),)

def gen_vendrpfa(ctl):
    for i, row in enumerate(ctl.iter_and_commit('VENDRPFA')):
        if ('pfa',row['CodePFA']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = {}
        ctl.store.add('Vendeur', entity)
        ctl.store.relate(entity['eid'], 'vendeur', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pfa', row['CodePFA'])], 'vendeurs', entity['eid'])
GENERATORS.append((gen_vendrpfa, CHK),)


artisan_id = {}
ARTISAN = [('JoursTravail', 'duree', (optional, int)),
           ('Salaire', 'remarques', ()),
           ]
def gen_artisan(ctl):
    for i, row in enumerate(ctl.iter_and_commit('ARTISAN')):
        if ('pff',row['CodePFF']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = mk_entity(row, ARTISAN)
        if not entity['duree']:
            del entity['duree']
        #print entity
        entity.update({'tache': u'fabrication %s' % pffabrik_id[row['CodePFF']]})
        ctl.store.add('Travail', entity)
        ctl.store.relate(entity['eid'], 'artisan', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pff', row['CodePFF'])], 'travaux', entity['eid'])
GENERATORS.append((gen_artisan, CHK),)

def gen_tondeur(ctl):
    for i, row in enumerate(ctl.iter_and_commit('TONDEUR')):
        if ('pb',row['CodePB']) not in transaction_id or row['CodePersonne'] not in personne_id:
            continue
        entity = {'remarques': u'Salaire: %s\n\nJours travail:%s'%(row['Salaire'], row['JoursTravail']),
                  'tache': 'tonte de %s' % pbrut_id.get('CodePB', u'?')}
        ctl.store.add('Travail', entity)
        ctl.store.relate(entity['eid'], 'artisan', personne_id[row['CodePersonne']])
        ctl.store.relate(transaction_id[('pb', row['CodePB'])], 'travaux', entity['eid'])
GENERATORS.append((gen_tondeur, CHK),)

def gen_matpach(ctl):
    for i, row in enumerate(ctl.iter_and_commit('MATPACH')):
        entity = {}
        ctl.store.add('MateriauxParure', entity)
        parure_id = pffabrik_parure[row['CodePFA']]
        ctl.store.relate(entity['eid'], 'materiaux', mat_id[row['CodeMateriaux']])
        ctl.store.relate(parure_id, 'composee_de', entity['eid'])
GENERATORS.append((gen_matpach, CHK),)

def gen_matpfab(ctl):
    for i, row in enumerate(ctl.iter_and_commit('MATPFAB')):
        entity = {}
        ctl.store.add('MateriauxParure', entity)
        parure_id = pffabrik_parure[row['CodePFF']]
        ctl.store.relate(entity['eid'], 'materiaux', mat_id[row['CodeMateriaux']])
        ctl.store.relate(parure_id, 'composee_de', entity['eid'])
GENERATORS.append((gen_matpfab, CHK),)

def gen_pbpfab(ctl):
    for i, row in enumerate(ctl.iter_and_commit('PBPFAB')):
        if row['CodePFF'] not in pffabrik_id or row['CodePB'] not in pbrut_id:
            continue
        entity = {}
        ctl.store.add('FabriqueAvecMat', entity)
        ctl.store.relate(entity['eid'], 'achat_matiere', pbrut_id[row['CodePB']])
        ctl.store.relate(pffabrik_id[row['CodePFF']], 'avec_mat', entity['eid'])
GENERATORS.append((gen_pbpfab, CHK),)



if 'cnx' in locals():
    ctl = CWImportController(RQLObjectStore(cnx), askerror=0, catcherrors=None, commitevery=1000)
else:
    ctl = CWImportController(ObjectStore())
ctl.generators = GENERATORS

if 'cnx' in locals():
    rset = rql('Any P WHERE P is Personne')
    for person in rset.entities():
        preexisting_personnes[person.identite.lower()] = person.eid
    create_monnaies()
    monnaies = load_monnaies()

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
               'DESTPFF',
               'INTRMEDR',
               'MATPACH',
               'MATPFAB',
               'PBPFAB',
               'TONDEUR',
               'VENDRPB',
               'VENDRPFA',
               ]
#XXX monnaies.csv
separators = {'MAT': ',', 'PBRUT': ',', 'PERSONNE': ',', 'PFACHETE': ',', 'PFFABRIK': ',',
              'monnaies': ',', }

for data_name in datasources:
    data_file = 'recup/pdox/'+data_name+'.TXT'
    ctl.data[data_name] = lazytable(ucsvreader_pb(open(data_file), encoding="utf-8",
                                                  separator=separators.get(data_name, ";")))


ctl.run()
import codecs
f = codecs.open('data_import_paradox.errors', 'w', encoding='utf-8')
for error in errors:
    print repr(error)
    f.write(error)
    f.write('\n')
f.close()
print '\n%d errors.' % len(errors)

if 'cnx' in locals():
    for c in rql('Commande C').entities(0):
        rql('SET T pagination %(p)s WHERE C eid %(e)s, C transactions T', {'e': c.eid, 'p': u'item %d'%c.numero})
    commit()
sys.exit(0)
