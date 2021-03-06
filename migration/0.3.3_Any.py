# -*- coding: utf-8 -*-
add_attribute('Occupation', 'annee')
add_attribute('Compte', 'historic')
sync_schema_props_perms('Prix')
commit()

rql('SET C historic True WHERE C is Compte')
rql('SET C historic False WHERE C is Compte, C inventaire "nul"')
rql('SET C historic False WHERE C is Compte, C inventaire "test"')

nulcompte = rql('Any CPT WHERE CPT inventaire "nul"').get_entity(0, 0)
rset = rql('Any C where C is Change, CPT change C, CPT inventaire "nul"')

monnaies = {}
for monnaie in rql('Any M WHERE M is Monnaie').entities():
    monnaies[monnaie.nom] = monnaie.eid
    
std_changes = set()
for change in rset.entities():
    std_changes.add((change.prix_depart[0].monnaie[0].eid, change.prix_converti[0].monnaie[0].eid)
                    )
if (monnaies['Gros'], monnaies['Gros tournois']) not in std_changes:
    p1 = create_entity('Prix', deniers=1, monnaie = monnaies['Gros'])
    p2 = create_entity('Prix', deniers=1, monnaie = monnaies['Gros tournois'])
    change = create_entity('Change', prix_depart=p1.eid, prix_converti=p2, reverse_change=nulcompte.eid)

if (monnaies['Gros tournois'], monnaies['g. t. p. p.']) not in std_changes:
    p1 = create_entity('Prix', deniers=1, monnaie = monnaies['Gros tournois'])
    p2 = create_entity('Prix', deniers=1, monnaie = monnaies['g. t. p. p.'])
    change = create_entity('Change', prix_depart=p1.eid, prix_converti=p2, reverse_change=nulcompte.eid)

if (monnaies["Florin d'or petit poids"], monnaies['g. t. p. p.']) not in std_changes:
    p1 = create_entity('Prix', florins=1, monnaie = monnaies["Florin d'or petit poids"])
    p2 = create_entity('Prix', deniers=12, monnaie = monnaies['g. t. p. p.'])
    change = create_entity('Change', prix_depart=p1.eid, prix_converti=p2, reverse_change=nulcompte.eid)


# corrections des prix en Franc Or renseignes comme si cette monnaie était une monnaie or (c'est un Florin Gros)
prix_franc_or = rql('Any P WHERE P is Prix, P monnaie M, M nom "franc or", P monnaie_or > 0')
for prix in prix_franc_or.entities():
    rql('SET P florins %(f)s, P monnaie_or NULL WHERE P eid %(eid)s',
        {'eid': prix.eid, 'f': prix.monnaie_or})

commit()
