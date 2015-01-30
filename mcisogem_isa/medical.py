# -*- coding: utf8 -*-
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields
from openerp.osv import osv
from datetime import datetime
from openerp import tools
from openerp.tools.translate import _
import openerp
from dateutil.relativedelta import relativedelta
from dateutil import parser
import logging
_logger = logging.getLogger(__name__)


_logger = logging.getLogger(__name__)

class mcisogem_langue(osv.osv):
    _name = "mcisogem.langue"
    _description = 'Langue'
    _columns = {
        'code_langue': fields.char('Code de la langue', size=10, required=True),
        'libelle_langue': fields.char('Libelle de la langue', size=50)
    }
     
class mcisogem_pays(osv.osv):
    _name = "mcisogem.pays"
    _description = 'Pays'
    _columns = {
        'name': fields.char('Code pays', size=18, required=True),
        'libelle_pays': fields.char('Libelle pays', size=50),
        'code_langue': fields.many2one('mcisogem.langue')
    }
    
class mcisogem_ville(osv.osv):
    _name = "mcisogem.ville"
    _description = 'Ville'
    _columns = {
        'name': fields.char('Code de la ville', size=18, required=True),
        'libelle_ville': fields.char('Libelle pays', size=50, required=True),
        'region': fields.many2one('mcisogem.region', 'Region'),
        'libelle_region' : fields.char('Libelle', readonly=True),
        'zone_geo': fields.many2one('mcisogem.zone', 'Zone geographique'),
        'libelle_zone' : fields.char('Libelle', readonly=True),
        'code_postal': fields.integer('Code postal'),
        'code_gest': fields.char('Code du centre de gestion')
    }
    
    def onchange_region(self, cr, uid, ids, region, context=None):
        if not region:
            return {'value': {'libelle_region': False}}
        if region:
            code_region_data = self.pool.get('mcisogem.region').browse(cr, uid, region, context=context)
        return{'value': {'libelle_region': code_region_data.libelle_region}}
    
    def onchange_code_zone(self, cr, uid, ids, zone_geo, context=None):
        if not zone_geo:
            return {'value': {'libelle_zone': False}}
        if zone_geo:
            code_zone_data = self.pool.get('mcisogem.zone').browse(cr, uid, zone_geo, context=context)
        return{'value': {'libelle_zone': code_zone_data.libelle_zone_geo}}
    
class mcisogem_zone(osv.osv):
    _name = "mcisogem.zone"
    _description = 'Zone geographique'
    _columns = {
        'name': fields.char('Code zone geographique', size=10, required=True),
        'libelle_zone_geo': fields.char('Libelle zone geographique', size=50, required=True),
        'code_gest': fields.char('Code du centre de gestion')
    }
    
class mcisogem_devise(osv.osv):
    _name = "mcisogem.devise"
    _description = 'Devise'
    _columns = {
        'name': fields.char('Code devise', size=10, required=True),
        'libelle_devise': fields.char('Libelle devise', size=150),
        'cours_devise_ref': fields.float('Cours par rapport a la devise de reference', digits=(10, 5)),
        'date_cours_devise': fields.datetime("Date du cours de la devise"),
        'code_langue': fields.char('Code langue'),
        'code_gest': fields.char('Code du centre de gestion')
    }
    
class mcisogem_type_garant(osv.osv):
    _name = "mcisogem.type.garant"
    _description = 'Type garant'
    _columns = {
        'name': fields.char('Code type garant', size=18, required=True),
        'libelle_type_garant': fields.char('Libelle type garant', size=50),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion')        
    }
    
class mcisogem_type_avenant(osv.osv):
    _name = "mcisogem.type.avenant"
    _description = 'Type avenant'
    _columns = {
        'name': fields.char('Code type avenant', size=5, required=True),
        'libelle_type_avenant': fields.char('Libelle type avenant', size=150),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion')        
    }
    
class mcisogem_type_contrat(osv.osv):
    _name = "mcisogem.type.contrat"
    _description = 'Type contrat'
    _columns = {
        'name': fields.integer('Code type contrat', required=True),
        'libelle_type_contrat': fields.char('Libelle type contrat', required=True, size=150),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion'),
        'cod_tx_comxion': fields.char('Code tx')          
    }
    
    _defaults = {
        'cod_tx_comxion': 1
    }
    
class mcisogem_mode_recond(osv.osv):
    _name = "mcisogem.mod.recond"
    _description = 'Mode de reconduction'
    _columns = {
        'name': fields.integer('Code mode de reconduction', required=True),
        'libelle_mod_recond': fields.char('Libelle mode de reconduction', size=150),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion')    
    }
    
class mcisogem_regime(osv.osv):
    _name = "mcisogem.regime"
    _description = 'Type de remboursement'
    _columns = {
        'name': fields.char('Code regime', size=10, required=True),
        'libelle_regime': fields.char('Libelle regime', size=50),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion')    
    }
    
class mcisogem_concurrent(osv.osv):
    _name = "mcisogem.concurrent"
    _description = 'Concurrents'
    _columns = {
        'name': fields.char('Code concurrent', size=20, required=True),
        'libelle_concur': fields.char('Libelle concurrent', size=150),
        'code_gest': fields.char('Code centre de gestion')    
    }
    
