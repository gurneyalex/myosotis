# -*- coding: utf-8 -*-
"""
Example of use (run this with `cubicweb-ctl shell instance import-script.py`):
"""
from cubicweb.dataimport import *
import datetime
from locale import LC_NUMERIC, setlocale, atof

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
           ('Debut', 'debut', (optional, date)),
           ('Fin', 'fin', ()),
           ('Change', 'change', ()),
           ]
def gen_compte(ctl):
    for i, row in enumerate(ctl.iter_and_commit('compte')):
        entity = mk_entity(row, COMPTE)
        ctl.store.add('Compte', entity)
        compte_id[row['Inventaire']] = entity['eid']
GENERATORS.append((gen_compte, CHK),)

lieu_id = {}
lieu_ville_id = {}
LIEU = [('Ville', 'ville', ()),
        ('Region', 'region', ()),
        ('Remarques', 'remarques', ()),
        ]

def gen_lieu(ctl):
    for i, row in enumerate(ctl.iter_and_commit('lieu')):
        entity = mk_entity(row, LIEU)
        ctl.store.add('Lieu', entity)
        lieu_id[(row['Ville'].lower(), row['Region'].lower())] = entity['eid']
        lieu_ville_id[row['Ville']] = entity['eid']
GENERATORS.append((gen_lieu, CHK))


monnaie_id = {}
MONNAIE = [("Nom", "nom", ()),
           ("type", "type", (monnaie_type,)),
           ]
def gen_monnaie(ctl):
    for i, row in enumerate(ctl.iter_and_commit('monnaie')):
        entity = mk_entity(row, MONNAIE)
        ctl.store.add('Monnaie', entity)
        monnaie_id[row['Nom']] = entity['eid']
GENERATORS.append((gen_monnaie, CHK))

personne_id = {}
PERSONNE = [("identite", "identite", ()),
            ("Nom", "nom", ()),
            ('Surnom', 'surnom',()),
            ('Diminutif', 'diminutif', ()),
            ('Occupation', 'occupation', ()),
            ('Titre', 'titre', ()),
            ('Sexe', 'sexe', ()),
            ('Remarques', 'remarques',()),
            ('MaJ_occupations', 'maj_occupation', (int, bool,)),
            ('Rattachement', 'rattachement', ()),
            ('VilleDomicile', 'ville_domicile', ()),
            ('VilleOrigine', 'ville_origine', ()),
            ]
def gen_personne(ctl):
    for i, row in enumerate(ctl.iter_and_commit('personne')):
        entity = mk_entity(row, PERSONNE)
        ctl.store.add('Personne', entity)
        personne_id[row['Id']] = entity['eid']
        if row['VilleDomicile']  and row['VilleDomicile'] in lieu_ville_id:
            ctl.store.relate(entity['eid'], 'lieu_domicile', lieu_ville_id[row['VilleDomicile']])
        if  row['VilleOrigine']  and row['VilleOrigine'] in lieu_ville_id:
            ctl.store.relate(entity['eid'], 'lieu_origine', lieu_ville_id[row['VilleOrigine']])
GENERATORS.append((gen_personne, CHK))

materiaux_id = {}
MATERIAUX = [("Type", "type", ()),
           ("Famille", "famille", ()),
             ('Nom', 'nom', ()),
             ('Couleur', 'couleur', ()),
             ('CaracCouleur', 'carac_couleur', ()),
             ('CaracFacture', 'carac_facture', ()),

           ]
def gen_materiaux(ctl):
    for i, row in enumerate(ctl.iter_and_commit('materiaux')):
        entity = mk_entity(row, MATERIAUX)
        ctl.store.add('Materiaux', entity)
        materiaux_id[row['Id']] = entity['eid']
        try:
            ctl.store.relate(entity['eid'], 'provenance', lieu_id[(row['Ville'].lower(), row['Region'].lower())])
        except KeyError:
            if row['Ville'] or row['Region']:
                errors.append('line %d: ' %(i+1) + 'Materiaux %s missing provenance %r %r' % (entity['eid'], row['Ville'], row['Region']))
                             
GENERATORS.append((gen_materiaux, CHK))

