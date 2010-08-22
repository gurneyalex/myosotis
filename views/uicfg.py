from cubicweb.web import uicfg

def setup_ui(vreg):
    _pvs = uicfg.primaryview_section
    _pvs.tag_object_of(('*', 'compte', 'Compte'), 'hidden')
    _pvs.tag_subject_of(('Transaction', 'prix_ensemble', 'Prix'), 'attributes')
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

def registration_callback(vreg):
    setup_ui(vreg)
