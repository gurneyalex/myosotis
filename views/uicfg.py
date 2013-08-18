from cubicweb.web.views import uicfg

def setup_ui(vreg):
    _pvs = uicfg.primaryview_section
    _pdc = uicfg.primaryview_display_ctrl
    _afs = uicfg.autoform_section
    _pvs.tag_object_of(('*', 'compte', 'Compte'), 'hidden')
    _pvs.tag_subject_of(('*', 'prix_depart', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_converti', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'salaire_argent', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'salaire_aides', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_valet', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_transport', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_total', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_unitaire', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'lieu', 'Lieu'), 'attributes')
    _pvs.tag_subject_of(('*', 'lieu_domicile', 'Lieu'), 'attributes')
    _pvs.tag_subject_of(('*', 'lieu_origine', 'Lieu'), 'attributes')
    _pvs.tag_object_of(('*', 'rattache_a', 'Personne'), 'hidden')
    _pvs.tag_object_of(('*', 'personne', 'Personne'), 'hidden')
    _pvs.tag_object_of(('*', 'artisan', 'Personne'), 'hidden')
    _pvs.tag_object_of(('*', 'vendeur', 'Personne'), 'hidden')
    _pvs.tag_object_of(('*', 'intervenant', 'Personne'), 'hidden')
    _pvs.tag_object_of(('*', 'destinataire', 'Personne'), 'hidden')
    _pvs.tag_subject_of(('Transaction', 'travaux', 'Travail'), 'relations')
    _pvs.tag_subject_of(('Transaction', 'vendeurs', 'Vendeur'), 'relations')
    _pdc.tag_subject_of(('Transaction', 'vendeurs', 'Vendeur'), {'vid': 'attributestableview', 'limit': None})
    _pvs.tag_subject_of(('Transaction', 'destinataires', 'Destinataire'), 'relations')
    _pdc.tag_subject_of(('Transaction', 'destinataires', 'Destinataire'), {'vid': 'list', 'limit': None})
    _pvs.tag_subject_of(('Transaction', 'intervenants', 'Intervenant'), 'relations')
    _pdc.tag_subject_of(('Transaction', 'intervenants', 'Intervenant'), {'vid': 'attributestableview', 'limit': None})
    _pvs.tag_subject_of(('Transaction', 'achat', '*'), 'relations')
    _pdc.tag_subject_of(('Transaction', 'achat', '*'), {'vid': 'list', 'limit': None})
    _pvs.tag_subject_of(('Transaction', 'prix_ensemble', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'compte', '*'), 'sideboxes')
    _pvs.tag_attribute(('Transaction', 'type_achat'), 'hidden')
    _afs.hide_fields('Transaction', ['type_achat'])
    _pvs.tag_subject_of(('Materiaux', 'provenance', '*'), 'attributes')
    _pvs.tag_object_of(('*', 'occasion', 'Occasion'), 'relations')
    _pdc.tag_object_of(('*', 'occasion', 'Occasion'), {'vid': 'myosotis.transaction.attributestableview', 'limit': None})
    _pvs.tag_subject_of(('AchatFabrication', 'avec_mat', '*'), 'relations')
    _pdc.tag_subject_of(('AchatFabrication', 'avec_mat', '*'), {'vid': 'list', 'limit': None})
    _pvs.tag_subject_of(('Occupation', 'personne', 'Personne'), 'attributes')
    inline_relations()

def inline_relations():
    _afs = uicfg.autoform_section
    to_inline = {'AchatPretPorter': ('parure',
                                     'prix_unitaire',
                                     'prix_total'),
                 'AchatFabrication': ('parure',
                                      'prix_unitaire',
                                      'prix_total',
                                      'avec_mat'),
                 'AchatMateriaux': ('materiaux',
                                    'prix_unitaire',
                                    'prix_total'),
                 'Travail': ('salaire_aide', 'salaire_argent'),
                 'Change': ('prix_converti', 'prix_depart'),
                 'Transaction': ('prix_ensemble',),
                 'Intervenant': ('prix_valet', 'prix_transport'),
                 'Parure': ('composee_de',),
                 'MateriauxParure': ('materiaux',),
                 }
    for etype, rtypes in to_inline.iteritems():
        for rtype in rtypes:
            _afs.tag_subject_of((etype, rtype, '*'), 'main', 'inlined')

def registration_callback(vreg):
    setup_ui(vreg)