prix_id = {}
PRIX = [("Livres", "livres", (optional, int,)),
        ("Sous", "sous", (optional, int,)),
        ('Deniers', 'deniers', (optional, atof,)),
        ('Florins', 'florins', (optional, atof,)),
        ('Gros', 'gros', (optional, atof,)),
        ('sous_florin', 'sous_florins', (optional, int,)),
        ('denier_florin', 'denier_florins', (optional, atof,)),
        ('MonnaieOr', 'monnaie_or', (optional, atof,)),
        ('Conversion', 'conversion', (optional, atof,))
           ]
def gen_prix(ctl):
    for i, row in enumerate(ctl.iter_and_commit('prix')):
        entity = mk_entity(row, PRIX)
        ctl.store.add('Prix', entity)
        prix_id[row['Id']] = entity['eid']
        ctl.store.relate(entity['eid'], 'monnaie', monnaie_id[row['Monnaie']])
GENERATORS.append((gen_prix, CHK))

change_id = {}
CHANGE = [('compte', 'dans_compte', ())]
def gen_change(ctl):
    for i, row in enumerate(ctl.iter_and_commit('change')):
        if row['Prix1'] and row['Prix2']:
            entity = mk_entity(row, CHANGE)
            ctl.store.add('Change', entity)
            change_id[row['IdChange']] = entity['eid']
            ctl.store.relate(entity['eid'], "prix_depart", prix_id[row['Prix1']])
            ctl.store.relate(entity['eid'], "prix_converti", prix_id[row['Prix2']])
            ctl.store.relate(entity['eid'], "compte", compte_id[row['compte']])
        else:
            errors.append("pas d'info change pour Id %s" % row['IdChange'])
GENERATORS.append((gen_change, CHK))

occupation_id = {}
OCCUPATION = [("libelle", "libelle", ()),
        ("valeur", "valeur", ()),
        ('Pagination', 'pagination', ()),
        ('Occupation', 'occupation', ()),
           ]
def gen_occupation(ctl):
    for i, row in enumerate(ctl.iter_and_commit('occupation')):
        entity = mk_entity(row, OCCUPATION)
        ctl.store.add('Occupation', entity)
        occupation_id[row['Id']] = entity['eid']
        ctl.store.relate(entity['eid'], 'compte', compte_id[row['Compte']])
        if row['PersonneId'] in personne_id:
            ctl.store.relate(entity['eid'], 'personne', personne_id[row['PersonneId']])
        else:
            errors.append('line %d: ' %(i+1) + 'MOccupation personne manquante id %s' % row['PersonneId'])
        if row['PersonneRattachement']:
            ctl.store.relate(entity['eid'], 'rattache_a', personne_id[row['PersonneRattachement']])
GENERATORS.append((gen_occupation, CHK))

occasion_id = {}
OCCASION = [("Type", "type", ()),
        ("DateEvenement", "date", (optional, date)),
        ('Remarques', 'remarques', ()),
           ]
occasion_lieu={}
def gen_occasion(ctl):
    for i, row in enumerate(ctl.iter_and_commit('occasion')):
        entity = mk_entity(row, OCCASION)
        ctl.store.add('Occasion', entity)
        occasion_id[row['Id']] = entity['eid']
        if row['ville'] and row['region']:
            ctl.store.relate(entity["eid"], 'lieu', lieu_id[(row['ville'].lower(), row['region'].lower())])
GENERATORS.append((gen_occasion, CHK))

parure_id = {}
PARURE = [("Type", "type", ()),
          ("Nature", "nature", ()),
          ('Caracteristique', 'caracteristique', ()),
          ]
def gen_parure(ctl):
    for i, row in enumerate(ctl.iter_and_commit('parure')):
        entity = mk_entity(row, PARURE)
        ctl.store.add('Parure', entity)
        parure_id[row['Id']] = entity['eid']
GENERATORS.append((gen_parure, CHK))

materiauxparure_id = {}
MATERIAUXPARURE = [("TypeMesure", "type_mesure", ()),
                   ("Quantite", "quantite", (optional, atof,)),
                   ('Unite', 'unite', ()),
                   ('provenance_mesure', 'provenance_mesure', ()),
                   ('Conversion', 'conversion', (optional, atof,)),
                   ('Materiaux_Achete', 'materiaux_achete', (int, bool,)),
                   ('usage', 'usage', ()),
                   ]
