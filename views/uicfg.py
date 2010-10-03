from cubicweb.web import uicfg

def setup_ui(vreg):
    _pvs = uicfg.primaryview_section
    _pdc = uicfg.primaryview_display_ctrl
    _pvs.tag_object_of(('*', 'compte', 'Compte'), 'hidden')
    _pvs.tag_subject_of(('*', 'prix_depart', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_converti', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'salaire_argent', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'salaire_aides', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('*', 'prix_transports', 'Prix'), 'attributes')
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
    _pvs.tag_subject_of(('Transaction', 'travaux', 'Travail'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'vendeurs', 'Vendeur'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'destinataires', 'Destinataire'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'intervenants', 'Intervenant'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'achat', '*'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'prix_ensemble', 'Prix'), 'attributes')
    _pvs.tag_subject_of(('Transaction', 'compte', '*'), 'sideboxes')
    _pvs.tag_subject_of(('Materiaux', 'provenance', '*'), 'attributes')
    _pvs.tag_object_of(('*', 'occasion', 'Occasion'), 'relations')
    _pdc.tag_object_of(('*', 'occasion', 'Occasion'), {'vid': 'myosotis.transaction.attributestableview', 'limit': None})

def registration_callback(vreg):
    setup_ui(vreg)