class mcisogem_unite_temps(osv.osv):
    _name = "mcisogem.unite.temps"
    _description = 'Unite temps'
    _columns = {
        'name': fields.char('Code unite temps', size=1, required=True),
        'libelle_unite_temps': fields.char('Libelle unite temps', size=150),
        'nbre_jour': fields.integer('Nombre de jour'),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion')    
    }

class mcisogem_territoire(osv.osv):
    _name = "mcisogem.territoire"
    _description = 'Territoire'
    _columns = {
        'name': fields.char('Code territorialite', size=30, required=True),
        'libelle_territoire': fields.char('Libelle territorialite', size=150, required=True),
        'code_lang': fields.char('Code langue'),
        'code_gest': fields.char('Code centre de gestion')
    }
    
class mcisogem_commune(osv.osv):
    _name = "mcisogem.commune"
    _description = 'Commune'
    _columns = {
        'code_commune': fields.char('Code commune', size=20, required=True),
        'code_ville': fields.many2one('mcisogem.ville', "Code de la ville", required=True),
        'name': fields.char('Libellé commune', size=150, required=True),
        'code_gest': fields.char('Code centre de gestion'),
        'code_sup' : fields.char('cod_sup', size=1)
    }
    
class mcisogem_region(osv.osv):
    _name = "mcisogem.region"
    _description = 'Region'
    _columns = {
        'name': fields.char('Code region', size=10, required=True),
        'libelle_region': fields.char('Libelle region', size=50),
        'pays': fields.many2one('mcisogem.pays', "Code Pays"),
        'libelle_pays' : fields.char('Libelle', readonly=True),
        'code_zone_geo': fields.many2one('mcisogem.zone', "Code Zone geographique"),
        'libelle_zone' : fields.char('Libelle', readonly=True),
        'code_gest': fields.char('Code du centre de gestion')
    }

        
    def onchange_code_pays(self, cr, uid, ids, pays, context=None):
        if not pays:
            return {'value': {'libelle_pays': False}}
        if pays:
            code_pays_data = self.pool.get('mcisogem.pays').browse(cr, uid, pays, context=context)
        return{'value': {'libelle_pays': code_pays_data.libelle_pays}}
    
    def onchange_code_zone(self, cr, uid, ids, code_zone_geo, context=None):
        if not code_zone_geo:
            return {'value': {'libelle_zone': False}}
        if code_zone_geo:
            code_zone_data = self.pool.get('mcisogem.zone').browse(cr, uid, code_zone_geo, context=context)
        return{'value': {'libelle_zone': code_zone_data.libelle_zone_geo}}

class mcisogem_centre_gestion(osv.osv):
    _name = "mcisogem.centre.gestion"
    _description = 'Centre de gestion'
    _columns = {
        'name': fields.char('Code centre de gestion', size=10, required=True),
        'libelle_centre': fields.char('Libelle centre de gestion', size=50),
        'code_devise': fields.many2one('mcisogem.devise', "Devise"),
        'libelle_devise' : fields.char('Libelle', readonly=True),
        'code_langue': fields.many2one('mcisogem.langue', "Langue"),
        'libelle_langue' : fields.char('Libelle', readonly=True),
        'code_pays': fields.many2one('mcisogem.pays', "Pays"),
        'libelle_pays' : fields.char('Libelle', readonly=True),
        'code_territoire': fields.many2one('mcisogem.territoire', "Territoire"),
        'libelle_territoire' : fields.char('Libelle', readonly=True),
        'code_gest': fields.char('Code du centre de gestion')
    }
        
    def onchange_code_devise(self, cr, uid, ids, code_devise, context=None):
        if not code_devise:
            return {'value': {'libelle_devise': False}}
        if code_devise:
            code_devise_data = self.pool.get('mcisogem.devise').browse(cr, uid, code_devise, context=context)
        return{'value': {'libelle_devise': code_devise_data.libelle_devise}}
    
    def onchange_code_langue(self, cr, uid, ids, code_langue, context=None):
        if not code_langue:
            return {'value': {'libelle_langue': False}}
        if code_langue:
            code_langue_data = self.pool.get('mcisogem.langue').browse(cr, uid, code_langue, context=context)
        return{'value': {'libelle_langue': code_langue_data.libelle_langue}}
    
    def onchange_code_pays(self, cr, uid, ids, code_pays, context=None):
        if not code_pays:
            return {'value': {'libelle_pays': False}}
        if code_pays:
            code_pays_data = self.pool.get('mcisogem.pays').browse(cr, uid, code_pays, context=context)
        return{'value': {'libelle_pays': code_pays_data.libelle_pays}}
    
    def onchange_code_territoire(self, cr, uid, ids, code_territoire, context=None):
        if not code_territoire:
            return {'value': {'libelle_territoire': False}}
        if code_territoire:
            code_territoire_data = self.pool.get('mcisogem.territoire').browse(cr, uid, code_territoire, context=context)
        return{'value': {'libelle_territoire': code_territoire_data.libelle_territoire}}
        
        
        
        
    