def gen_materiauxparure(ctl):
    for i, row in enumerate(ctl.iter_and_commit('materiauxparure')):
        if row['Materiaux'] in materiaux_id and row['Parure'] in parure_id:
            entity = mk_entity(row, MATERIAUXPARURE)
            ctl.store.add('MateriauxParure', entity)
            materiauxparure_id[(row['Parure'], row['Materiaux'])] = entity['eid']
            ctl.store.relate(entity['eid'], 'materiaux', materiaux_id[row['Materiaux']])
            ctl.store.relate(parure_id[row['Parure']], 'composee_de', entity['eid'])
        if row['Materiaux'] not in materiaux_id:
            errors.append('line %d: ' %(i+1) + 'MateriauxParure: missing materiaux %s' % row['Materiaux'])
        if row['Parure'] not in parure_id:
            errors.append('line %d: ' %(i+1) + 'MateriauxParure: missing parure %s' % row['Parure'])

GENERATORS.append((gen_materiauxparure, CHK))

transaction_id = {}
TRANSACTION = [("Date", "date", (optional, date)),
               ("Remarques", "remarques", ()),
               ('typeAchat', 'type_achat', ()),
               ('pagination', 'pagination', ()),
               ('date_ordre', 'date_ordre', (optional, date)),
               ('date_recette', 'date_recette', (optional, date)),
               ('prix_partage', 'prix_partage', (int, bool,)),
          ]

def gen_transaction(ctl):
    for i, row in enumerate(ctl.iter_and_commit('transaction')):
        entity = mk_entity(row, TRANSACTION)
        ctl.store.add('Transaction', entity)
        eid = entity['eid']
        transaction_id[row['numTrans']] = eid
        ctl.store.relate(eid, 'compte', compte_id[row['compte']])
        if row['Prix_Ensemble']:
            try:
                ctl.store.relate(eid, 'prix_ensemble', prix_id[row['Prix_Ensemble']])
            except KeyError:
                errors.append('line %d: ' %(i+1) + 'transaction %s prix_ensemble %s' % (row['numTrans'], row['Prix_Ensemble']))

        if row['Ville']:
            ctl.store.relate(eid, 'lieu',
                             lieu_id[(row['Ville'].lower(), row['Region'].lower())])
        if row['Occasion']:
            ctl.store.relate(eid, 'occasion', occasion_id[row['Occasion']])


GENERATORS.append((gen_transaction, CHK))

destinataire_id = {}
DESTINATAIRE = [("Nombre", "nombre", ()),
           ]
def gen_destinataire(ctl):
    for i, row in enumerate(ctl.iter_and_commit('destinataire')):
        entity = mk_entity(row, DESTINATAIRE)
        ctl.store.add('Destinataire', entity)
        try:
            ctl.store.relate(entity['eid'], 'destinataire', personne_id[row['Personne']])
        except KeyError:
            errors.append('line %d: ' %(i+1) + 'Destinataires eid %s missing Personne %s'%(entity['eid'], row['Personne']))
        try:
            ctl.store.relate(transaction_id[row['numTrans']], 'destinataires', entity['eid'])
        except KeyError:
            errors.append('line %d: ' %(i+1) + 'Destinataires eid %s missing Transaction %s'%(entity['eid'], row['numTrans']))
GENERATORS.append((gen_destinataire, CHK))

vendeur_id = {}
VENDEUR = [("Expression", "expression", ()),
           ]
def gen_vendeur(ctl):
    for i, row in enumerate(ctl.iter_and_commit('vendeur')):
        if row['Personne'] in personne_id and row['numTrans'] in transaction_id:
            entity = mk_entity(row, VENDEUR)
            ctl.store.add('Vendeur', entity)
            ctl.store.relate(entity['eid'], 'vendeur', personne_id[row['Personne']])
            ctl.store.relate(transaction_id[row['numTrans']], 'vendeurs', entity['eid'])
        if row['Personne'] not in personne_id:
            errors.append('line %d: ' %(i+1) + 'Vendeur missing Personne %s'%(row['Personne']))
        if  row['numTrans'] not in transaction_id:
            errors.append('line %d: ' %(i+1) + 'Vendeur missing Transaction %s'%(row['numTrans']))
