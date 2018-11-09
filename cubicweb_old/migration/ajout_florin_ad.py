import os.path as osp
migr_dir = osp.dirname(__file__)
target_monnaie = rql('Any M WHERE M is Monnaie, M nom "g. t. p. p."').get_entity(0, 0)

print "init transactions"
transactions = {}
for t in rql('Any T WHERE T is Transaction').entities():
    transactions[t.dc_title()] = t.eid
print "init monnaies"
monnaies = {}
for m in rql('Any M WHERE M is Monnaie').entities():
    monnaies[m.nom] = m.eid
print "read csv file"
import csv
import codecs
f=open(osp.join(migr_dir, 'florin_ad.csv'), 'r')
dialect = csv.Sniffer().sniff(f.read(1024), ';')
f.seek(0)
reader = csv.DictReader(f, dialect=dialect)
monnaies_ad = {}
prix_monnaies = set()
for row in reader:
    ad = float(row['monnaie ad'].replace(',', '.'))
    monnaie = monnaies[row['monnaie'].decode('utf-8')]
    prix_monnaies.add(monnaie)
    transaction = transactions[row['source'].decode('utf-8')]
    monnaies_ad.setdefault(transaction, []).append((ad, monnaie))


print "processing prix"
query = 'Any P ORDERBY P WHERE P is Prix, NOT EXISTS(C prix_depart P), NOT EXISTS (C2 prix_converti P), P monnaie M, M eid in (%s)'
rset = rql(query % (','.join(str(m) for m in prix_monnaies)))

def compute_ad_from_file(prix):
    monnaie_prix = prix._get_monnaie()
    transactions = prix.get_transaction(allow_multi=True)
    for transaction in transactions:
        for ad, monnaie_eid in monnaies_ad.get(transaction.eid, []):
            if monnaie_prix == monnaie_eid:
                print prix.monnaie[0].dc_title().encode('utf-8'), ad
                rql('SET P florin_ad %(ad)s WHERE P eid %(eid)s', {'ad': ad, 'eid': prix.eid})
                return True
    return False

def compute_ad_from_changes(prix):
    monnaie_prix = prix._get_monnaie()
    for mode, changes in prix._search_changes():
        path = prix._get_change_path(changes, target_monnaie.eid)
        if not path:
            continue
        conversion = 1.
        monnaie = monnaie_prix
        for comp in path:
            change = comp[-1][-1]
            conversion, monnaie = change.change(conversion, monnaie)
        ad = conversion
        print prix.monnaie[0].dc_title().encode('utf-8'), ad
        rql('SET P florin_ad %(ad)s WHERE P eid %(eid)s', {'ad': ad, 'eid': prix.eid})
        return True
    return False

success_file = 0
success_change = 0
nb_prix = len(rset)
for i, prix in enumerate(rset.entities()):
    if (success_file+success_change) % 100 == 99:
        commit()
    print ' ', success_file, success_change, success_file+success_change
    print '%d/%d %d' % (i+1, nb_prix, prix.eid)
    status = compute_ad_from_file(prix)
    if status:
        success_file += 1
        continue
    status = compute_ad_from_changes(prix)
    if status:
        success_change += 1
print ' ', success_file, success_change, success_file+success_change

commit()
