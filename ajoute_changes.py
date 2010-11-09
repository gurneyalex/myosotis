import sys, codecs
#sys.stdout = codecs.EncodedFile(sys.stdout,'utf-8')
rset = rql('Any T WHERE T is Transaction')

count = 0
print "transaction\tmonnaie transaction\tremarque"
for transaction in rset.entities():
    rem = transaction.remarques
    if rem is None:
        continue
    rem = rem.lower()
    if u's. ' in rem or ' d ' in rem or rem.endswith(' d') or ' ad ' in rem:
        prix = transaction.prix_ensemble
        if prix:
            monnaie = prix[0].monnaie[0].nom.encode('utf-8')
        else:
            monnaie = None
        print '%s\t%s\t%s' % (transaction.eid, monnaie, rem.encode('utf-8'))
        count += 1
print count