GENERATORS.append((gen_vendeur, CHK))

travail_id = {}
TRAVAIL = [("SalaireNatureQt", "salaire_nature_qt", (optional, int,)),
           ('SalaireNatureObj', 'salaire_nature_obj', ()),
           ('NombreAides', 'nombre_aides', (optional, int,)),
           ('DesignationAides', 'designation_aides', ()),
           ('Tache', 'tache', ()),
           ('Duree', 'duree', (optional, int,)),
           ('DateTravaille', 'date_travail', (optional, date)),
           ('Remarques', 'remarques', ()),
           ('Facon_et_etoffe', 'facon_et_etoffe', (int, bool,))
           ]
def gen_travail(ctl):
    for i, row in enumerate(ctl.iter_and_commit('travail')):
        if row['Personne'] in personne_id:
            entity = mk_entity(row, TRAVAIL)
            ctl.store.add('Travail', entity)
            travail_id[row['idTravaille']] = entity['eid']
            ctl.store.relate(entity['eid'], 'artisan', personne_id[row['Personne']])
            try:
                ctl.store.relate(entity['eid'], 'salaire_argent', prix_id[row['SalaireArgent']])
            except KeyError:
                if row['SalaireArgent']:
                    errors.append('line %d: ' %(i+1) + 'Travail eid %s missing Prix (salaire_argent) %s'%(entity['eid'], row['SalaireArgent']))

            try:
                ctl.store.relate(entity['eid'], 'salaire_aides', prix_id[row['SalaireAides']])
            except KeyError:
                if row['SalaireAides']:
                    errors.append('line %d: ' %(i+1) + 'Travail eid %s missing Prix (salaire_aides) %s'%(entity['eid'], row['SalaireAides']))
        else:
            errors.append('line %d: ' %(i+1) + 'Travail eid %s missing Personne %s'%(entity['eid'], row['Personne']))

GENERATORS.append((gen_travail, CHK))

def gen_ltravail(ctl):
    for i, row in enumerate(ctl.iter_and_commit('ltravail')):
        if row['idTravaille'] not in travail_id:
            errors.append('line %d: ' %(i+1) + 'MLTravail missing Travail  %s'%(row['idTravaille']))
        elif row['numTrans'] not in transaction_id:
            errors.append('line %d: ' %(i+1) + 'MLTravail missing Transaction %s'%(row['numTrans']))
        else:
            ctl.store.relate(transaction_id[row['numTrans']], 'travaux', travail_id[row['idTravaille']])

GENERATORS.append((gen_ltravail, CHK))

def gen_receveur(ctl):
    for i, row in enumerate(ctl.iter_and_commit('receveur')):
        ctl.store.relate(compte_id[row['Compte']], 'receveur', personne_id[row['Personne']])
GENERATORS.append((gen_receveur, CHK))


intervenant_id = {}
INTERVENANT = [('Indemnite', 'indemnite', (optional, int,)), #XXX
               ('NbMoyenTransport', 'nb_moyen_transport', (optional, int,)),
               ('MoyenTransport', 'moyen_transport',()),
               ('NombreValets', 'nombre_valets', (optional, int,)),
               ('Duree', 'duree', (optional, int,)),
               ('Payeur', 'payeur', (int, bool,)),
               ('Pris', 'pris', (int, bool,)),
               ('Commandement', 'commandement',(int, bool,)),
               ('relation_de', 'relation_de', (int, bool,)),
               ('donne_par', 'donne_par', (int, bool,)),
               ('par_la_main', 'par_la_main', (int, bool,)),
               ('present', 'present', (int, bool,)),
               ('delivre_a', 'delivre_a', (int, bool,)),
               ('fait_compte_avec', 'fait_compte_avec', (int, bool,)),
           ]
