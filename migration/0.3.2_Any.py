# -*- coding: utf-8 -*-
add_attribute('Prix', 'florin_ad')


add_attribute('Monnaie', 'nb_gros')
nb_gros = [(u'Florentin', 12),
           (u"florin d'or", 12),
           (u'Florin gros', 12),
           (u'florin reg.', 12),
           (u'Ducat', 14),
           (u'ducat de Genes', 14),
           (u'florin b. p. orangie', 12),
           (u'Florin de Genes', 12),
           (u"florin d'or b. p.", 12.5),
           (u"florin d'or b. p. vet.", 12.5),
           (u'écus', 20),
           (u"Florin d'or petit poids", 11),
           (u'Florin duc. au.', 12),
           (u'franc or', 16),
           (u'franc or reg', 16),
           (u"gênois d'or", 12),
           ]

for monnaie, nb in nb_gros:
    rql('SET M nb_gros %(gros)s WHERE M is Monnaie, M nom %(nom)s', {'nom': monnaie, 'gros': nb})

commit()