"""
**********************************************************************************
CLASSE DU MODULE MEDICAL
**********************************************************************************
"""    

""" Classe : Utilisateurs """
class res_users(osv.osv):
    _inherit = 'res.users'
    _columns = {
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion"),
        'poste': fields.char('Poste', size=30),
}

""" Classe : TYPE_CENTRE """ 
class mcisogem_type_centre(osv.osv):
    _name = "mcisogem.type.centre"
    _description = 'Type de centre'
    _columns = {
        'code_type_centre': fields.char('Code type centre', size=10, required=True),
        'name': fields.char('Libellé type centre', size=50, required=True),
        'code_type_reserve' : fields.boolean('Type reservé'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'libelle_gest': fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'Nbre_ctr' : fields.integer('Nbre_ctr'),
        'code_type_centre2' : fields.char('Lettre type de centre', size=50, required=True)                
    }
    
    _sql_constraints = [('unique_type_centre', 'unique(code_type_centre, code_langue)', "Le type de centre existe déjà !"), ]

    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        # Récuperation du centre de gestion de l'utilisateur
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)
        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        vals['Nbre_ctr'] = 0
        return super(mcisogem_type_centre, self).create(cr, uid, vals, context=context)
        
    
mcisogem_type_centre() 


""" Classe : PLAGE_CENTRE """ 
class mcisogem_plage_centre(osv.osv):
    
    _name = "mcisogem.plage.centre"
    _description = 'Plage centre'
  
    _columns = {
        'numero_plage_centre': fields.integer('Code plage', required=True),
        'code_gest': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'libelle_gest': fields.char('libelle_gest', size=10, required=True), 'code_type_centre': fields.many2one('mcisogem.type.centre', "Type de centre", required=True),
        'code_centre' : fields.char('Code centre', size=50),
        'code_plage' : fields.integer('Code début plage', size=50, required=True),
        'dernier_numero' : fields.integer('Dernier numéro'),
    }
    
    _sql_constraints = [('unique_plage_centre', 'unique(numero_plage_centre,code_gest,code_type_centre,code_plage)', "Cette plage de centre existe déjà !"), ]

  
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        # Récuperation du type de centre
        type_centre_data = self.pool.get('mcisogem.type.centre').browse(cr, uid, vals['code_type_centre'], context=context)
        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['dernier_numero'] = vals['code_plage']
        vals['code_centre'] = type_centre_data.code_type_centre2
        return super(mcisogem_plage_centre, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        # Récuperation du type de centre
        type_centre_data = self.pool.get('mcisogem.type.centre').browse(cr, uid, vals['code_type_centre'], context=context)
        # Ajout des valeurs par defauts
        vals['code_centre'] = type_centre_data.code_type_centre2
        return super(mcisogem_plage_centre, self).write(cr, uid, ids, vals, context=context) 
    

mcisogem_plage_centre()

""" Classe : CENTRE """ 
class mcisogem_centre(osv.osv):
    
    _name = "mcisogem.centre"
    _description = 'Centre'
    
    _columns = {
        'code_centre': fields.char('Code du centre', size=10, required=True),
        'code_type_centre': fields.many2one('mcisogem.type.centre', "Type de centre", required=True),
        'code_ville': fields.many2one('mcisogem.ville', "Ville", required=True),
        'name' : fields.char('Libellé du centre', size=150, required=True),
        'adresse_centre' : fields.char('Adresse', size=60),
        'code_bp_centre' : fields.char('Code BP', size=20),
        'bp_centre' : fields.char('Boite postale', size=20),
        'tel_centre1' : fields.char('Téléphone 1', size=20),
        'tel_centre2' : fields.char('Téléphone 2', size=20),
        'fax_centre' : fields.char('Fax', size=20),
        'observation_centre' : fields.text('Observation', size=65),
        'regl_centre_prestat' : fields.selection([('C', 'Centre'), ('P', 'Prestataire'), ('A', 'Autre ordre')], 'Paiement à l\'ordre de '),
        'mode_paiement_centre' : fields.selection([('LC', 'Chèque'), ('ES', 'Espèce'), ('VI', 'Virement bancaire'), ('AU', 'Autre')], 'Mode de paiement'),
        'numero_banque_centre' : fields.char('No Banque', size=20),
        'numero_guichet_centre' : fields.char('No Guichet', size=20),
        'numero_compte_centre' : fields.char('No Compte', size=20),
        'cle_rib_centre' : fields.char('Clé RIB', size=20),
        'autre_ordre_centre' : fields.char('Autre ordre', size=65),
        'bl_cme' : fields.boolean('Centre d\'entreprise'),
        'cpta_centre' : fields.char('Compte général', size=20),
        'code_gest': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'libelle_gest': fields.char('libelle_gest', size=10, required=True),
        'code_type_centre': fields.many2one('mcisogem.type.centre', "Type de centre", required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'email_centre' : fields.char('Email', size=50),
        'correspondant' : fields.char('Correspondant', size=150),
        'responsable' : fields.char('Responsable', size=150),
        'capital' : fields.integer('Capital'),
        'code_territoire': fields.many2one('mcisogem.territoire', "Térritoire"),
        'mot_passe' : fields.char('Mot de passe', size=50, required=True),
        'code_commune': fields.many2one('mcisogem.commune', "Commune", required=True),
        'privilege' : fields.selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], 'Privilège'),
        'activer' : fields.boolean('Activé'),
        'compta_prestat_tiers' : fields.char('Compte tiers', size=50),
        'code_externe' : fields.char('Code externe', size=50),
}
    
       
    def onchange_code_ville_centre(self, cr, uid, ids, code_ville, context=None):
            return {'value': {'code_commune' : False}}
    
    def onchange_regl_centre_prestat(self, cr, uid, ids, nom, context=None):
        if not nom:
            return {'value': {'autre_ordre_centre' : False}}
        if nom:
            return {'value': {'autre_ordre_centre' : nom}}

    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        # Génaration du code du centre 
        plage_centre_id = self.pool.get('mcisogem.plage.centre').search(cr, uid, args=[('code_type_centre', '=', vals['code_type_centre'])], offset=0, limit=None, order=None, context=None, count=False)
        plage_centre_data = self.pool.get('mcisogem.plage.centre').browse(cr, uid, plage_centre_id[0], context=context)
        vals['code_centre'] = plage_centre_data.code_centre + str(plage_centre_data.code_plage) + str(plage_centre_data.dernier_numero)
        self.pool.get('mcisogem.plage.centre').write(cr, uid, plage_centre_data.id, {'dernier_numero': plage_centre_data.dernier_numero + 1})
        return super(mcisogem_centre, self).create(cr, uid, vals, context=context)