def gen_intervenant(ctl):
    for i, row in enumerate(ctl.iter_and_commit('intervenant')):
        entity = mk_entity(row, INTERVENANT)
        ctl.store.add('Intervenant', entity)
        if row['Personne'] in personne_id and row['numTrans'] in transaction_id:
            try:
                ctl.store.relate(entity['eid'], 'prix_valets', prix_id[row['PrixValets']])
            except KeyError:
                if row['PrixValets']:
                    errors.append('line %d: ' %(i+1) + 'Intervenant eid %s missing Prix (prix_valets) %s'%(entity['eid'], row['PrixValets']))

            try:
                ctl.store.relate(entity['eid'], 'prix_transport', prix_id[row['PrixTransport']])
            except KeyError:
                if row['PrixTransport']:
                    errors.append('line %d: ' %(i+1) + 'Intervenant eid %s missing Prix (prix_transport) %s'%(entity['eid'], row['PrixTransport']))

            ctl.store.relate(entity['eid'], 'intervenant', personne_id[row['Personne']])
            ctl.store.relate(transaction_id[row['numTrans']], 'intervenants', entity['eid'])
        if row['Personne'] not in personne_id:
            errors.append('line %d: ' %(i+1) + 'Intervenant missing Personne %s'%(row['Personne']))
        if row['numTrans'] not in transaction_id:
            errors.append('line %d: ' %(i+1) + 'Intervenant missing Transaction %s'%(row['numTrans']))
GENERATORS.append((gen_intervenant, CHK))



achatmateriaux_id = {}
ACHATMATERIAUX = [("TypeMesure", "type_mesure", ()),
                   ("Quantite", "quantite", (optional, atof,)),
                   ('Unite', 'unite', ()),
                   ('provenance_mesure', 'provenance_mesure', ()),
                   ('Conversion', 'conversion', (optional, atof,)),
                  ('date_achat', 'date_achat', (optional, date)),
                   ]
def gen_achatmateriaux(ctl):
    for i, row in enumerate(ctl.iter_and_commit('achatmateriaux')):
        if row['Materiaux'] in materiaux_id and row['numTrans'] in transaction_id:
            entity = mk_entity(row, ACHATMATERIAUX)
            ctl.store.add('AchatMateriaux', entity)
            achatmateriaux_id[row['Id']] = entity['eid']
            ctl.store.relate(entity['eid'], 'materiaux',  materiaux_id[row['Materiaux']])
            ctl.store.relate(transaction_id[row['numTrans']], 'achat', entity['eid'])
            if row['prix_unitaire']:
                ctl.store.relate(entity['eid'], 'prix_unitaire', prix_id[row['prix_unitaire']])
            if row['prix_total']:
                ctl.store.relate(entity['eid'], 'prix_total', prix_id[row['prix_total']])
        if row['Materiaux'] not in materiaux_id:
            errors.append('line %d: ' %(i+1) + 'AchatMateriaux %s: missing materiaux %s' % (row['Id'], row['Materiaux']))
        if row['numTrans'] not in transaction_id:
            errors.append('line %d: ' %(i+1) + 'AchatMateriaux %s: missing transaction %s' % (row['Id'], row['numTrans']))

GENERATORS.append((gen_achatmateriaux, CHK))


achatpretporter_id = {}
ACHATPRETPORTER = [("Quantite", "quantite", (optional, int,)),
                   ('date_achat', 'date_achat', (optional, date)),
                   ]
def gen_achatpretporter(ctl):
    for i, row in enumerate(ctl.iter_and_commit('achatpretporter')):
        if row['Parure'] in parure_id and row['numTrans'] in transaction_id:
            entity = mk_entity(row, ACHATPRETPORTER)
            ctl.store.add('AchatPretPorter', entity)
            achatpretporter_id[row['Id']] = entity['eid']
            ctl.store.relate(entity['eid'], 'parure',  parure_id[row['Parure']])
            ctl.store.relate(transaction_id[row['numTrans']], 'achat', entity['eid'])
            if row['prix_unitaire']:
                ctl.store.relate(entity['eid'], 'prix_unitaire', prix_id[row['prix_unitaire']])
            if row['prix_total']:
                ctl.store.relate(entity['eid'], 'prix_total', prix_id[row['prix_total']])
        if row['Parure'] not in parure_id:
            errors.append('line %d: ' %(i+1) + 'AchatPretPorter %s: missing parure %s' % (row['Id'], row['Parure']))
        if row['numTrans'] not in transaction_id:
            errors.append('line %d: ' %(i+1) + 'AchatPretPorter %s: missing transaction %s' % (row['Id'], row['numTrans']))
GENERATORS.append((gen_achatpretporter, CHK))