mcisogem_centre()

""" Classe : FAM_ACTIVITE """ 
class mcisogem_fam_activite(osv.osv):
    _name = "mcisogem.fam.activite"
    _description = 'Famille d\'activité'
    
    _sql_constraints = [('unique_fam_activite', 'unique(code_activite,code_fam_prest)', "Cette famille d'activité existe déjà !"), ] 
    
    _columns = {
        'code_activite': fields.char('Code de l\'activite', size=10, required=True),
        'code_fam_prest': fields.integer('Code famille', required=True),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
mcisogem_fam_activite()

""" Classe : FAM_PREST """ 
class mcisogem_fam_prest(osv.osv):
    _name = "mcisogem.fam.prest"
    _description = 'Famille d\'actes'
    
    _sql_constraints = [('unique_fam_prest', 'unique(code_langue,libelle_court_famille,code_gest)', "Cette famille d'activité existe déjà !"), ] 
    
    _columns = {
        'code_famille': fields.integer('Code de la famille', required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'libelle_court_famille' : fields.char('Libellé court', size=10, required=True),
        'name' : fields.char('Libellé', size=60, required=True),
        'observation_famille' : fields.text('Observation', size=65),
        'type_liasse' : fields.char('type_liasse', size=1),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'type_fam_act' : fields.integer('type_fam_act'),
}
    _defaults = {
        'type_fam_act': 0
}
  
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Récuperation du dernier code famile pour faire l'incrementation
        search_ids = self.pool.get("mcisogem.fam.prest").search(cr, uid, [])
        # Testons le contenu de la liste
        last_id = 0
        if not search_ids:
            last_id = 1
        else :
            # Recuperation du code famille
            last_id = search_ids and max(search_ids)
            last_famille_data = self.pool.get('mcisogem.fam.prest').browse(cr, uid, last_id, context=context)
            last_id = last_famille_data['code_famille']
            last_id = last_id + 1   
        vals['code_famille'] = last_id
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        id_famille = super(mcisogem_fam_prest, self).create(cr, uid, vals, context=context)
        
        # Recuperation de l'enregistrement code famille crée
        famille_data = self.pool.get('mcisogem.fam.prest').browse(cr, uid, id_famille, context=context)
        vals1 = {}
        vals1['code_activite'] = famille_data['code_famille']
        vals1['code_fam_prest'] = famille_data['code_famille']
        vals1['code_gest'] = utilisateur_data.code_gest.id
        vals1['libelle_gest'] = utilisateur_data.code_gest.name
        self.pool.get('mcisogem.fam.activite').create(cr, uid, vals1, context=context)
        return id_famille    
    
mcisogem_fam_prest()


""" Classe : NOM_PREST """ 
class mcisogem_nomen_prest(osv.osv):
    _name = "mcisogem.nomen.prest"
    _description = 'Actes'
    
    _sql_constraints = [('unique_nomen_prest', 'unique(code_langue,libelle_court_acte)', "Cette famille d'activité existe déjà !"), ] 
    
    _columns = {
        'libelle_court_acte': fields.char('Code de l\'acte', size=10, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_fam_prest': fields.many2one('mcisogem.fam.prest', "Code de la famille d'acte", required=True),
        'name' : fields.char('Libellé', size=100, required=True),
        'cout_unit_nomen' : fields.integer('cout_unit_nomen'),
        'l_de_nomen' : fields.char('l_de_nomen', size=3),
        'mtt_lc_carmed' : fields.integer('mtt_lc_carmed'),
        'mtt_lc_hors_carmed' : fields.integer('mtt_lc_hors_carmed'),
        'ratio_th_nomen' : fields.integer('ratio_th_nomen'),
        'bl_nomen_envig' : fields.boolean('En vigueur'),
        'observation_nomen' : fields.text('Observation', size=65),
        'plf_prest_dft' : fields.integer('plf_prest_dft'),
        'ticm_dft' : fields.integer('ticm_dft'),
        'bl_ticm_tx_dft' : fields.integer('bl_ticm_tx_dft'),
        'prest_espece_dft' : fields.integer('prest_espece_dft'),
        'plf_an_prest_dft' : fields.integer('plf_an_prest_dft'),
        'max_act_an_dft' : fields.integer('max_act_an_dft'),
        'bl_envig_carmed' : fields.integer('bl_envig_carmed'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True), 'code_sup' : fields.char('cod_sup', size=1),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
    _defaults = {
        'bl_envig_carmed': 0,
        'max_act_an_dft' : 0,
        'plf_an_prest_dft' : 0,
        'prest_espece_dft' : 0,
        'bl_ticm_tx_dft' : 0,
        'ticm_dft' : 0,
        'plf_prest_dft' : 0,
        'ratio_th_nomen' : 0,
        'mtt_lc_hors_carmed' : 0,
        'mtt_lc_carmed' : 0,
        'cout_unit_nomen' : 0,
        
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_nomen_prest, self).create(cr, uid, vals, context=context)
    
mcisogem_nomen_prest()


class mcisogem_acte_entente_preal(osv.osv):

    _name = "mcisogem.acte.entente.prealable"
    _description = 'Actes soumis à entente préalable'
    
    _sql_constraints = [('unique_nomen_prest', 'unique(code_langue,code_famille)', "Cette famille d'activité figure déjà dans la liste des actes soumis à entente préalable, veuillez la modifier si vous désirez ajouter ou rétirer des actes !"), ] 
    
    _columns = {
        # 'acte_ids': fields.one2many('mcisogem.nomen.prest','libelle_court_acte', 'Acte'),
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte"),
        'acte_ids': fields.many2many('mcisogem.nomen.prest',
                                       'mcisogem_acte_rel',
                                        'acte_entente_prealable_id',
                                        'code_acte',
                                        'Actes soumis à entente préalable'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion"),
        'libelle_gest' : fields.char('libelle_gest', size=10),
        'code_sup' : fields.char('cod_sup', size=1),
        'code_langue': fields.char('code_langue', size=10),
    }
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_acte_entente_preal, self).create(cr, uid, vals, context=context)

    def onchange_code_famille_entente(self, cr, uid, ids, code_famille, context=None):
        if not code_famille:
            return {'value': {'code_famille' : False}}
        else:
            # Vérifions si le code famille existe bien en base de données
            cr.execute('select id from mcisogem_acte_entente_prealable where code_famille=%s', (code_famille,))        
            famille_id = cr.fetchone()[0]
            return {
                    'name':'Actes soumis à entente préalable',
                    'view_type':'form',
                    'form_view_ref':'view_mcisogem_acte_entente_prealable_form',
                    'view_mode':'form',
                    'res_model':'mcisogem.acte.entente.prealable',
                    'view_id':False,
                    'target':'new',
                    'type':'ir.actions.act_window',
                    'context':context,
                    'nodestroy':True,
                    'res_id': famille_id,
                    }

mcisogem_acte_entente_preal()

""" Classe : CONVENTION """ 
class mcisogem_convention(osv.osv):
    _name = "mcisogem.convention"
    _description = 'Convention'
    _columns = {
        'numero_convention': fields.integer('Numéro convention', required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'date_debut_convention': fields.datetime('Date d\'effet', required=True),
        'date_fin_convention': fields.datetime('Date de résiliation'),
        'validite_convention': fields.boolean('Validité'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'description_convention': fields.text('Description', size=30),
        'code_langue': fields.char('code_langue', size=10, required=True),

    }
    
    _defaults = {
        'date_fin_convention': '1900-01-01 00:00:00',
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_convention, self).create(cr, uid, vals, context=context)
    
mcisogem_convention()

""" Classe : SPEC_MED """ 
class mcisogem_spec_med(osv.osv):
    _name = "mcisogem.spec.med"
    _description = 'Spécialités'
    _columns = {
        'libelle_court_spec': fields.char('Libellé court spécialité', size=10, required=True),
        'name': fields.char('Libellé spécialité', size=30, required=True),
        'bl_prescr_autoris': fields.boolean('Prescription autorisée'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'Nbre_ctr': fields.integer('Nbre_ctr'),
        'code_specialite_reserve': fields.boolean('Spécialité reservée'),

    }
    
    _sql_constraints = [('unique_spec_med', 'unique(libelle_court_spec,code_langue)', "Cette spécialité existe déjà !"), ]

    _defaults = {
        'Nbre_ctr': 0,
        'code_spec_reserve': 0,
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_spec_med, self).create(cr, uid, vals, context=context)
    
mcisogem_spec_med()



""" Classe : PRESTAT """ 
class mcisogem_prestat(osv.osv):
    _name = "mcisogem.prestat"
    _description = 'Prestataire'
    _columns = {
        'libelle_court_prestat': fields.char('Libellé court', size=10, required=True),
        'code_ville': fields.many2one('mcisogem.ville', "Ville", required=True),
        'code_specialite': fields.many2one('mcisogem.spec.med', "Spécialité", required=True),
        'nom_prestat': fields.char('Nom', size=100, required=True),
        'prenoms_prestat': fields.char('Prenoms', size=100, required=True),
        'adresse_prestat': fields.char('Adresse', size=60),
        'code_bp_prestat': fields.char('Code postale', size=20),
        'bp_prestat': fields.char('Boite postale', size=20),
        'tel_prestat': fields.char('Boite postale', size=20),
        'tel1_prestat': fields.char('Boite postale', size=20),
        'fax_prestat': fields.char('Fax', size=20),
        'pc_gratuit_prestat': fields.char('pc_gratuit_prestat', size=20),
        'observation_prestat': fields.text('Observation', size=60),
        'regl_centre_prestat' : fields.selection([('C', 'Centre'), ('P', 'Prestataire'), ('A', 'Autre ordre')], 'Paiement à l\'ordre de '),
        'mode_paiement_prestat' : fields.selection([('LC', 'Chèque'), ('ES', 'Espèce'), ('VI', 'Virement bancaire'), ('AU', 'Autre')], 'Mode de paiement'),
        'numero_banque_prestat': fields.char('No banque', size=20),
        'numero_guichet_prestat': fields.char('No guichet', size=20),
        'numero_compte_prestat': fields.char('No Compte', size=20),
        'cle_rib_prestat': fields.char('Clé rib', size=20),
        'cpta_prestat': fields.char('Compte général', size=20),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'email_prestat' : fields.char('Email', size=50),
        'correspondant_prestat' : fields.char('Correspondant', size=150),
        'responsable_prestat' : fields.char('Responsable', size=150),
        'capital' : fields.integer('capital'),
        'code_territoire': fields.many2one('mcisogem.territoire', "Térritoire", required=True),
        'code_commune': fields.many2one('mcisogem.commune', "Commune"),
        'numero_ordre_prestat' : fields.char('Numero ordre', size=30),
        'code_journal' : fields.char('code_journal', size=20),
        'compta_prestat_tiers' : fields.char('Compte tiers', size=50),
        'privilege' : fields.selection([('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], 'Privilège'),
        'activer' : fields.boolean('Activé'),
        'autre_ordre_prestat' : fields.char('Autre ordre', size=100),

    }

    _defaults = {
        'pc_gratuit_prestat': 0,
        'capital': 0,
}
    
    def onchange_code_ville_prestat(self, cr, uid, ids, code_ville, context=None):
            return {'value': {'code_commune' : False}}
    
    def onchange_regl_centre_prestat(self, cr, uid, ids, nom, context=None):
        if not nom:
            return {'value': {'autre_ordre_prestat' : False}}
        if nom:
            return {'value': {'autre_ordre_prestat' : nom}}

    
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Recuperation de la spécialité
        specialite_data = self.pool.get('mcisogem.spec.med').browse(cr, uid, vals['code_specialite'], context=context)
        vals['nom_prestat'] = specialite_data.name
        vals['prenoms_prestat'] = vals['prenoms_prestat'].upper()

        # Recuperation de la plage centre
        # cr.execute('select "id" from "mcisogem_plage_centre" where code_gest=utilisateur_data.code_gest.id order by "id" desc')
        # cr.fetchone()[0]
        # plage_centre_data = self.pool.get('mcisogem.plage.centre').search(cr, uid, [('code_centre','=',vals['nom_prestat'][0]),('code_gest','=',utilisateur_data.code_gest.id)], offset=0, limit=None, order=None, context=None, count=False)
        plage_centre = self.pool.get('mcisogem.plage.centre').search(cr, uid, [('code_centre', '=', vals['nom_prestat'][0]), ('code_gest', '=', utilisateur_data.code_gest.id)], offset=0, limit=None, order=None, context=None, count=False)
        plage_centre_data = self.pool.get('mcisogem.plage.centre').browse(cr, uid, plage_centre[0], context=context)
        vals['libelle_court_prestat'] = vals['nom_prestat'][0] + str(plage_centre_data.code_plage) + str(plage_centre_data.dernier_numero)
        # incrémentation du dernier numero de la plage de centre
        self.pool.get('mcisogem.plage.centre').write(cr, uid, plage_centre_data.id, {'dernier_numero': plage_centre_data.dernier_numero + 1})

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_prestat, self).create(cr, uid, vals, context=context)
   
mcisogem_prestat()



""" Classe : PRATICIEN """ 
class mcisogem_praticien(osv.osv):
    _name = "mcisogem.praticien"
    _description = 'Praticien'
    _inherit = 'mcisogem.prestat'
    _defaults = {
        'pc_gratuit_prestat': 0,
        'capital': 0,
}
    
    def onchange_code_ville_praticien(self, cr, uid, ids, code_ville, context=None):
            return {'value': {'code_commune' : False}}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        vals['nom_prestat'] = vals['nom_prestat'].upper()
        vals['prenoms_prestat'] = vals['prenoms_prestat'].upper()

        # Constitution du code du praticien
        # Recuperation de l'identifiant
        search_ids = self.pool.get("mcisogem.praticien").search(cr, uid, [])
        last_id = 0
        if not search_ids:
            last_id = 1
        else:
            last_id = search_ids and max(search_ids)
            last_id = last_id + 1
        vals['libelle_court_prestat'] = vals['nom_prestat'][0] + vals['prenoms_prestat'][0] + str(last_id)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_praticien, self).create(cr, uid, vals, context=context)
    
mcisogem_praticien()


""" Classe : TYPE_AFF """ 
class mcisogem_type_aff(osv.osv):
    _name = "mcisogem.type.aff"
    _description = 'Type affection'
    _columns = {
        'code_type_affection': fields.integer('Code famille', required=True),
        'libelle_court_affection': fields.char('Libellé court', size=10, required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_type_aff, self).create(cr, uid, vals, context=context)
    
mcisogem_type_aff()



""" Classe : AFFEC """ 
class mcisogem_affec(osv.osv):
    _name = "mcisogem.affec"
    _description = 'Affection'
    _columns = {
        'code_affection': fields.integer('Code affection', required=True),
        'type_affection': fields.many2one('mcisogem.type.aff', "Type d'affection", required=True),
        'libelle_court_affection': fields.char('Libellé court', size=10, required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'observation_affection': fields.text('Observation', size=65),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_affec, self).create(cr, uid, vals, context=context)
    
mcisogem_affec()


""" Classe : LISTE_DENTS """ 
class mcisogem_liste_dents(osv.osv):
    _name = "mcisogem.liste.dents"
    _description = 'Liste dents'
    _columns = {
        'numero_dent': fields.integer('Numéro dent', required=True),
        'name': fields.char('Libellé dent', size=150, required=True),
        'type_dent' : fields.selection([('1', 'Adulte'), ('2', 'Lait')], 'Type de dent'),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_liste_dents, self).create(cr, uid, vals, context=context)
    
mcisogem_liste_dents()


""" Classe : ACTE_ABSENCE_DENTS """ 
class mcisogem_acte_absence_dents(osv.osv):
    _name = "mcisogem.acte.absence.dents"
    _description = 'Acte d\'extraction de dents'
    _columns = {
        'libelle_court_acte': fields.char('Libellé court', size=10, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'code_ext_dent' : fields.boolean('Code d\'extraction'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        return super(mcisogem_acte_absence_dents, self).create(cr, uid, vals, context=context)
    
mcisogem_acte_absence_dents()


""" Classe : SOUS_ACTES """ 
class mcisogem_sous_actes(osv.osv):
    _name = "mcisogem.sous.actes"
    _description = 'Sous Actes'
    _columns = {
        'libelle_court_sous_acte': fields.char('Libellé court', size=20, required=True),
        'code_acte': fields.many2one('mcisogem.nomen.prest', "Acte", required=True),
        'code_famille_acte': fields.many2one('mcisogem.fam.prest', "Famille d'acte", required=True),
        'name': fields.char('Libellé', size=100, required=True),
        'cout_unit_nomen': fields.integer('cout_unit_nomen'),
        'l_cle_nomen': fields.char('Lettre clé', size=3, required=True),
        'mtt_lc_carmed': fields.integer('mtt_lc_carmed'),
        'mtt_lc_hors_carmed': fields.integer('mtt_lc_hors_carmed'),
        'ratio_th_nomen': fields.integer('ratio_th_nomen'),
        'bl_nomen_envig': fields.boolean('Valide'),
        'observation_nomen': fields.text('Observation'),
        'plf_prest_dft': fields.integer('plf_prest_dft'),
        'ticm_dft': fields.integer('ticm_dft'),
        'bl_ticm_tx_dft': fields.integer('bl_ticm_tx_dft'),
        'prest_espece_dft': fields.integer('prest_espece_dft'),
        'plf_an_prest_dft': fields.integer('plf_an_prest_dft'),
        'max_act_an_dft': fields.integer('max_act_an_dft'),
        'bl_envig_carmed': fields.boolean('Valide spécial'),
        'qte_cg': fields.integer('Coefficient centre de gestion'),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    def create(self, cr, uid, vals, context=None):
        # Récuperation de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)

        # Ajout des valeurs par defauts
        vals['code_gest'] = utilisateur_data.code_gest.id
        vals['libelle_gest'] = utilisateur_data.code_gest.name
        vals['code_langue'] = centre_gestion_data.code_langue.code_langue
        return super(mcisogem_sous_actes, self).create(cr, uid, vals, context=context)
    
mcisogem_sous_actes()


class mcisogem_tarif_convention(osv.osv):
    _name = "mcisogem.tarif.convention"
    _description = 'Tarif convention'
    _columns = {
        'code_convention': fields.many2one('mcisogem.convention', "Convention", required=True),
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte", required=True),
        'code_acte': fields.many2one('mcisogem.nomen.prest', "Acte", required=True),
        'montant_brut_tarif': fields.integer('Montant brut tarif', required=True),
        'date_effet_tarif': fields.datetime("Date d'effet", required=True),
        'date_resiliation_tarif': fields.datetime("Date de résiliation", required=True),
        'cod_res_conv': fields.integer('cod_res_conv'),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_gest': fields.many2one('mcisogem.centre.gestion', "Centre de gestion", required=True),
        'libelle_gest' : fields.char('libelle_gest', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),

}

mcisogem_tarif_convention()


class mcisogem_convention_temp(osv.osv):
    _name = "mcisogem.convention.temp"
    _description = 'Convention'
    _columns = {
        'code_convention': fields.many2one('mcisogem.convention', "Convention", required=True),
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte", required=True),
        'code_tarif_convention_temp': fields.many2many('mcisogem.tarif.convention.temp',
                                       'mcisogem_convention_temp_rel',
                                        'convention_temp_id',
                                        'code_convention',
                                        'Choix des actes', required=True),
        'date_effet_tarif': fields.datetime("Date d'effet", required=True),
        'date_resiliation_tarif': fields.datetime("Date de résiliation"),
        
}
    
    _defaults = {
        'date_resiliation_tarif': '1900-01-01 00:00:00',
}
    
    def onchange_code_famille_tarif_convention(self, cr, uid, ids, code_famille, context=None):
        
        #Avant tout on vide la table temporaire des tarifs
        #Vidage des tables temporaires
        cr.execute("delete from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
        
        if not code_famille:
            return {'value': {'code_tarif_convention_temp': False}}
        if code_famille:
            result = []
            #Recuperation de la liste de tous les actes de la famille
            cr.execute("select * from mcisogem_nomen_prest where code_fam_prest=%s", (code_famille,))
            lesactes = cr.dictfetchall()
            if len(lesactes)>0:
               #Insertion de la liste des actes dans la table mcisogem_tarif_convention_temp
               #Parcours de la liste et enregistrement des données en base
               for acte in lesactes:
                   cr.execute("insert into mcisogem_tarif_convention_temp (create_uid,choix,code_famille,code_acte,montant_brut_tarif, write_uid) values(%s, %s, %s, %s, %s, %s)", (uid, False, code_famille, acte['id'],0, uid))
               cr.execute("select * from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
               lestarifstemp = cr.dictfetchall()
               for tarif in lestarifstemp:
                    result.append(tarif['id'])
               return{'value': {'code_tarif_convention_temp': result}}
            else:
                return {'value': {'code_tarif_convention_temp': False}}
    
    def create(self, cr, uid, vals, context=None):
        
        #Recuperation des lignes qui ont été cochées dans la table mcisogem_tarif_convention_temp
        cr.execute("select * from mcisogem_tarif_convention_temp where write_uid=%s and choix=%s", (uid,True))
        lesactes = cr.dictfetchall()
        if len(lesactes)>0:
            
            #Recuperation des valeurs par défaut
            utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest.id, context=context)
            
            #Recuperation de la date du jour
            datedujour = time.strftime('%d-%m-%y %H:%M:%S',time.localtime())
            #Parcours de la liste des actes sélectionné
            for acte in lesactes:
                if not vals['date_resiliation_tarif']:
                    vals['date_resiliation_tarif'] = '1900-01-01 00:00:00'
                cr.execute("""insert into mcisogem_tarif_convention 
                (create_uid, code_convention, cod_res_conv, code_acte, code_famille,  date_effet_tarif, write_uid, montant_brut_tarif, code_gest, 
                libelle_gest, write_date, create_date, code_langue, date_resiliation_tarif)
                 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (uid, vals['code_convention'], 0, acte['code_acte'], acte['code_famille'], vals['date_effet_tarif'], uid, acte['montant_brut_tarif'], utilisateur_data.code_gest.id, utilisateur_data.code_gest.name, datedujour, datedujour, centre_gestion_data.code_langue.code_langue, vals['date_resiliation_tarif']))
            #On vide la table des tarifs temporaires
            cr.execute("delete from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
            return {
                    'name':'Tarif Convention',
                    'view_type':'tree',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.tarif.convention',
                    'view_id':'mcisogem_tarif_convention_tree',
                    'target':'new',
                    'type':'ir.ui.view',
                    'context':context,
                    'nodestroy':True,
                    }
        else:
            raise osv.except_osv('Attention !', "Veillez sélectionner au moins un acte!")
            return True

mcisogem_convention_temp()

class mcisogem_tarif_convention_temp(osv.osv):
    _name = "mcisogem.tarif.convention.temp"
    _description = 'Tarif convention'
    _columns = {
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte", required=True),
        'choix': fields.boolean('Choix'),
        'code_acte': fields.many2one('mcisogem.nomen.prest', "Acte", required=True, readonly=True),
        'montant_brut_tarif': fields.integer('Montant brut tarif', required=True),
}
    
mcisogem_tarif_convention_temp()