achatfabrication_id = {}
ACHATFABRICATION = [("Quantite", "quantite", (optional, int)),
                   ('date_achat', 'date_achat', (optional, date)),
                   ]
def gen_achatfabrication(ctl):
    for i, row in enumerate(ctl.iter_and_commit('achatfabrication')):
        if row['Parure'] in parure_id and row['numTrans'] in transaction_id:
            entity = mk_entity(row, ACHATFABRICATION)
            ctl.store.add('AchatFabrication', entity)
            achatfabrication_id[row['Id']] = entity['eid']
            ctl.store.relate(entity['eid'], 'parure',  parure_id[row['Parure']])
            ctl.store.relate(transaction_id[row['numTrans']], 'achat', entity['eid'])
            if row['prix_unitaire']:
                ctl.store.relate(entity['eid'], 'prix_unitaire', prix_id[row['prix_unitaire']])
            if row['prix_total']:
                ctl.store.relate(entity['eid'], 'prix_total', prix_id[row['prix_total']])
        if row['Parure'] not in parure_id:
            errors.append('line %d: ' %(i+1) + 'AchatFabrication %s: missing parure %s' % (row['Id'], row['Parure']))
        if row['numTrans'] not in transaction_id:
            errors.append('line %d: ' %(i+1) + 'AchatFabrication %s: missing transaction %s' % (row['Id'], row['numTrans']))
GENERATORS.append((gen_achatfabrication, CHK))


fabriqueavecmat_id = {}
FABRIQUEAVECMAT = [("TypeMesure", "type_mesure", ()),
                   ("Quantite", "quantite", (optional, atof,)),
                   ('Unite', 'unite', ()),
                   ('provenance_mesure', 'provenance_mesure', ()),
                   ('Conversion', 'conversion', (optional, atof,)),
                   ('usage', 'usage', ()),
                  ]
def gen_fabriqueavecmat(ctl):
    for i, row in enumerate(ctl.iter_and_commit('fabriqueavecmat')):
        if row['IdFab'] in achatfabrication_id and row['IdMP'] in achatmateriaux_id:
            entity = mk_entity(row, FABRIQUEAVECMAT)
            ctl.store.add('FabriqueAvecMat', entity)
            ctl.store.relate(achatfabrication_id[row['IdFab']], 'avec_mat', entity['eid'])
            ctl.store.relate(entity['eid'], 'achat_matiere', achatmateriaux_id[row['IdMP']])
        if row['IdFab'] not in achatfabrication_id:
            errors.append('line %d: ' %(i+1) + 'FabriqueAvecMat: missing AchatFabrication %r' % (row['IdFab']))
        if row['IdMP'] not in achatmateriaux_id:
            errors.append('line %d: ' %(i+1) + 'FabriqueAvecMat: missing AchatMateriaux %r' % (row['IdMP']))

GENERATORS.append((gen_fabriqueavecmat, CHK))





# create controller
if 'cnx' in locals():
    ctl = CWImportController(RQLObjectStore(cnx), askerror=True, commitevery=100)
else:
    ctl = CWImportController(ObjectStore())
ctl.generators = GENERATORS
datasources = [('compte', 'MCompte'),
               ('lieu', 'MLieu'),
               ('monnaie', 'MMonnaie'),
               ('personne', 'MPersonne'),
               ('materiaux', 'MMateriaux'),
               ('prix', 'MPrix_cp1252'),
               ('change', 'MChange'),
               ('occupation', 'MOccupation'),
               ('occasion', 'MOccasion'),
               ('destinataire', 'MLDestinataire'),
               ('intervenant', 'MLIntervenant'),
               ('vendeur', 'MLVendeur'),
               ('travail', 'MTravaille'),
               ('ltravail', 'MLTravaille'),
               ('receveur', 'MLReceveur'),
               ('parure', 'MParure'),
               ('materiauxparure', 'MLParureMateriaux'),
               ('transaction', 'MTransaction'),
               ('achatpretporter', 'MAchatPretPorter'),
               ('achatfabrication', 'MAchatFabrication'),
               ('achatmateriaux', 'MAchatMateriaux'),
               ('fabriqueavecmat', 'MLFabriqueMatierePremiere'),
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
