# -*- coding:utf8 -*-
import time

from openerp import SUPERUSER_ID
from openerp.osv import fields
from openerp.osv import osv
from datetime import datetime, timedelta
from openerp import tools
from openerp.tools.translate import _
import openerp
from dateutil.relativedelta import relativedelta
from dateutil import parser
import logging
_logger = logging.getLogger(__name__)

class mcisogem_langue(osv.osv):
    _name = "mcisogem.langue"
    _description = 'Langue'
    
    _columns = {
        'code_langue': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=50, required=True),
        'ph_lib_langue': fields.char('PH Libellé', size=50, required=True),
    }

    
class mcisogem_commune(osv.osv):
    _name = "mcisogem.commune"
    _description = 'Commune'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
        
    
    _columns = {
        'code_commune': fields.char('Code', size=20, required=True),
        'code_ville': fields.many2one('mcisogem.ville', "Code de la ville", required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    

class mcisogem_tranche_age(osv.osv):
    _name = "mcisogem.tranche.age"
    _description = 'Tranche d\'age'
        
    _columns = {
        'code_tranche': fields.integer('code tranche'),
        'debut_tranche': fields.integer('Début tranche'),
        'fin_tranche': fields.integer('Fin tranche'),
        'name': fields.char('affichage'),
    }
    
class mcisogem_numero(osv.osv):
    _name = "mcisogem.numero"
    _description = 'Numéro'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'name': fields.integer('Montant', size=18),
        'num_remb': fields.integer('Montant', size=18),
        'numero': fields.integer('Montant', size=18),
        'num_benef': fields.integer('Montant', size=18),
        'num_police': fields.integer('Montant', size=18),
        'num_prestexec': fields.char('Montant', size=18),
        'num_quittance': fields.integer('Montant', size=18),
        'num_centre': fields.integer('Montant', size=18),
        'num_regl_quittance': fields.integer('Montant', size=18),
        'num_regt': fields.integer('Montant', size=18),
        'num_regt_garant': fields.integer('Montant', size=18),
        'num_remb_garant': fields.integer('Montant', size=18),
        'num_court_souscr': fields.integer('Montant', size=18),
        'num_quittancier': fields.integer('Montant', size=18),
    }
    
class mcisogem_pays(osv.osv):
    _name = "mcisogem.pays"
    _description = 'Pays'

    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name

    _columns = {
        'name': fields.char('Libellé', size=50, required=True),
        'code_pays': fields.char('Code', size=18, required=True),
        'code_langue': fields.char('code_langue', size=10, required=False),
    }
    
    _defaults = {
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_ville(osv.osv):
    _name = "mcisogem.ville"
    _description = 'Ville'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_ville': fields.char('Code', size=18, required=True),
        'name': fields.char('Libellé', size=50, required=True),
        'region_id': fields.many2one('mcisogem.region', 'Région'),
        'zone_geo_id': fields.many2one('mcisogem.zone', 'Zone géographique'),
        'code_postal': fields.integer('Code postal'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }

class mcisogem_zone(osv.osv):
    _name = "mcisogem.zone"
    _description = 'Zone géographique'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_zone_geo': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=50, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_devise(osv.osv):
    _name = "mcisogem.devise"
    _description = 'Devise'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_devise': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'cours_devise_ref': fields.float('Cours par rapport a la devise de reférence', digits=(10, 5)),
        'date_cours_devise': fields.datetime("Date du cours de la devise"),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=False),
        'code_gest': fields.char('libelle_gest', size=50, required=False),
        'code_langue': fields.char('code_langue', size=10, required=False),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_type_garant(osv.osv):
    _name = "mcisogem.type.garant"
    _description = 'Type garant'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_type_garant': fields.char('Code', size=18, required=True),
        'name': fields.char('Libellé', size=50, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=False),
        'code_gest': fields.char('libelle_gest', size=50, required=False),
        'code_langue': fields.char('code_langue', size=10, required=False),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_type_avenant(osv.osv):
    _name = "mcisogem.type.avenant"
    _description = 'Type avenant'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_type_avenant': fields.char('Code', size=5, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_type_contrat(osv.osv):
    _name = "mcisogem.type.contrat"
    _description = 'Type de contrat'

    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_type_contrat': fields.integer('Code', required=True),
        'name': fields.char('Libellé', required=True, size=150),
        'cod_tx_comxion': fields.char('Code tx'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'cod_tx_comxion': 1,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_mode_recond(osv.osv):
    _name = "mcisogem.mod.recond"
    _description = 'Mode de reconduction'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_mod_recond': fields.integer('Code', required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_regime(osv.osv):
    _name = "mcisogem.regime"
    _description = 'Type de remboursement'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_regime': fields.char('Code regime', size=10, required=True),
        'name': fields.char('Libelle regime', size=50),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_concurent(osv.osv):
    _name = "mcisogem.concurent"
    _description = 'Concurents'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_concur': fields.char('Code', size=20, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
      
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_unite_temps(osv.osv):
    _name = "mcisogem.unite.temps"
    _description = 'Unité de temps'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_unite_temps': fields.char('Code', size=1, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'nbre_jour': fields.integer('Nombre de jour'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=False),
        'code_gest': fields.char('libelle_gest', size=50, required=False),
        'code_langue': fields.char('code_langue', size=10, required=False),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }

class mcisogem_territoire(osv.osv):
    _name = "mcisogem.territoire"
    _description = 'Térritoire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_territoire': fields.char('Code', size=30, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=False),
        'code_gest': fields.char('libelle_gest', size=50, required=False),
        'code_langue': fields.char('code_langue', size=10, required=False),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
    
class mcisogem_regroupe_territoire(osv.osv):
    _name = "mcisogem.regroupe.territoire"
    _description = 'Regroupe Térritoire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
        
    
    _columns = {
        'code_regroupe_territoire': fields.char('Code', size=30, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'code_sup': fields.char('Code sup'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_region(osv.osv):
    _name = "mcisogem.region"
    _description = 'Region'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_region': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=50, required=True),
        'pays_id': fields.many2one('mcisogem.pays', "Pays"),
        'zone_geo_id': fields.many2one('mcisogem.zone', "Zone géographique"),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
        
class mcisogem_banque(osv.osv):
    _name = "mcisogem.banque"
    _description = 'Banque'    
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_banque': fields.char('Code de la banque', size=30, required=True),
        'name': fields.char('Libelle banque', size=100),
        'telephone1': fields.char('Tel', size=18),
        'fax': fields.char('Fax', size=18),
        'gestionnaire_banque': fields.char('Gestionnaire de la banque', size=20),
        'boite_postale': fields.char('Boite postale', size=50),
        'telephone2': fields.char('Tel portable', size=18),
        'adresse': fields.char('Adresse geographique', size=100),
        'date_cloture': fields.datetime("Date de cloture"),
        'cpta_banque': fields.char('Swift code', size=50),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'date_cloture': '1900-01-01 00:00:00',
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }

class mcisogem_courtier(osv.osv):
    _name = "mcisogem.courtier"
    _description = 'Courtier'    
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_courtier': fields.char('Code', size=10, required=True),
        'name': fields.char('Désignation', size=150, required=True),
        'ville_id': fields.many2one('mcisogem.ville', 'Ville', required=True),
        'adresse': fields.char('Adresse', size=150),
        'mail': fields.char('Email', size=50),
        'code_bp': fields.integer('Code BP'),
        'boite_postale': fields.integer('Boite postale'),
        'telephone': fields.char('Téléphone', size=18),
        'fax': fields.char('Fax', size=50),
        'observation': fields.text('Observations', size=20),
        'statut_social': fields.selection([('1', 'Personne physique'), ('2', 'Personne morale')], 'Statut juridique'),
        'Seq_deb_num_pol': fields.integer('deb num police'),
        'Seq_fin_num_pol': fields.integer('deb fin police'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'Seq_deb_num_pol': 0,
        'Seq_fin_num_pol': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
        
class mcisogem_motif_suspen(osv.osv):
    _name = "mcisogem.motif.suspen"
    _description = 'Motif Liste Noire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_motif': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=30),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_exercice(osv.osv):
    _name = "mcisogem.exercice"
    _description = 'Exercice'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'date_debut': fields.date('Date debut', required=True),
        'date_fin': fields.date('Date fin', required=True),
        'name': fields.char('Libelle exercice', size=150),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class mcisogem_avenant(osv.osv):
    _name = "mcisogem.avenant"
    _description = 'Avenant'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
        
    
    _columns = {
        'type_avenant_id': fields.many2one('mcisogem.type.avenant', 'Type avenant', required=True),
        'name': fields.char(''),
        'police_id': fields.many2one('mcisogem.police', 'Police', required=True),
        'souscripteur_police': fields.many2one('mcisogem.souscripteur', 'Souscripteur', required=True, readonly=True),
        'num_ave_interne_police': fields.integer('Numéro avenant police', readonly=True),
        'calc_prime_ave': fields.selection([('1', 'Avec calcul de prime'), ('0', 'Sans calcul de prime')], 'Mode de calcul'),
        'dt_eff_mod_pol': fields.date('Date émission'),
        'dt_ope_deb_ave': fields.date('Periode motif du'),
        'dt_ope_fin_ave': fields.date('Au'),
        'periode_mvmt_du': fields.date('Periode mouvement du'),
        'periode_mvt_au': fields.date('Au'),
        'dt_deb_exercice_pol': fields.date('Exercice du', readonly=True),
        'dt_fin_exercice_pol': fields.date('Au', readonly=True),
        'date_effet_prime': fields.datetime('Date éffet prime', readonly=True),
        'date_effet_police': fields.date('Date éffet police', readonly=True),
        'valider': fields.boolean('Valider'),
        'annuler': fields.boolean('Annuler'),
        'date_annuler': fields.datetime('le'),
        'dt': fields.boolean(''),
        
        'mnt_regl_prime_ave': fields.integer('t'),
        'mnt_emi_ave': fields.integer('t'),
        'dt_anul_ave': fields.datetime('t'),
        'mnt_quitance_emi': fields.integer('t'),
        'code_avenant_initial': fields.integer('t'),
        'mnt_echea_paiemt': fields.integer('t'),
        'dt_fin_ave': fields.date('t'),
        'prime_cal_ave': fields.char('t'),
        'nbre_echea_paiemt': fields.char('t'),
        'cod_avenant_initial': fields.integer('t'),
        'mnt_echea_paiemt': fields.integer('t'),
        
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        
        'state': fields.selection([
            ('draft', "Nouveau"),
            ('valid', "Valider"),
            ('anul', "Annuler"),
        ])
    }
    
    def onchange_annule(self, cr, uid, ids, annuler, context=None):
        if annuler == False:
            return {'value': {'dt': False}}
        else:
            return {'value': {'dt': True}}
    
    def onchange_type_avenant_id(self, cr, uid, ids, type_avenant_id, context=None):
        vals = {}
        if not type_avenant_id:
            return {'value': {'name': False}}
        else:
            obj_ave_data = self.pool.get('mcisogem.type.avenant').browse(cr, uid, type_avenant_id, context=context)
            vals = { 'name': obj_ave_data.code_type_avenant }
        return {'value':vals}
    
    def onchange_police(self, cr, uid, ids, police_id, context=None):
        vals = {}
        if not police_id:
            return {'value': {'libelle_police': False}}
        else:
            obj_police_data = self.pool.get('mcisogem.police').browse(cr, uid, police_id, context=context)
            datedujour = time.strftime("%Y-%m-%d", time.localtime())
            vals = {'souscripteur_police': obj_police_data.souscripteur_id,
                    'num_ave_interne_police': obj_police_data.num_ave_interne_police,
                    'dt_deb_exercice_pol': obj_police_data.dt_deb_exercice,
                    'dt_fin_exercice_pol': obj_police_data.dt_fin_exercice,
                    'dt_eff_mod_pol': obj_police_data.dt_fin_exercice,
                    'periode_mvt_au': obj_police_data.dt_fin_exercice,
                    'date_effet_police':obj_police_data.dt_deb_exercice,
                    'dt_eff_mod_pol':datedujour,
                    'dt_ope_fin_ave':obj_police_data.dt_fin_exercice}
        return {'value':vals}
    
    def _get_context(self, cr, uid, context):
        context = context or {}
        return context.get('police')
    
    
    _defaults = {
        'police_id' : _get_context,
        'date_effet_prime' : '1900-01-01 00:00:00',
        'state': 'draft',
        'dt_eff_mod_pol': lambda *a: time.strftime("%Y-%m-%d"),
        'dt_ope_deb_ave': lambda *a: time.strftime("%Y-%m-%d"),
        'periode_mvmt_du': lambda *a: time.strftime("%Y-%m-%d"),
        'mnt_regl_prime_ave': 0,
        'mnt_emi_ave': 0,
        'dt_anul_ave' : '1900-01-01 00:00:00',
        'mnt_echea_paiemt': 0,
        'mnt_quitance_emi': 0,
        'code_avenant_initial': 0,
        'prime_cal_ave': 0,
        'nbre_echea_paiemt': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        'date_annuler' : '1900-01-01 00:00:00',
        'calc_prime_ave' : '1',
    }
    
    def button_to_valid(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'valid'}, context=context)
    
    def button_to_anul(self, cr, uid, ids, data, context=None):
        return self.write(cr, uid, ids, data, {'state' : 'anul'}, context=context)
    
    def _check_date_mvt(self, cr, uid, ids, context=None):
        for val in self.read(cr, uid, ids, ['periode_mvmt_du'], context=context):
            if val['periode_mvmt_du']:
                if val['periode_mvmt_du'] > val['periode_mvt_au']:
                    return False
                
    def _check_date_modif(self, cr, uid, ids, context=None):
        for val in self.read(cr, uid, ids, ['dt_ope_deb_ave'], context=context):
            if val['dt_ope_deb_ave']:
                if val['dt_ope_deb_ave'] > val['dt_ope_fin_ave']:
                    return False
                
    def _check_date_emission(self, cr, uid, ids, context=None):
        for val in self.read(cr, uid, ids, ['dt_eff_mod_pol'], context=context):
            if val['dt_eff_mod_pol']:
                if val['dt_eff_mod_pol'] > val['dt_ope_fin_ave']:
                    return False
    
    def button_to_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        return True
          
    def create(self, cr, uid, data, context=None):
        # Recuperation de l'exercice de police
        cr.execute("select * from mcisogem_exercice_police where police_id=%s order by id desc", (data['police_id'],))
        lesexopolice = cr.dictfetchall()
        
        if len(lesexopolice) > 0:
            
            exercice_police = lesexopolice[0]
            
            # Recuperation de l'avenant sélectionné
            cr.execute("select * from mcisogem_avenant where state !=%s and police_id=%s", (data['type_avenant_id'], 'valid', data['police_id']))
            lesavenants = cr.dictfetchall()
            
            if len(lesavenants) > 0:
                raise osv.except_osv('Attention !', "La police a déjà un avenant du même type non valide. Validez l'ancienne avant de créer un nouveau !")
                return False
            else:
                
                # Controle sur les dates
                if (data['dt_ope_deb_ave'] < data['dt_ope_fin_ave']) and (data['dt_ope_deb_ave'] >= exercice_police['date_debut_exercice']) and (data['dt_ope_fin_ave'] <= exercice_police['date_fin_exercice']) :
                    if (data['periode_mvmt_du'] < data['periode_mvt_au']) and (data['periode_mvmt_du'] >= exercice_police['date_debut_exercice']) and (data['periode_mvt_au'] <= exercice_police['date_fin_exercice']):
                        # Recuperation du dernier avenant de la police
                        cr.execute("select * from mcisogem_avenant where police_id=%s order by id desc" , (data['police_id'],))
                        avenant = cr.dictfetchall()[0]
                        data['num_ave_interne_police'] = avenant['num_ave_interne_police'] + 1
                        data['souscripteur_police'] = avenant['souscripteur_police']
                        data['dt_deb_exercice_pol'] = exercice_police['date_debut_exercice']
                        data['dt_fin_exercice_pol'] = exercice_police['date_fin_exercice']
                        data['date_effet_police'] = exercice_police['date_debut_exercice']
                        res = super(mcisogem_avenant, self).create(cr, uid, data, context=context)
                        return res 
                    else:
                        raise osv.except_osv('Attention !', "La date de début de la période de mouvement doit être supérieur à la date de fin et compris dans l'exercice de la police !")
                        return False  
                else:
                    raise osv.except_osv('Attention !', "La date de début de la période de modification doit être supérieur à la date de fin et compris dans l'exercice de la police !")
                    return False                
            
        else:
            raise osv.except_osv('Attention !', "Cette police ne possède pas d'exercice de police !")

    
class mcisogem_college(osv.osv):
    _name = "mcisogem.college"
    _description = 'Collège'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_college': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
class res_users(osv.osv):
    _inherit = 'res.users'
    _columns = {
        'poste': fields.char('Poste', size=18),
        'code_gest_id': fields.many2one('mcisogem.centre.gestion')
    }
    
class mcisogem_centre_gestion(osv.osv):
    _name = "mcisogem.centre.gestion"
    _description = 'Centre de gestion'
    
    _columns = {
        'name': fields.char('Libellé', size=50),
        'code_centre': fields.char('Code', size=10, required=True),
        'devise_id': fields.many2one('mcisogem.devise', "Devise"),
        'langue_id': fields.many2one('mcisogem.langue', "Langue", required=True),
        'pays_id': fields.many2one('mcisogem.pays', "Pays"),
        'territoire_id': fields.many2one('mcisogem.territoire', "Territoire"),
        'cod_sup': fields.boolean('Module sous actes'),
    }
    
class mcisogem_plage_type_garant(osv.osv):
  
    _name = "mcisogem.plage.type.garant"
    _description = 'Plage type garant'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id 
    
    _columns = {
        'name': fields.integer('Code plage', required=True),
        'code_type_garant': fields.many2one('mcisogem.type.garant', "Type de garant"),
        'debut_plage_type_garant': fields.integer('Début plage', required=True),
        'fin_plage_type_garant': fields.integer('Fin plage', required=True),
        'dernier_numero_attribue': fields.integer('Dernier Numéro attribué', readonly=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'affichage': fields.integer('affichage',),
    }
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'dernier_numero_attribue' : 0,
        'affichage' : 0,
    }
    
    def create(self, cr, uid, vals, context=None):
        vals['dernier_numero_attribue'] = vals['debut_plage_type_garant']
        vals['affichage'] = 1
        return super(mcisogem_plage_type_garant, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        # Recuperation des données
        plage_type_data = self.pool.get('mcisogem.plage.type.garant').browse(cr, uid, ids, context=context)
        if vals['fin_plage_type_garant'] < plage_type_data.dernier_numero_attribue:
            raise osv.except_osv('Attention !', "La fin de la plage doit être supérieure ou égale au dernier numéro attribué pour cette plage !")
            return False
        else:
            return super(mcisogem_plage_type_garant, self).write(cr, uid, ids, vals, context=context) 
    
class mcisogem_garant(osv.osv):
    _name = "mcisogem.garant"
    _description = 'Garant'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, ids, name, value, args, context=None):
        return self.write(cr, uid, ids, {'image': tools.image_resize_image_big(value)}, context=context)
    
    _columns = {
        'code_garant': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'ville_id': fields.many2one('mcisogem.ville', 'Ville', required=True),
        'type_garant_id': fields.many2one('mcisogem.type.garant', 'Type garant', required=True),
        'adresse_garant': fields.char('Adresse', size=150),
        'code_boite_postale': fields.integer('Code Boîte postale'),
        'boite_postale': fields.integer('Boite postale'),
        'telephone_garant': fields.char('Téléphone', size=50),
        'fax_garant': fields.char('Fax', size=50),
        'email_garant': fields.char('Email', size=50),
        'correspondant': fields.char('Correspondant', size=150),
        'responsable': fields.char('Responsable', size=150),
        'capital': fields.integer('Capital'),
        'observation': fields.text('Observation', size=250),
        'debut_num_pol': fields.integer('Debut numéro police'),
        'fin_num_pol': fields.integer('Fin numéro police'),
        'st_assur': fields.integer('St assur'),
        'image': fields.binary("Image",
            help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'mcisogem.garant': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of the product. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved, "\
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'mcisogem.garant': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of the product. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        
        'cpta_assur': fields.char('Compte assureur', size=20),
        'cpta_assur_commission': fields.char('Compte assureur commission'),
        'cpta_assur_taxe': fields.char('Compte assureur taxe', size=20),
        'cpta_prime': fields.char('Compte prime', size=20),
        'num_plage_type_garant': fields.integer('Numero plage type'),
        'cpta_assur_rd': fields.char('Compte assureur ref', size=20),
        'cpta_assurtier': fields.char('Compte assurtier', size=50),
        'libelle_cpta_assurtiers_rd': fields.char('Libellé compte assurtier', size=50),
        
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'show_chp': fields.boolean(''),
             
        'state': fields.selection([
            ('draft', "Nouveau"),
            ('sent', "Comptabilité"),
            ('done', "Informations Comptable"),
            ('cancel', "Annuler"),
            ('finish', "Terminer"),
        ], 'Status', required=True, readonly=True)
    }
    
    def _get_group(self, cr, uid, context=None):
        cr.execute('select gid from res_groups_users_rel where uid=%s', (uid,))
        group_id = cr.fetchone()[0]
        group_obj = self.pool.get('res.groups').browse(cr, uid, group_id, context=context)
        if group_obj.name == 'Financial Manager':
            return True
        else:
            return False
    
    _defaults = {
        'debut_num_pol' : 0,
        'fin_num_pol': 0,
        'st_assur': 1,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        'state' : 'draft',
        'show_chp' : _get_group
    }
    
    def button_to_sent(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state':'done'}, context=context)
    
    def button_to_done(self, cr, uid, ids, data, context=None):
        if not data['cpta_assur'] in data or not data['cpta_assur_commission'] in data:
            e_mess = "Veuillez renseigner les infos comptable avant la validation"
            raise osv.except_osv(_('Erreur'), _(e_mess))
        else:
            self.write(cr, uid, ids, data, {'state' : 'finish'}, context=context)
        return True
    
    def button_to_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        return True
    
    def create(self, cr, uid, vals, context=None):
        # Détermination du dernier numéro de la plage type garant
        cr.execute("select * from mcisogem_plage_type_garant where code_type_garant=%s order by id desc", (vals['type_garant_id'],))
        lesplages = cr.dictfetchall()
        if len(lesplages) > 0:
            laplage = lesplages[0]
            dernier_numero = laplage['dernier_numero_attribue']
            vals['num_plage_type_garant'] = dernier_numero
            dernier_numero = dernier_numero + 1
            cr.execute("update mcisogem_plage_type_garant set dernier_numero_attribue=%s where id=%s", (dernier_numero, laplage['id']))
            
            # Workflow vers la comptabilité
            vals['state'] = 'done'

            
            return super(mcisogem_garant, self).create(cr, uid, vals, context=context)    
        else:
            raise osv.except_osv('Attention !', "Aucune plage type garant n'a été trouvé pour ce type de garant. Veuillez procéder à la création d'une plage !")
            return False;
    
    
class mcisogem_souscripteur(osv.osv):
    _name = "mcisogem.souscripteur"
    _description = 'Souscripteur'
    PAIEM_SELECTION = [
        ('cheque', 'Chèque'),
        ('espece', 'Espèce'),
        ('virement', 'Virement'),
        ('autres', 'Autres')
    ]
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, ids, name, value, args, context=None):
        return self.write(cr, uid, ids, {'image': tools.image_resize_image_big(value)}, context=context)
    
    _columns = {
        'name': fields.char('Libellé', size=100, required=True),
        'ville_id': fields.many2one('mcisogem.ville', 'Ville', required=True),
        'adresse_souscripteur': fields.char('Adresse', size=60),
        'code_boite_postale': fields.integer('Code Boite postale'),
        'boite_postale': fields.integer('Boite postale'),
        'telephone': fields.char('Téléphone', size=30),
        'fax': fields.char('Fax', size=30),
        'email': fields.char('Email', size=50),
        
        'image': fields.binary("Image",
            help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'mcisogem.souscripteur': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of the product. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved, "\
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'mcisogem.souscripteur': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of the product. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        
        'banque_id': fields.many2one('mcisogem.banque', 'Banque'),
        'mod_paiem': fields.selection(PAIEM_SELECTION, 'Mode de paiement', select=True),
        'num_compte': fields.char('Numéro Compte', size=30),
        'num_guichet': fields.char('Numéro Guichet', size=30),
        'num_compte_interne': fields.char('Numero Compte interne', size=30),
        'cle_rib': fields.char('Cle R.I.B.', size=30),
        'mass_sal_souscr': fields.char('mass sal souscr'),
        
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=False),
        
        'affiche': fields.boolean(''),
              
        'state': fields.selection([
            ('draft', "Nouveau"),
            ('sent', "Comptabilité"),
            ('done', "Informations Comptable"),
            ('cancel', "Annuler"),
            ('finish', "Terminer"),
        ], 'Status', required=True, readonly=True)
    }
    
    def _get_group(self, cr, uid, context=None):
        cr.execute('select gid from res_groups_users_rel where uid=%s', (uid,))
        group_id = cr.fetchone()[0]
        group_obj = self.pool.get('res.groups').browse(cr, uid, group_id, context=context)
        if group_obj.name == 'Financial Manager':
            return True
        else:
            return False
    
    _defaults = {
        'mass_sal_souscr' : 0,
        'state' : 'draft',
        'mod_paiem' : 'cheque',
        'affiche' : _get_group,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
    def button2_to_sent(self, cr, uid, ids, context=None):
        """L utilisateur envoi la requete a la comptabilite pour ajouter les informations comptable"""
        # souscripteur = self.pool.get('mcisogem.souscripteur').browse(cr, uid, uid, context=context)
        # usr = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        message = 'Un souscripteur a ete créer veuillez renseigner les informations comptable'
        
        cr.execute('select id from res_groups where name=%s', ('Settings',))
        group_id = cr.fetchone()[0]
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        ident_centre = cr.fetchone()[0]
        res_users = self.pool('res.users')
        user_ids = res_users.search(
            cr, SUPERUSER_ID, [
                ('code_gest_id', '=', ident_centre),
                ('groups_id', 'in', group_id)
            ], context=context)     
        partner_id = []
        
        if user_ids:
            partner = self.pool.get('res.partner').browse(cr, uid, uid, context=context) 
            partner_id = list(set(u.partner_id.id for u in res_users.browse(cr, SUPERUSER_ID, user_ids, context=context)))
            partner.message_post(cr, uid, False,
                                 body=message,
                                 partner_ids=partner_id,
                                 subtype='mail.mt_comment', context=context
            )            
        return self.write(cr, uid, ids, {'state':'done'}, context=context)
    
    def button2_to_done(self, cr, uid, ids, context=None):
        """La comptabilite renseigne et valide les informations comptable"""
        compta = self.read(cr, uid, ids, ['banque_id', 'num_guichet', 'num_compte', \
                        'num_compte_interne', 'cle_rib'])        
        if not compta['banque_id'] or not compta['num_guichet'] or not compta['num_compte'] or not compta['num_compte_interne'] or not compta['cle_rib']:
            raise osv.except_osv('Attention !', "Vous devez renseigner tous les champs comptable avant de valider!")
            return False;
        self.write(cr, uid, ids, {'state':'finish'}, context=context)
        return True
    
    def button2_to_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        return True 
    
    def create(self, cr, uid, vals, context=None):
        vals['state'] = 'done'
        return super(mcisogem_souscripteur, self).create(cr, uid, vals, context)   
    
class mcisogem_police(osv.osv):
    _name = "mcisogem.police"
    _description = 'Police'
    REMB_SELECTION = [
        ('S', 'Souscripteur'),
        ('A', 'Assuré principal'),
        ('Aut', 'Autre')
    ]

    _columns = {
        'num_interne_police': fields.integer('Numéro interne de police', readonly=True),
        'num_police': fields.integer('t', required=False),
        'statut_police': fields.integer('Statut police'),
        'name': fields.char('Libellé', required=True),
        'num_ave_interne_police': fields.integer('Numéro avenant interne police'),
        'remb_souscr_assure': fields.selection(REMB_SELECTION, 'Remboursement souscripteur', required=True),
        'remb_autre': fields.char('Autre mode de remboursement'),
        'exercice_id': fields.many2one('mcisogem.exercice', 'Exercice', required=True),
        'dt_deb_exercice': fields.date('Début', readonly=True),
        'dt_fin_exercice': fields.date('Fin', readonly=True),
        'dt_effet': fields.date('Date d\'éffet'),
        'dt_expiration': fields.date('Date d\'expiration'),
        'num_police_assur': fields.integer('Numéro police assureur'),
        'num_pol_remplacee': fields.integer('Numéro police remplacée'),
        'type_contrat_id': fields.many2one('mcisogem.type.contrat', 'Type de contrat', required=True),
        'mod_recond_id': fields.many2one('mcisogem.mod.recond', 'Mode de reconduction', required=True),
        'territoire_id': fields.many2one('mcisogem.territoire', 'Térritorialité', required=True),
        'souscripteur_id': fields.many2one('mcisogem.souscripteur', 'Souscripteur', required=True),
        'souscripteur_pol': fields.char(''),
        'garant_id': fields.many2one('mcisogem.garant', 'Assureur', required=True),
        'courtier_id': fields.many2one('mcisogem.courtier', 'Intermédiaire', required=True),
        'code_regime': fields.many2one('mcisogem.regime', 'Type de remboursement', required=True),
        'periode_ferme_pol': fields.integer('Période ferme'),
        'dt_resil_pol': fields.date('Date de résiliation'),
        'cpta_pol': fields.integer('Compte interne'),
        'concurent_id': fields.many2one('mcisogem.concurent', 'Concurent'),
        
        'code_avenant_initial': fields.integer('Code avenant initiale'),
        'dt_emi_ave': fields.date('Exercice du'),
        'dt_fin_ave': fields.date('Au'),
        'typ_ave': fields.char('Type avenant'),
        'mnt_emi_ave': fields.integer('t'),
        'dt_eff_prime': fields.datetime('t'),
        'mnt_regl_prime_ave': fields.integer('t'),
        'cod_annul_ave': fields.integer('t'),
        'cod_avenant_initial': fields.integer('t'),
        'mnt_regl_prime_ave': fields.integer('t'),
        'calc_prime_ave': fields.integer('t'),
        'tva_oui_non': fields.boolean('Tva'),
        
        'imputation_acc_cie': fields.boolean('Accessoire compagnie'),
        'imputation_acc_courtier': fields.boolean('Accessoire courtier'),
        'type_prime': fields.selection([('1', 'Statut de bénéficiaire'), ('2', 'Tranche d\'age')], 'Enregistrement prime par', required=True),
        'repartition_prime': fields.selection([('1', 'Mois'), ('2', 'Jour')], 'Repartition prime'),
        'typ_prime': fields.selection([(1, 'Police'), (2, 'Collège'), (3, 'Famille'), (4, 'Bénéficiaire') , (5, 'Souscripteur')], 'typ_prime', required=True),
        'bl_exercice_clo': fields.integer('t'),
        'prime_pol_exercice': fields.integer('t'),
        'num_exercice_pol': fields.integer('t'),
        'masse_sal_pol': fields.integer('t'),
        'pc_masse_sal_pol': fields.integer('t'),
        'periodicite_paiem': fields.many2one('mcisogem.unite.temps', 'Périodicité paiement prime'),
           
        'afiche': fields.boolean('t'),
        'remb': fields.boolean('t'),
        
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        
        'state': fields.selection([
            ('draft', "Actif"),
            ('resil', "Resilier"),
            ('lnoir', "Liste noire"),
            ('cancel', "Annuler"),
        ], 'Status', required=True, readonly=True)
    }
    

    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id

    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        'statut_police': 0,
        'state' : 'draft',
        'typ_ave': 'AI',
        'mnt_emi_ave': 0,
        'cod_annul_ave': 0,
        'dt_eff_prime': '1900-01-01 00:00:00',
        'mnt_regl_prime_ave': 0,
        'calc_prime_ave': 0,
        'cod_avenant_initial': 0,
        'num_ave_interne_police': 1,
        'afiche': False,
        'typ_prime': 1,
        'type_prime': '1',
        'periodicite_paiem': '1',
        'repartition_prime' : '1',
        'dt_resil_pol': '1900-01-01 00:00:00',
        
    }
    
    def onchange_remb(self, cr, uid, ids, remb_souscr_assure, context=None):
        if remb_souscr_assure == 'Aut':
            return {'value': {'remb': False}}
        else:
            return {'value': {'remb': True}}
    
    def onchange_exercice(self, cr, uid, ids, exercice_id):
        v = {}
        if exercice_id:
            exercice = self.pool.get('mcisogem.exercice').search(cr, uid, [('id', '=', exercice_id)])
            for exercice_data in self.pool.get('mcisogem.exercice').browse(cr, uid, exercice):
                v = { 'dt_deb_exercice': exercice_data.date_debut, 'dt_fin_exercice': exercice_data.date_fin, 'dt_effet': exercice_data.date_debut, 'dt_expiration': exercice_data.date_fin,
                     'dt_emi_ave': exercice_data.date_debut, 'dt_fin_ave': exercice_data.date_fin}
        return{'value':v}
        
    def button_to_resil(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'resil'}, context=context)
        return True 
    
    def button_to_lnoire(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'lnoir'}, context=context)
        return True 
    
    def button_to_annuler(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'draft'}, context=context)
        return True 
        
    def onchange_souscr(self, cr, uid, ids, souscripteur_id):
        v = {}
        if souscripteur_id:
            souscr = self.pool.get('mcisogem.souscripteur').search(cr, uid, [('id', '=', souscripteur_id)])
            for souscr_data in self.pool.get('mcisogem.souscripteur').browse(cr, uid, souscr):
                v = { 'souscripteur_pol': souscr_data.name}
        return{'value':v}
    
    def create(self, cr, uid, data, context=None):
        
        # Recuperation du centre de gestiob et de l'utilisateur
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest_id.id, context=context)
        
        # Recuperation de la date de debut et de fin de l'exercice
        cr.execute('select date_debut from mcisogem_exercice where id=%s', (data['exercice_id'],)) 
        dtdeb = cr.fetchone()[0]
        cr.execute('select date_fin from mcisogem_exercice where id=%s', (data['exercice_id'],)) 
        dfin = cr.fetchone()[0]
        data['dt_deb_exercice'] = dtdeb
        data['dt_fin_exercice'] = dfin
        
        # Recuperation du numero interne de police et insertion de la police en base de données
        cr.execute("select id,num_police from mcisogem_numero")
        numero = cr.dictfetchall()[0]
        dernier_num = numero['num_police'] + 1
        data['num_interne_police'] = dernier_num
        data['num_police'] = dernier_num
        res = super(mcisogem_police, self).create(cr, uid, data, context)
        
        # Mise a jour des numeros dans la table des numéros         
        cr.execute("update mcisogem_numero set num_police=%s", (dernier_num,))
        
        datedujour = time.strftime('%d-%m-%y %H:%M:%S', time.localtime())
                
        # Création de l'exercice de police
        exopolice = {}
        if data['repartition_prime'] == '1':
            exopolice['repartition_prime'] = 1
        else:
            exopolice['repartition_prime'] = 0
            
        if data['type_prime'] == '1':
            exopolice['type_prime'] = 1
        else:
            exopolice['type_prime'] = 2

        cr.execute("""insert into mcisogem_exercice_police
        (police_id,name,num_interne_police,exercice_id,date_debut_exercice,date_fin_exercice,bl_exercice_clot,tva_oui_non,repartition_prime,type_prime,
        periodicite_paiem_pol,code_gest,ident_centre,code_langue,dernier_avenant, create_uid, write_uid, write_date, create_date,
        prime_pol_exercice,cum_mnt_pol,masse_sal_pol,pc_masse_sal_pol,bl_pc_masse_sal_pol,rapport_sp_preced,tot_sinistre_preced,tot_prime_preced) values
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (res, data['name'],dernier_num, data['exercice_id'], data['dt_deb_exercice'], data['dt_fin_exercice'], False, False, exopolice['repartition_prime'],
         data['type_prime'], data['periodicite_paiem'], utilisateur_data.code_gest_id.name, utilisateur_data.code_gest_id.id,
         centre_gestion_data.langue_id.name, 0, uid, uid, datedujour, datedujour, 0, 0, 0, 0, 0, 0, 0, 0))

        if res:
            # Tentative de recuperation du type avenant AI (Avenant initial)
            if not self.pool.get('mcisogem.type.avenant').search(cr, uid, [('code_type_avenant', '=', 'AI')]):
                # cr.execute('select id from mcisogem_police where id=%s', (res,)) 
                num = res
                # QUESTION : A QUOI SERT souscripteur_pol
                cr.execute('select souscripteur_id from mcisogem_police where id=%s', (res,)) 
                souscripteur_pol = cr.fetchone()[0]
                
                # L'avenant initial n'existe pas on procede a sa creation
                cr.execute("INSERT INTO mcisogem_type_avenant (code_type_avenant, name, code_gest, ident_centre, create_uid, write_uid, create_date, write_date, code_langue ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", ('AI', 'Avenant initial', utilisateur_data.code_gest_id.name, utilisateur_data.code_gest_id.id, uid, uid, datedujour, datedujour, centre_gestion_data.langue_id.code_langue))
                cr.execute('select id from mcisogem_type_avenant where code_type_avenant=%s', ('AI',)) 
                ai = cr.fetchone()[0]
                
                cr.execute("""INSERT INTO mcisogem_avenant (code_avenant_initial, type_avenant_id, dt_deb_exercice_pol, dt_fin_exercice_pol,
                 name, mnt_emi_ave, num_ave_interne_police, mnt_regl_prime_ave, calc_prime_ave, police_id, souscripteur_police, state,
                  code_gest, ident_centre, code_langue, create_uid, write_uid, create_date, write_date, date_effet_prime, dt_eff_mod_pol,
                  dt_ope_deb_ave,periode_mvmt_du, dt_anul_ave,mnt_echea_paiemt,mnt_quitance_emi,prime_cal_ave,nbre_echea_paiemt,date_annuler,
                  dt_fin_ave,dt_ope_fin_ave, valider, date_effet_police)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                , (0, ai, dtdeb, dfin, 'AI', 0, 0, 0, 1, res, souscripteur_pol, 'draft', utilisateur_data.code_gest_id.name,
                    utilisateur_data.code_gest_id.id, centre_gestion_data.langue_id.code_langue, uid, uid, datedujour, datedujour,
                    '1900-01-01 00:00:00', datedujour, dtdeb, datedujour, '1900-01-01 00:00:00', 0, 0, 0, 0, '1900-01-01 00:00:00', dfin, dfin, False, dtdeb))
     
            else:
                cr.execute('select id from mcisogem_type_avenant where code_type_avenant=%s', ('AI',))
                ai = cr.fetchone()[0]
                
                # QUESTION A QUOI SERT souscripteur_pol
                cr.execute('select souscripteur_id from mcisogem_police where id=%s', (res,)) 
                souscripteur_pol = cr.fetchone()[0]
                
                # Création de l'avenant de la police
                cr.execute("""INSERT INTO mcisogem_avenant (code_avenant_initial, type_avenant_id, dt_deb_exercice_pol, dt_fin_exercice_pol,
                 name, mnt_emi_ave, num_ave_interne_police, mnt_regl_prime_ave, calc_prime_ave, police_id, souscripteur_police, state,
                  code_gest, ident_centre, code_langue, create_uid, write_uid, create_date, write_date, date_effet_prime, dt_eff_mod_pol,
                  dt_ope_deb_ave,periode_mvmt_du, dt_anul_ave,mnt_echea_paiemt,mnt_quitance_emi,prime_cal_ave,nbre_echea_paiemt,date_annuler,
                  dt_fin_ave,dt_ope_fin_ave, valider,date_effet_police)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                , (0, ai, dtdeb, dfin, 'AI', 0, 0, 0, 1, res, souscripteur_pol, 'draft', utilisateur_data.code_gest_id.name,
                    utilisateur_data.code_gest_id.id, centre_gestion_data.langue_id.code_langue, uid, uid, datedujour, datedujour,
                    '1900-01-01 00:00:00', datedujour, dtdeb, datedujour, '1900-01-01 00:00:00', 0, 0, 0, 0, '1900-01-01 00:00:00', dfin, dfin, False, dtdeb))
     
        else:
            raise osv.except_osv('Attention !', "L'avenant initiale n'a pas été crée!")
        return res
    
    def button_to_histo_police(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['tree_view_ref'] = 'mcisogem_histo_police_tree'
        ctx['form_view_ref'] = 'view_mcisogem_histo_police_form'
        if ctx['police'] :
            return {
                    'name':'Historique police',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.histo.police',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('num_police', '=', police_data.num_interne_police)],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True

    def button_to_histo_prime(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['tree_view_ref'] = 'mcisogem_histo_prime_tree'
        ctx['form_view_ref'] = 'view_mcisogem_histo_prime_form'
        if ctx['police'] :
            return {
                    'name':'Historique prime',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.histo.prime',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('police_id', '=', police_data.id)],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True

    def button_to_bareme_pol(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['tree_view_ref'] = 'mcisogem_bareme_tree'
        ctx['form_view_ref'] = 'mcisogem_bareme_form'
        if ctx['police'] :
            return {
                    'name':'Barème police',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.bareme',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('police_id', '=', police_data.id)],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True

    def button_to_exercice_pol(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['tree_view_ref'] = 'mcisogem_exercice_police_tree'
        ctx['form_view_ref'] = 'view_mcisogem_exercice_police_form'
        if ctx['police'] :
            return {
                    'name':'Exercice police',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.exercice.police',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('police_id', '=', police_data.id)],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True
    
    def button_to_avenant(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['tree_view_ref'] = 'mcisogem_avenant_tree'
        ctx['form_view_ref'] = 'view_mcisogem_avenant2_form'
        if ctx['police'] :
            return {
                    'name':'Avenant',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.avenant',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('police_id', '=', police_data.id)],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True

    def button_to_college(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['tree_view_ref'] = 'mcisogem_college_tree'
        ctx['form_view_ref'] = 'view_mcisogem_college_form'
        if ctx['police'] :
            return {
                    'name':'Collège',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'mcisogem.college',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('police_id', '=', police_data.id)],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True

class mcisogem_histo_police(osv.osv):
    _name = "mcisogem.histo.police"
    _description = 'Historique de police'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'name': fields.many2one('mcisogem.police', 'Police', required=True),
        'dt_eff_histo_pol': fields.date('Date éffet histo police', required=True),
        'dt_eff_mod_pol': fields.date('Date éffet mod police', readonly=True),
        'num_avenant': fields.integer('Numéro avenant', readonly=True),
        'souscripteur': fields.char('Souscripteur', readonly=True),
        'garant': fields.char('Garant', readonly=True),
        'intermediaire': fields.char('Assur. intermédiaire', readonly=True),
        'num_police': fields.integer('Numéro interne police', readonly=True),
        'code_type_contrat': fields.char('Type de contrat', readonly=True),
        'code_regroupe_territoire': fields.char('Térritorialite', readonly=True),
        'regime_id': fields.many2one('mcisogem.regime', 'Type de remboursement', required=True),
        'num_police_assur': fields.char('Numéro police assureur', readonly=True),
        
        # Informations liees au beneficiaire
        'bl_ouvert_assur': fields.boolean("Couverture assuré"),
        'bl_ouvert_conj': fields.boolean('Couverture conjoint(e)'),
        'bl_ouvert_enfant': fields.boolean('Couverture enfant'),
        'bl_ouvert_parent': fields.boolean('Couverture parent'),
        'bl_ouvert_autre': fields.boolean('Couverture autre'),
        'limite_age_pol': fields.integer('Limite d\'age police'),
        'age_majorite_pol': fields.integer('Age majorité police'),
        'age_majorite_eleve_pol': fields.integer('Age majorité élève police'),
        'mod_calcul_age': fields.selection([('1', 'Date anniversaire'), ('2', 'Année')], 'Date', required=True),
        
        # college
        'college_ids': fields.many2many('mcisogem.college', 'college_rel', 'name', 'code_college', 'Collèges'),
        'code_college': fields.many2one('mcisogem.college', 'Collège', required=False),

        'tranche_age_ids': fields.many2many('mcisogem.tranche.age', 'tranche_age_rel', 'name', 'fin_tranche', 'Tranche d\'âge'),
        'code_tranche_age': fields.many2one('mcisogem.tranche.age', 'Tranche d\'âge', required=False),

        
        # Prestations autorisees
        'mnt_plfd_pol': fields.integer('Police', required=True),
        'mnt_plfd_col': fields.integer('Collège'),
        'mnt_plfd_ass': fields.integer('Assure principal', required=True),
        'mnt_plfd_conj': fields.integer('Conjoint', required=True),
        'mnt_plfd_enf': fields.integer('Enfant', required=True),
        'mnt_plfd_dep': fields.integer('Dependant'),
        'mnt_plfd_fam': fields.integer('Famille', required=True),
        'mnt_plfd_tenf': fields.integer('Tous les enfants'),
        'mnt_plfd_parent': fields.integer('Parents'),
        'mnt_plfd_autre': fields.integer('Autres'),
        'mnt_plfd_parent_autre': fields.integer('Parents et autre'),
        'mnt_plfd_territoire': fields.integer('Térritoire'),
        
        
        'bl_carmed_exclusif': fields.integer(''),
        'code_tranche': fields.integer(''),
        'plf_an_pol': fields.integer(''),

        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        
        'affichage_ta' : fields.integer('affichage_ta'),
        'affichage_college' : fields.integer('affichage_college'),
        'affichage_col' : fields.integer('affichage_col'),
        'affichage_tran' : fields.integer('affichage_tran'),
    }

    def _get_context(self, cr, uid, context):
        context = context or {}
        return context.get('police')
    
    _defaults = {
        'name': _get_context,
        'bl_carmed_exclusif': 0,
        'plf_an_pol': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        'code_tranche': 0,
        'affichage_ta': 0,
        'affichage_col': 0,
        'affichage_tran': 0,
        'affichage_college': 0,
        'mod_calcul_age' : '1',
    }
    
    def button_to_create_histo(self, cr, uid, ids, context=None):
        ctx = (context or {}).copy()
        
        police = self.browse(cr, uid, ids[0], context=context).id
        police_table = self.search(cr, uid, [('id', '=', police)])
        police_data = self.browse(cr, uid, police_table)
        
        ctx['police'] = self.browse(cr, uid, ids[0], context=context).id
        ctx['form_view_ref'] = 'view_mcisogem_histo_police_form'
        if ctx['police'] :
            return {
                    'name':'Historique police',
                    'view_type':'form',
                    'view_mode':'form',
                    'res_model':'mcisogem.histo.police',
                    'view_id':False,
                    'target':'new',
                    'type':'ir.actions.act_window',
                    'domain':[('name', '=', police_data.id)],
                    'context':ctx,
                    'nodestroy':True,
                    'res_id': ctx['police'],
                    }
        else : return True
    
    
    def onchange_police(self, cr, uid, ids, name, context=None):
        if not name:
            return {'value': {'police_id': False}}
        else:
            obj_police_data = self.pool.get('mcisogem.police').browse(cr, uid, name, context=context)
            
            cr.execute('select souscripteur_id from mcisogem_police where id=%s', (name,)) 
            souscr = cr.fetchone()[0]
            cr.execute('select name from mcisogem_souscripteur where id=%s', (souscr,)) 
            souscr_name = cr.fetchone()[0]
            
            cr.execute('select garant_id from mcisogem_police where id=%s', (name,)) 
            garant_id = cr.fetchone()[0]            
            cr.execute('select name from mcisogem_garant where id=%s', (garant_id,)) 
            garant = cr.fetchone()[0]
            
            cr.execute('select courtier_id from mcisogem_police where id=%s', (name,)) 
            courtier_id = cr.fetchone()[0]
            cr.execute('select name from mcisogem_courtier where id=%s', (courtier_id,)) 
            inter = cr.fetchone()[0]
            
            cr.execute('select type_contrat_id from mcisogem_police where id=%s', (name,)) 
            type_id = cr.fetchone()[0]
            cr.execute('select name from mcisogem_type_contrat where id=%s', (type_id,)) 
            typ = cr.fetchone()[0]
            
            cr.execute('select territoire_id from mcisogem_police where id=%s', (name,)) 
            ter_id = cr.fetchone()[0]
            cr.execute('select name from mcisogem_territoire where id=%s', (ter_id,)) 
            ter = cr.fetchone()[0]
            
            affichage = 0
            # Police par statut de bénéficiaire
            if obj_police_data.type_prime == '1':
                affichage = 0
            else:
            # Police par tranche d'age
                affichage = 1
            
            if obj_police_data.code_regime == 1:
                vals = { 'num_police': obj_police_data.num_interne_police,
                    'num_police_assur': obj_police_data.num_police_assur,
                    'dt_eff_mod_pol': obj_police_data.dt_deb_exercice,
                    'dt_eff_histo_pol': obj_police_data.dt_deb_exercice,
                    'num_avenant': obj_police_data.num_ave_interne_police,
                    'souscripteur':souscr_name,
                    'garant':garant,
                    'intermediaire':inter,
                    'code_type_contrat': typ,
                    'code_regroupe_territoire':ter,
                    'code_regime': 1,
                    'affichage_ta': affichage, }
                return {'value':vals}
            else:
                vals = { 'num_police': obj_police_data.num_interne_police,
                    'num_police_assur': obj_police_data.num_police_assur,
                    'dt_eff_mod_pol': obj_police_data.dt_deb_exercice,
                    'dt_eff_histo_pol': obj_police_data.dt_deb_exercice,
                    'num_avenant': obj_police_data.num_ave_interne_police,
                    'souscripteur': souscr_name,
                    'garant':garant,
                    'intermediaire':inter,
                    'code_type_contrat': typ,
                    'code_regroupe_territoire':ter,
                    'affichage_ta' : affichage, }
                return {'value':vals}
            
    def create(self, cr, uid, data, context=None):

        dernier_id = 0
        
        name = data['name']        
        cr.execute('select souscripteur_id from mcisogem_police where id=%s', (name,)) 
        souscr = cr.fetchone()[0]
        
        cr.execute('select type_prime from mcisogem_police where id=%s', (name,)) 
        type_prime = cr.fetchone()[0]
        
        cr.execute('select name from mcisogem_souscripteur where id=%s', (souscr,)) 
        data['souscripteur'] = cr.fetchone()[0]
        
        cr.execute('select dt_deb_exercice from mcisogem_police where id=%s', (name,)) 
        data['dt_eff_mod_pol'] = cr.fetchone()[0]
            
        cr.execute('select garant_id from mcisogem_police where id=%s', (name,)) 
        garant_id = cr.fetchone()[0]            
        cr.execute('select name from mcisogem_garant where id=%s', (garant_id,)) 
        data['garant'] = cr.fetchone()[0]
            
        cr.execute('select courtier_id from mcisogem_police where id=%s', (name,)) 
        courtier_id = cr.fetchone()[0]
        cr.execute('select name from mcisogem_courtier where id=%s', (courtier_id,)) 
        data['intermediaire'] = cr.fetchone()[0]
            
        cr.execute('select type_contrat_id from mcisogem_police where id=%s', (name,)) 
        type_id = cr.fetchone()[0]
        cr.execute('select name from mcisogem_type_contrat where id=%s', (type_id,)) 
        data['code_type_contrat'] = cr.fetchone()[0]
            
        cr.execute('select territoire_id from mcisogem_police where id=%s', (name,)) 
        ter_id = cr.fetchone()[0]
        cr.execute('select name from mcisogem_territoire where id=%s', (ter_id,)) 
        data['code_regroupe_territoire'] = cr.fetchone()[0]
        
        cr.execute('select num_interne_police from mcisogem_police where id=%s', (name,)) 
        data['num_police'] = cr.fetchone()[0]
        
        # Recuperation du numero avenant de la police
        cr.execute("select num_ave_interne_police from mcisogem_avenant where police_id=%s order by id desc" , (name,))
        num_ave = cr.fetchone()[0]
    
        data['affichage_ta'] = 0
        data['affichage_col'] = 1
        data['affichage_college'] = 1
        
        compteur_create = 0
        compteur_data = 0
                
        # Test pour voir si il s'agit d'une police par tranche d'age ou statut de bénéficiaire
        if type_prime == '2':
            # Police par tranche d'age
            # Parcours des colleges puis des tranches d'age
            data['affichage_tran'] = 1

            if len(data['college_ids'][0][2]) and len(data['tranche_age_ids'][0][2]) > 0:
                for col in data['college_ids'][0][2]:
                    for tr in data['tranche_age_ids'][0][2]:
                        compteur_data = compteur_data + 1
                        # Insertion des données en base
                        data['code_college'] = col 
                        data['code_tranche_age'] = tr
                        cr.execute("select * from mcisogem_histo_police where num_police=%s and dt_eff_histo_pol>=%s and code_college=%s and code_tranche_age=%s", (data['num_police'], data['dt_eff_histo_pol'], col, tr))
                        if len(cr.dictfetchall()) == 0:
                            compteur_create = compteur_create + 1
                            dernier_id = super(mcisogem_histo_police, self).create(cr, uid, data, context)
                            cr.execute("update mcisogem_histo_police set num_avenant =%s where id=%s", (num_ave, dernier_id))

                if compteur_create == 0:
                    raise osv.except_osv('Attention !', "la date d'effet du nouvel historique de police doit être !")
                    return False
                else:
                    return dernier_id
                    """if compteur_create == compteur_data:
                        return dernier_id
                    else:
                        raise osv.except_osv('Attention !', "Erreur duplication lors de l'addition de l'enregistrement. " + str(compteur_create) +  " ligne(s) crée(s) !", (compteur_create,))
                        return dernier_id"""
            else:
                raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un collège et une tranche d'age !")
                return False           

        else:
            # Police par statut de bénéficiaire
            # Parcours des collèges
            data['affichage_tran'] = 0
            if len(data['college_ids'][0][2]) > 0:
                for col in data['college_ids'][0][2]:
                    compteur_data = compteur_data + 1
                    data['code_college'] = col
                    cr.execute("select * from mcisogem_histo_police where num_police=%s and dt_eff_histo_pol>=%s and code_college=%s", (data['num_police'], data['dt_eff_histo_pol'], col))
                    if len(cr.dictfetchall()) == 0:
                        compteur_create = compteur_create + 1
                        dernier_id = super(mcisogem_histo_police, self).create(cr, uid, data, context)
                        cr.execute("update mcisogem_histo_police set num_avenant =%s where id=%s", (num_ave, dernier_id))
                
                if compteur_create == 0:
                    raise osv.except_osv('Attention !', "Cet historique de police existe déjà !")
                    return False
                else:
                    return dernier_id
                    """if compteur_create == compteur_data:
                        return dernier_id
                    else:
                        raise osv.except_osv('Attention !', "Erreur duplication lors de l'addition de l'enregistrement. " + str(compteur_create) + " ligne(s) crée(s) !")
                        return dernier_id"""
            else:
                raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un collège !")
                return False


class mcisogem_liste_noire(osv.osv):
    _name = "mcisogem.liste.noire"
    _description = 'Liste noire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'police_id': fields.many2one('mcisogem.police', 'Police', required=True),
        'dt_eff': fields.date('Date effet', required=True),
        'dt_levee': fields.date('Date levee'),
        'motif_suspen_id': fields.many2one('mcisogem.motif.suspen', 'Motif liste noire', required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }

    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
    
class mcisogem_exercice_police(osv.osv):
    _name = "mcisogem.exercice.police"
    _description = 'Historique de la police'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
            'police_id': fields.many2one('mcisogem.police', 'Police', required=True),
            'num_interne_police': fields.integer('num_police', required=True),
            'name': fields.char(''),
            'exercice_id': fields.many2one('mcisogem.exercice', 'Exercice', required=True),
            'date_debut_exercice': fields.date('Date de début', readonly=True),
            'date_fin_exercice': fields.date('Date de fin', readonly=True),
            'bl_exercice_clot': fields.boolean('Cloturé'),
            'prime_pol_exercice': fields.integer('prime_pol_exercice'),
            'dernier_avenant': fields.integer('dernier_avenant'),
            'cum_mnt_pol': fields.integer('cum_mnt_pol'),
            'typ_prime': fields.integer('typ_prime'),
            'masse_sal_pol': fields.integer('masse_sal_pol'),
            'pc_masse_sal_pol': fields.integer('pc_masse_sal_pol'),
            'bl_pc_masse_sal_pol': fields.integer('bl_pc_masse_sal_pol'),
            'periodicite_paiem_pol': fields.selection([(1, 'Annuelle'), (2, 'Semestrielle'), (3, 'Trimestrielle'), (4, 'Bimensuelle'), (5, 'Mensuelle')], 'Périodicité paiement prime'),
            'rapport_sp_preced': fields.integer('rapport_sp_preced'),
            'tot_sinistre_preced': fields.integer('tot_sinistre_preced'),
            'tot_prime_preced': fields.integer('tot_prime_preced'),
            'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
            'code_gest': fields.char('libelle_gest', size=50, required=True),
            'code_langue': fields.char('code_langue', size=10, required=True),
            'cod_sup': fields.char('cod_sup'),
            'repartition_prime': fields.selection([(0, 'Jour'), (1, 'Mois')], 'Repartition prime'),
            'tva_oui_non': fields.boolean('Tva'),
            'imputation_accessoires': fields.integer('imputation_accessoires'),
            'imputation_acc_cie': fields.integer('imputation_acc_cie'),
            'imputation_acc_courtier': fields.integer('imputation_acc_courtier'),
            'type_prime': fields.selection([(1, 'Statut bénéficiaire'), (2, 'Tranche d\'age')], 'Type prime'),
}
    
    _sql_constraints = [('unique_exercice_police', 'unique(num_interne_police, date_debut_exercice, date_fin_exercice)', "Cet exercice police existe déjà !"), ]
    
    def _get_context(self, cr, uid, context):
        context = context or {}
        return context.get('police')

    _defaults = {
            'police_id': _get_context,
            'type_prime' : 1,
            'repartition_prime' : 1,
            'periodicite_paiem_pol': 1,
            'prime_pol_exercice': 0,
            'dernier_avenant': 0,
            'cum_mnt_pol':0,
            'masse_sal_pol':0,
            'pc_masse_sal_pol':0,
            'bl_pc_masse_sal_pol':0,
            'rapport_sp_preced':0,
            'tot_sinistre_preced': 0,
            'tot_prime_preced': 0,
            'code_gest': _get_cod_gest,
            'ident_centre': _get_cod_gest_id,
            'code_langue': _get_cod_lang,
}
    
    def onchange_police(self, cr, uid, ids, police_id, context=None):
        if not police_id:
            return False
        else:
            # Recuperation de l'ancien exercice de police
            cr.execute("select * from mcisogem_exercice_police where police_id=%s order by id desc", (police_id,))
            lesexopolice = cr.dictfetchall()
            if len(lesexopolice) > 0:
                exopolice = lesexopolice[0]
                return {'value': {'repartition_prime' : exopolice['repartition_prime'], 'type_prime' : exopolice['type_prime'],
                                  'periodicite_paiem_pol' : exopolice['periodicite_paiem_pol']}}
            else:
                return False

    def onchange_exercice(self, cr, uid, ids, exercice_id, context=None):
        # Recuperation de l'exercice
        if not exercice_id:
            return {'value': {'date_debut_exercice': False, 'date_fin_exercice': False}} 
        else:
            cr.execute("select * from mcisogem_exercice where id=%s", (exercice_id,))
            lesexo = cr.dictfetchall()
            print lesexo
            exo = lesexo[0]
            return {'value': {'date_debut_exercice': exo['date_debut'], 'date_fin_exercice': exo['date_fin']}} 
   
    def create(self, cr, uid, vals, context=None):
            
        # QUESTION : LA CREATION D'UN NOUVEL EXERCICE DE POLICE IMPLIQUE T'IL LA CREATION D'UN NOUVEL AVENANT ?
        cr.execute("select * from mcisogem_exercice where id=%s", (vals['exercice_id'],))
        lesexo = cr.dictfetchall()
        exo = lesexo[0]
        vals['date_debut_exercice'] = exo['date_debut']
        vals['date_fin_exercice'] = exo['date_fin']
        
        # Recuperation du numero interne de la police
        cr.execute("select num_interne_police, name from mcisogem_police where id=%s", (vals['police_id'],))
        content = cr.dictfetchall()[0]

        vals['num_interne_police'] = content['num_interne_police']
        vals['name'] = content['name']
        return super(mcisogem_exercice_police, self).create(cr, uid, vals, context=context)
       
    # histo_prime
class mcisogem_histo_prime(osv.osv):
    _name = "mcisogem.histo.prime"
    _description = 'Historique de la prime'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'garant_id': fields.many2one('mcisogem.garant', 'Assureur', required=True),
        'police_id': fields.many2one('mcisogem.police', 'Police', required=True),
        'name': fields.char(''),
        'college_id': fields.many2one('mcisogem.college', 'College', required=False),
        'statut_benef_id': fields.many2one('mcisogem.stat.benef', 'Statut bénéficiaire', required=False),
        'dt_eff_mod_prime': fields.date('Date éffet mod prime', readonly=False, required=True),
        'num_avenant': fields.integer('Numéro avenant', readonly=True),
        'dt_echea_pol': fields.date('Date écheance police', readonly=True),
        'cout_d_acte': fields.integer('cout d acte', required=False),
        'taxe_sur_prime': fields.integer('taxe sur prime', required=False),
        'taxe_sur_comm': fields.integer('taxe sur_comm', required=False),
        'prim_pol': fields.integer('prim pol', required=False),
        'prim_col': fields.integer('prim_col', required=False),
        'prim_fam': fields.integer('prim_fam', required=False),
        'prim_assure': fields.integer('Prime assuré', required=False),
        'prim_conj': fields.integer('prim_conj', required=False),
        'prim_enfant': fields.integer('prim_enfant', required=False),
        'masse_sal_pol': fields.integer('masse_sal_pol', required=False),
        'pc_sal_prime': fields.integer('pc_sal_prime', required=False),
        'dt_prem_ech': fields.date('dt_prem_ech', readonly=True, required=False),
        'num_police': fields.integer('Numero interne police', readonly=True, required=False),
        
        'cod_college_ids':fields.many2many('mcisogem.histo.prime.college.temp',
                                       'mcisogem_histo_prime_college_temp_rel',
                                        'college_temp_id',
                                        'code_college', 'Choix des collèges', required=False),
                
        'cod_statut_benef_ids':fields.many2many('mcisogem.histo.prime.stat.benef.temp',
                                       'mcisogem_histo_prime_stat_benef_temp_rel',
                                        'stat_benef_temp_id',
                                        'cod_statut_benef', 'Choix des statuts de bénéficiaire', required=False),
                
        'bl_pc_sal_prime': fields.integer('bl_pc_sal_prime', required=False),
        'bl_cout_act': fields.integer('bl_cout_act', required=False),
        'type_prime': fields.integer('type_prime', required=False),
        'mode_calcul': fields.integer('mode_calcul', required=False),
        'mode_encaissement': fields.integer('mode_encaissement', required=False),
        'taux_majo_prime': fields.integer('taux_majo_prime', readonly=True, required=False),
        'cout_d_acte_courtier': fields.integer('cout_d_acte_courtier', readonly=True, required=False),
        'bl_cout_d_acte_courtier': fields.integer('bl_cout_d_acte_courtier', readonly=True, required=False),
        'cout_d_acte_assur': fields.integer('cout_d_acte_assur', readonly=True, required=False),
        'bl_cout_d_acte_assur': fields.integer('bl_cout_d_acte_assur', readonly=True, required=False),
        'taxe_acc_nostro': fields.integer('taxe_acc_nostro', readonly=True, required=False),
        'taxe_acc_courtier': fields.integer('taxe_acc_courtier', readonly=True, required=False),
        'taxe_acc_assureur': fields.integer('taxe_acc_assureur', readonly=True, required=False),
        'bl_taxe_acc_nostro': fields.integer('bl_taxe_acc_nostro', readonly=True, required=False),
        'bl_taxe_acc_courtier': fields.integer('t', readonly=True, required=False),
        'bl_taxe_acc_assureur': fields.integer('t', readonly=True, required=False),
        'bl_taxe_sur_prime': fields.integer('t', readonly=True, required=False),
        'bl_taxe_sur_comm': fields.integer('t', readonly=True, required=False),
        'bl_cout_d_acte': fields.integer('t', readonly=True, required=False),
        'prime_reassur': fields.integer('t', readonly=True, required=False),
        'bl_prime_reassur': fields.integer('t', readonly=True, required=False),
        'comm_reassur': fields.integer('t', readonly=True, required=False),
        'taxe_sur_prime_reassur': fields.integer('t', readonly=True, required=False),
        'bl_taxe_sur_prime_reassur': fields.integer('t', readonly=True, required=False),
        'taxe_sur_comm_reassur': fields.integer('t', readonly=True, required=False),
        'bl_taxe_sur_comm_reassur': fields.integer('t', readonly=True, required=False),
        'prime_parent': fields.integer('t', readonly=True, required=False),
        'prime_autre': fields.integer('t', readonly=True, required=False),
        'prime_sida': fields.integer('Prime SIDA', required=False),
        'prime_autre': fields.integer('t', readonly=True, required=False),
        'repartition_prime': fields.integer('t', readonly=True, required=False),
        'prime_mois_exercice': fields.selection([(1, 'Exercice'), (2, 'Mensuel')], 'Période montant prime', required=True),
        'tva_oui_non': fields.integer('t', readonly=True, required=False),
        'code_tranche_age': fields.many2one('mcisogem.tranche.age', 'Tranche d\'age', required=False),
        
        'cod_tranche_age_ids':fields.many2many('mcisogem.histo.prime.tranche.age.temp',
                                       'mcisogem_histo_prime_tranche_age_temp_rel',
                                        'tranche_age_temp_id',
                                        'tranche_age', 'Choix des tranches d\'age', required=False),
                
        'budget_sida': fields.integer('Budget sida', required=False),
        'budget_simple': fields.integer('Budget sans sida', required=False),
        'budget_ttc': fields.boolean('Montant TTC', required=False),
        'mode_prime': fields.integer('t', readonly=True, required=False),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        
        'affiche_tab_benef': fields.integer('affiche tab benef', required=False),
        'affiche_tab_tranche': fields.integer('affiche tab tranche', required=False),
        'affiche_budget': fields.integer('affiche budget', required=False),
        'affiche_tab_college': fields.integer('affiche college', required=False),
        'modification': fields.integer('Modification', required=False),
        'modification_tranche': fields.integer('Modification Tranche', required=False),
        'modification_benef': fields.integer('Modification benef', required=False),
    }

    def _get_context(self, cr, uid, context):
        context = context or {}
        return context.get('police')

    def _get_assur(self, cr, uid, context):
        context = context or {}
        pol = context.get('police')
        cr.execute('select garant_id from mcisogem_police where id=%s', (pol,))        
        val = cr.fetchone()[0]
        return val
    
    _defaults = {
        'police_id': _get_context,
        'garant_id': _get_assur,
        'prime_mois_exercice' : 1,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'cout_d_acte' : 0,
        'taxe_sur_prime': 0,
        'taxe_sur_comm' : 0,
        'prim_pol' : 0,
        'prim_col' : 0,
        'prim_conj' : 0,
        'prim_enfant' : 0,
        'prim_fam' : 0,
        'masse_sal_pol' : 0,
        'pc_sal_prime' : 0,
        'dt_prem_ech' : '1900-01-01 00:00:00',
        'bl_pc_sal_prime' : 0,
        'bl_cout_act' : 0,
        'mode_encaissement' : 1,
        'taux_majo_prime' : 0,
        'cout_d_acte_courtier' : 0,
        'bl_cout_d_acte_courtier': 0,
        'cout_d_acte_assur' : 0,
        'bl_cout_d_acte_assur' : 0,
        'taxe_acc_nostro' : 0,
        'taxe_acc_courtier' : 0,
        'taxe_acc_assureur': 0,
        'bl_taxe_acc_nostro': 0,
        'bl_taxe_acc_courtier' : 0,
        'bl_taxe_acc_assureur': 0,
        'bl_taxe_sur_prime': 0,
        'bl_taxe_sur_comm': 0,
        'bl_cout_d_acte' : 0,
        'prime_reassur' : 0,
        'bl_prime_reassur' : 0,
        'comm_reassur' : 0,
        'taxe_sur_prime_reassur': 0,
        'bl_taxe_sur_prime_reassur': 0,
        'taxe_sur_comm_reassur' : 0,
        'bl_taxe_sur_comm_reassur' : 0,
        'prime_parent': 0,
        'prime_autre': 0,
        'affiche_tab_college': 0,
        'affiche_tab_benef': 0,
        'affiche_tab_tranche': 0,
        'affiche_budget': 0,
        'modification': 0,
        'modification_tranche': 0,
        'modification_benef': 0,
        }
    

    def onchange_garant(self, cr, uid, ids, garant_id, context=None):
        return {'value': {'affiche_budget': 0, 'affiche_tab_tranche': 0, 'affiche_tab_benef' : 0, 'affiche_tab_college' : 0, 'police_id' : False}} 
        
                
    def onchange_police(self, cr, uid, ids, police_id, context=None):
        
        tabcollege = []
        tabtrancheage = []
        tabstatutbeneficiare = []
        
        exp = []
        if not police_id:
            return {'value': {'police_id': False}}
        else:
            # Tentative de recuperation de l'exercice de police de la police sélectionnée
            cr.execute("select * from mcisogem_exercice_police where police_id=%s order by id desc", (police_id,))
            lesexospolice = cr.dictfetchall()
            if len(lesexospolice) > 0:
                # Recuperation de la date d'effet de la police 
                dt_eff_mod_prime = lesexospolice[0]['date_debut_exercice']
                # On vide la table college tampon
                cr.execute("delete from mcisogem_histo_prime_college_temp where write_uid=%s", (uid,))
                # Recuperation de la police
                obj_police_data = self.pool.get('mcisogem.police').browse(cr, uid, police_id, context=context)
               
                cr.execute('select id from mcisogem_histo_police where name=%s order by id desc', (police_id,))
                leshistopolices = cr.dictfetchall()
    
                if len(leshistopolices) == 0:
                    affiche_budget = 0
                    affiche_tab_tranche = 0
                    affiche_tab_benef = 0      
                    raise osv.except_osv('Attention !', "Aucune historique de police n'a été trouvée pour cette police. Veuillez procéder à la création de l'historique de police !")
                    return {'value': {'police_id': False}} 
                else:
                    # Recuperation des colleges de la police
                    cr.execute('select c.id as col,crel.code_college as codc  from college_rel crel,mcisogem_college c where crel.code_college=c.id and crel.name=%s', (leshistopolices[0]['id'],)) 
                    vals = cr.dictfetchall()
                # Insertion des colleges recuperés dans la table temporaire
                for elt in vals:
                    cr.execute("insert into mcisogem_histo_prime_college_temp (create_uid,choix,cod_college,write_uid) values(%s, %s, %s, %s)", (uid, False, elt['codc'], uid))
                    
                cr.execute("select * from mcisogem_histo_prime_college_temp where write_uid=%s", (uid,))
                lescollegestemp = cr.dictfetchall()
                for col in lescollegestemp:
                    tabcollege.append(col['id'])
                    
                # On va chercher a savoir si les champs budget doivent s'afficher ou non
                # Recuperation du garant
                print obj_police_data.garant_id.type_garant_id.code_type_garant
                
                if obj_police_data.garant_id.type_garant_id.code_type_garant in ['4', '3', '2']:
                   affiche_budget = 1 
                else:
                   affiche_budget = 0                
                # A ce stade nous avons les colleges de la police et l'objet police pour les tests
                            
                # Test pour savoir si il s'agit d'une police par beneficiare ou par tranche d'age
              
                if obj_police_data.type_prime == '2':
                    # Police par tranche d'age
                    # requete de recuperation des tranches d'age de la police
                    cr.execute("delete from mcisogem_histo_prime_tranche_age_temp where write_uid=%s", (uid,))
                    cr.execute('select * from tranche_age_rel where name=%s', (leshistopolices[0]['id'],))
                    lestrancheagepolice = cr.dictfetchall()
                    
                    print lestrancheagepolice
                    if len(lestrancheagepolice) == 0:
                         raise osv.except_osv('Attention !', "Aucune tranche d'age n'a été trouvé pour la police !")
                         return {'value': {'police_id': False}}  
                    else:
                        # Porcours des tranches d'ages 
                        for tr in lestrancheagepolice:
                            obj_tranche_data = self.pool.get('mcisogem.tranche.age').browse(cr, uid, tr['fin_tranche'], context=context)
                            cr.execute("""insert into mcisogem_histo_prime_tranche_age_temp (create_uid,montant_prime_sida,debut,fin,montant_prime,write_uid, code_tranche_age)
                             values(%s, %s, %s, %s, %s, %s,%s)""",
                             (uid, 0, obj_tranche_data.debut_tranche, obj_tranche_data.fin_tranche, 0, uid, obj_tranche_data.id))
                        cr.execute("select * from mcisogem_histo_prime_tranche_age_temp where write_uid=%s", (uid,))
                        lestranchestemp = cr.dictfetchall()
                        for tr in lestranchestemp:
                            tabtrancheage.append(tr['id'])
                        affiche_tab_tranche = 1
                        affiche_tab_benef = 0 
                        affiche_tab_college = 1            
                        return {'value': {'dt_eff_mod_prime': dt_eff_mod_prime, 'cod_tranche_age_ids': tabtrancheage, 'cod_college_ids': tabcollege, 'affiche_tab_tranche': affiche_tab_tranche, 'affiche_budget':affiche_budget, 'affiche_tab_college': affiche_tab_college}}
    
                else:
                    # Police par statut bénéficiaire - Recuperation des statut benef
                     cr.execute("delete from mcisogem_histo_prime_stat_benef_temp where write_uid=%s", (uid,))
                     cr.execute('select * from mcisogem_stat_benef ')
                     lesstatutsbenef = cr.dictfetchall()
                    
                     if len(lesstatutsbenef) == 0:
                         affiche_budget = 0
                         affiche_tab_tranche = 0
                         affiche_tab_benef = 0
                         raise osv.except_osv('Attention !', "Aucun statut de bénéficiaire n'a ete trouve !")
                         return {'value': {'police_id': False}} 
                     else:
                        for statut in lesstatutsbenef:
                            print '------------------------++++++++'
                            print statut
                            # Insertion des statuts dans la table temporaire
                            cr.execute("insert into mcisogem_histo_prime_stat_benef_temp (create_uid,choix,cod_statut_benef,write_uid) values(%s, %s, %s, %s)", (uid, False, statut['id'], uid))
                            cr.execute("select * from mcisogem_histo_prime_stat_benef_temp where write_uid=%s", (uid,))
                            lesstatutstemp = cr.dictfetchall()
                        for stemp in lesstatutstemp:
                            tabstatutbeneficiare.append(stemp['id'])  
                        affiche_tab_benef = 1             
                        affiche_tab_tranche = 0
                        affiche_tab_college = 1           
                        return{'value': {'dt_eff_mod_prime': dt_eff_mod_prime, 'cod_college_ids': tabcollege, 'cod_statut_benef_ids': tabstatutbeneficiare, 'affiche_tab_benef': affiche_tab_benef, 'affiche_budget': affiche_budget, 'affiche_tab_college': affiche_tab_college}}
            else:
                raise osv.except_osv('Attention !', "Cette police ne possède pas d'exercice de police !")
                return {'value': {'police_id': False}} 
    
    def create(self, cr, uid, vals, context=None):
        
        dernier_id = 0
        
        # Recuperation des informations relatives à l'exercice de la police
        cr.execute("select * from mcisogem_exercice_police where police_id=%s order by id desc", (vals['police_id'],))
        lesexercicespolices = cr.dictfetchall()
        
        # Recuperation de la liste des colleges sélectionnés
        cr.execute("select * from mcisogem_histo_prime_college_temp where write_uid=%s and choix=%s", (uid, True))
        lescollegesselect = cr.dictfetchall()
        
        # Recuperation des données relatives à la police
        cr.execute("select * from mcisogem_police where id=%s", (vals['police_id'],))
        lapolice = cr.dictfetchall()[0]
                              
        # Test pour voir si cette police possède un exercice de police
        if len(lesexercicespolices) > 0:
        # Test pour voir si au moins un collège a été sélectionné
            if len(lescollegesselect) > 0:
                # Test pour voir si il s'agit d'une police par tranche d'age ou par statut de bénéficiaire
                if vals['affiche_tab_benef'] == 1:
                    # Police par statut de beneficiaire
                    # Recuperation de la liste des statuts de bénéficiaire cochés
                    cr.execute("select * from mcisogem_histo_prime_stat_benef_temp where write_uid=%s and choix=%s", (uid, True))
                    lesstatutbenefselect = cr.dictfetchall()
                    if len(lesstatutbenefselect) > 0:
                        
                        compteur_create = 0
                        
                         # Parccours des collèges pour insertion des données en base
                        for college in lescollegesselect:
                            # parcours des statuts bénef
                            for stat in lesstatutbenefselect:
                                # Insertion des données en base
                                #Avant insertion on va chercher a voir si un enregistrement possédant le meme statut benef et le meme college
                                #Si un enregistrement a été trouvé on récuprer la date d'effet qu'on va comparer a la nouvelle date. La nouvelle date d'effet doit etre supérieur à la précédente date
                                cr.execute("select id, dt_eff_mod_prime from mcisogem_histo_prime where college_id=%s and statut_benef_id=%s order by dt_eff_mod_prime desc", (college['cod_college'],stat['cod_statut_benef']))
                                leshistoprimes = cr.dictfetchall()
                                
                                test_create = True
                                
                                if len(leshistoprimes) > 0:
                                    histop = leshistoprimes[0]
                                    if  vals['dt_eff_mod_prime'] > histop['dt_eff_mod_prime']:
                                        #1er niveau de vérification
                                        datedujour = time.strftime('%Y-%m-%d', time.localtime())
                                        #cr.execute("update mcisogem_histo_prime set dt_eff_mod_prime=%s where id=%s", (datedujour, histop['id']))
                                        test_create = True
                                    else:
                                        test_create = False
                                        
                                if test_create:
                                    compteur_create = compteur_create + 1
                                    data = {}
                                    data['college_id'] = college['cod_college']
                                    data['statut_benef_id'] = stat['cod_statut_benef']
                                    data['garant_id'] = vals['garant_id']
                                    data['police_id'] = vals['police_id']
                                    data['dt_eff_mod_prime'] = vals['dt_eff_mod_prime']
                                    data['num_avenant'] = 0                 
                                    data['dt_echea_pol'] = lesexercicespolices[0]['date_fin_exercice']
                                    data['prim_assure'] = stat['montant_prime']
                                    data['prime_sida'] = stat['montant_prime_sida']
                                    data['num_police'] = lapolice['num_interne_police']
                                    data['name'] = lapolice['name']
                                    data['type_prime'] = lapolice['type_prime']
                                    data['mode_calcul'] = lapolice['repartition_prime']
                                    data['repartition_prime'] = lapolice['repartition_prime']
                                    data['prime_mois_exercice'] = vals['prime_mois_exercice']
                                    data['code_tranche_age'] = 1
                                    data['budget_sida'] = vals['budget_sida']
                                    data['budget_simple'] = vals['budget_simple']
                                    data['budget_ttc'] = vals['budget_ttc']                                
                                    data['affiche_tab_college'] = 0                               
                                    data['affiche_tab_benef'] = 0                               
                                    data['affiche_tab_tranche'] = 0
                                    data['affiche_budget'] = vals['affiche_budget'] 
                                    data['modification'] = 1
                                    data['modification_tranche'] = 0
                                    data['modification_benef'] = 1                       
                                    dernier_id = super(mcisogem_histo_prime, self).create(cr, uid, data, context=context)

                        
                        # On va vider les tables temporaires
                        if compteur_create == 0:
                            raise osv.except_osv('Attention !', "La date d'éffet doit être supérieur à la date d'éffet de la précédente historique de prime !")
                            return False  
                        else:
                            cr.execute("delete from mcisogem_histo_prime_stat_benef_temp where write_uid=%s", (uid,))     
                            cr.execute("delete from mcisogem_histo_prime_college_temp where write_uid=%s", (uid,)) 
                            print'dernier_id-------------------------'
                            print dernier_id    
                            return dernier_id
                    else:
                        raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un statut de bénéficiaire !")
                        return False  
                else:
                    # Police par tranche d'age
                    # Recuperation de la liste des tranches d'age cochées
                    cr.execute("select * from mcisogem_histo_prime_tranche_age_temp where write_uid=%s", (uid,))
                    lestarnchesagesselect = cr.dictfetchall()
                    compteur_create = 0
                    
                    if len(lestarnchesagesselect) > 0:
                        # Parcours des collèges
                        for college in lescollegesselect:
                            # Parcours des traches d'ages
                            for tranche in lestarnchesagesselect:
                                 # Insertion des données en base
                                  #Avant insertion on va chercher a voir si un enregistrement possédant le meme statut benef et le meme college
                                #Si un enregistrement a été trouvé on récuprer la date d'effet qu'on va comparer a la nouvelle date. La nouvelle date d'effet doit etre supérieur à la précédente date
                                cr.execute("select id, dt_eff_mod_prime from mcisogem_histo_prime where college_id=%s and code_tranche_age=%s order by dt_eff_mod_prime desc", (college['cod_college'], tranche['code_tranche_age']))
                                leshistoprimes = cr.dictfetchall()
                                
                                test_create = True
                                
                                if len(leshistoprimes) > 0:
                                    histop = leshistoprimes[0]
                                    if  vals['dt_eff_mod_prime'] > histop['dt_eff_mod_prime']:
                                        #1er niveau de vérification
                                        datedujour = time.strftime('%Y-%m-%d', time.localtime())
                                        cr.execute("update mcisogem_histo_prime set dt_eff_mod_prime=%s where id=%s", (datedujour, histop['id']))
                                        test_create = True
                                    else:
                                        test_create = False
                                    
                                if test_create:
                                    compteur_create = compteur_create + 1
                                    data = {}
                                    data['college_id'] = college['cod_college']
                                    data['garant_id'] = vals['garant_id']
                                    data['police_id'] = vals['police_id']
                                    data['dt_eff_mod_prime'] = vals['dt_eff_mod_prime']
                                    data['num_avenant'] = 0                 
                                    data['dt_echea_pol'] = lesexercicespolices[0]['date_fin_exercice']
                                    data['prim_assure'] = tranche['montant_prime']
                                    data['prime_sida'] = tranche['montant_prime_sida']
                                    data['num_police'] = lapolice['num_interne_police']
                                    data['type_prime'] = lapolice['type_prime']
                                    data['mode_calcul'] = lapolice['repartition_prime']
                                    data['name'] = lapolice['name']
                                    data['repartition_prime'] = lapolice['repartition_prime']
                                    data['prime_mois_exercice'] = vals['prime_mois_exercice']
                                    data['code_tranche_age'] = tranche['code_tranche_age']
                                    data['budget_sida'] = vals['budget_sida']
                                    data['budget_simple'] = vals['budget_simple']
                                    data['budget_ttc'] = vals['budget_ttc']                                
                                    data['affiche_tab_college'] = 0                               
                                    data['affiche_tab_benef'] = 0                               
                                    data['affiche_tab_tranche'] = 0
                                    data['modification'] = 1
                                    data['modification_tranche'] = 1
                                    data['modification_benef'] = 0
                                    data['affiche_budget'] = vals['affiche_budget']                          
                                    dernier_id = super(mcisogem_histo_prime, self).create(cr, uid, data, context=context)
                                        
                        if compteur_create == 0:
                            raise osv.except_osv('Attention !', "La date d'éffet doit être supérieur à la date d'éffet de la précédente historique de prime !")
                            return False  
                        else:
                             # On va vider les tables temporaires
                            cr.execute("delete from mcisogem_histo_prime_tranche_age_temp where write_uid=%s", (uid,))     
                            cr.execute("delete from mcisogem_histo_prime_college_temp where write_uid=%s", (uid,))     
                            return dernier_id
                    else:
                        raise osv.except_osv('Attention !', "Veuillez sélectionner au moins une tranche d'age !")
                        return False   
                        
            else:
                raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un collège !")
                return False
        else:
            raise osv.except_osv('Attention !', "Cette police n'a pas été associé à un exercice de police !")
            return False  

    
class mcisogem_histo_prime_stat_benef_temp(osv.osv):
    _name = "mcisogem.histo.prime.stat.benef.temp"
    _description = 'Statut du beneficiaire'
    
    _columns = {
        'choix': fields.boolean('Choix'),
        'montant_prime': fields.integer('Montant prime', required=False),
        'montant_prime_sida': fields.integer('Montant prime SIDA', required=False),
        'cod_statut_benef':fields.many2one('mcisogem.stat.benef', 'lb_fam_statut', 'Famille statut', readonly=True),
       
    }

    def onchange_choix(self, cr, uid, ids, choix, context=None):
        cr.execute("update mcisogem_histo_prime_stat_benef_temp set choix=%s where id=%s", (choix, ids[0]))
    
    def onchange_montant_prime(self, cr, uid, ids, montant_prime, context=None):
        cr.execute("update mcisogem_histo_prime_stat_benef_temp set montant_prime=%s where id=%s", (montant_prime, ids[0]))
        
    def onchange_montant_prime_sida(self, cr, uid, ids, montant_prime_sida, context=None):
        cr.execute("update mcisogem_histo_prime_stat_benef_temp set montant_prime_sida=%s where id=%s", (montant_prime_sida, ids[0]))

class mcisogem_histo_prime_college_temp(osv.osv):
    _name = "mcisogem.histo.prime.college.temp"
    _description = 'College'
    
    _columns = {
        'choix': fields.boolean('Choix'),
       'cod_college':fields.many2one('mcisogem.college', 'name', 'College', readonly=True),
       
    }
    
    def onchange_choix(self, cr, uid, ids, choix, context=None):
        cr.execute("update mcisogem_histo_prime_college_temp set choix=%s where id=%s", (choix, ids[0]))
    
    


class mcisogem_histo_prime_tranche_age_temp(osv.osv):
    _name = "mcisogem.histo.prime.tranche.age.temp"
    _description = 'Tranche age'
    
    _columns = {
       'code_tranche_age':fields.many2one('mcisogem.tranche.age', 'name', 'Tranche_age', readonly=True),
        'debut': fields.integer('debut', required=False, readonly=True),
        'fin': fields.integer('fin', required=False, readonly=True),
        'montant_prime': fields.integer('Montant prime', required=False),
        'montant_prime_sida': fields.integer('Montant prime sida', required=False),
       
    }

    def onchange_montant_prime(self, cr, uid, ids, montant_prime, context=None):
        cr.execute("update mcisogem_histo_prime_tranche_age_temp set montant_prime=%s where id=%s", (montant_prime, ids[0]))
        
    def onchange_montant_prime_sida(self, cr, uid, ids, montant_prime_sida, context=None):
        cr.execute("update mcisogem_histo_prime_tranche_age_temp set montant_prime_sida=%s where id=%s", (montant_prime_sida, ids[0]))
    

    # statut_benef
class mcisogem_stat_benef(osv.osv):
    _name = "mcisogem.stat.benef"
    _description = 'Statut du bénéfficiaire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'cod_statut_benef': fields.char('Code', required=True),
        'tm_stamp': fields.date('tm_stamp', readonly=True),
        'cod_lang':fields.many2one('mcisogem.langue', 'name', 'Langue'),
        'cod_sup': fields.integer('cod_sup'),
        'name': fields.char('Libellé'),
        'lbc_fam_statut': fields.char('lbc_fam_statut'),
        'code_gest': fields.char('Code centre de gestion'),
        'ident_centre': fields.char('id centre')
    }
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
    }
    
    def create(self, cr, uid, vals, context=None):
        vals['lbc_fam_statut'] = vals['cod_statut_benef']
        return super(mcisogem_stat_benef, self).create(cr, uid, vals, context=context)

# fam_statut

class mcisogem_fam_statut(osv.osv):
    _name = "mcisogem.fam.statut"
    _description = 'Famille de statut'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
        
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    _columns = {
        'lbc_fam_statut': fields.char('Libellé court', required=True),
        'lb_fam_statut': fields.char('Libellé', required=True),
        'code_sup': fields.integer('Code centre de gestion'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
    
class mcisogem_nature_risque(osv.osv):
    _name = "mcisogem.nature.risque"
    _description = 'Nature risque'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
        
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    _columns = {
        'code_nature_risque': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'code_sup': fields.integer('Code centre de gestion'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
    """ 
    CLASSE MEDICAL
    """""
    
class mcisogem_type_centre(osv.osv):
    _name = "mcisogem.type.centre"
    _description = 'Type de centre'
    
        
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_type_centre': fields.char('Code', size=10, required=True),
        'name': fields.char('Libellé', size=50, required=True),
        'code_type_reserve' : fields.boolean('Type reservé'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'Nbre_ctr' : fields.integer('Nbre_ctr'),
        'code_type_centre2' : fields.char('Lettre', size=50, required=True)                
    }
    
    _sql_constraints = [('unique_type_centre', 'unique(code_type_centre, code_langue)', "Le type de centre existe déjà !"), ]
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        'Nbre_ctr':0,
    }

mcisogem_type_centre() 




""" Classe : PLAGE_CENTRE """ 
class mcisogem_plage_centre(osv.osv):
    
    _name = "mcisogem.plage.centre"
    _description = 'Plage centre'
  
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'numero_plage_centre': fields.integer('Code plage', required=True),
        'code_centre' : fields.char('Code centre', size=50),
        'code_plage' : fields.integer('Début plage', size=50, required=True),
        'code_type_centre' : fields.many2one('mcisogem.type.centre', 'Type de centre', required=True),
        'dernier_numero' : fields.integer('Dernier numéro'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
    
    _sql_constraints = [('unique_plage_centre', 'unique(numero_plage_centre,code_gest,code_type_centre,code_plage)', "Cette plage de centre existe déjà !"), ]

    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
  
    def create(self, cr, uid, vals, context=None):
        # Récuperation du type de centre
        type_centre_data = self.pool.get('mcisogem.type.centre').browse(cr, uid, vals['code_type_centre'], context=context)
        vals['code_centre'] = type_centre_data.code_type_centre2
        return super(mcisogem_plage_centre, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        # Récuperation du type de centre
        type_centre_data = self.pool.get('mcisogem.type.centre').browse(cr, uid, vals['code_type_centre'], context=context)
        # Ajout des valeurs par defauts
        vals['code_centre'] = type_centre_data.code_type_centre2
        return super(mcisogem_plage_centre, self).write(cr, uid, ids, vals, context=context) 

mcisogem_plage_centre()


class mcisogem_centre(osv.osv):
    
    _name = "mcisogem.centre"
    _description = 'Centre'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_centre': fields.char('Code du centre', size=10, required=False),
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
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
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
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
       
    def onchange_code_ville_centre(self, cr, uid, ids, code_ville, context=None):
            return {'value': {'code_commune' : False}}
    
    def onchange_regl_centre_prestat(self, cr, uid, ids, nom, context=None):
        if not nom:
            return {'value': {'autre_ordre_centre' : False}}
        if nom:
            return {'value': {'autre_ordre_centre' : nom}}

    
    def create(self, cr, uid, vals, context=None):
        # Génaration du code du centre 
        plage_centre_id = self.pool.get('mcisogem.plage.centre').search(cr, uid, args=[('code_type_centre', '=', vals['code_type_centre'])], offset=0, limit=None, order=None, context=None, count=False)
        if not plage_centre_id:
            raise osv.except_osv('Attention !', "Aucune plage centre n'a été définit pour cette plage centre !")
            return False
        else:
            plage_centre_data = self.pool.get('mcisogem.plage.centre').browse(cr, uid, plage_centre_id[0], context=context)
            vals['code_centre'] = plage_centre_data.code_centre + str(plage_centre_data.code_plage) + str(plage_centre_data.dernier_numero)
            dernier_numero = plage_centre_data.dernier_numero + 1
            cr.execute('update mcisogem_plage_centre set dernier_numero =%s where id=%s', (dernier_numero, plage_centre_data.id))
            return super(mcisogem_centre, self).create(cr, uid, vals, context=context)

mcisogem_centre()


class mcisogem_fam_activite(osv.osv):
    
    _name = "mcisogem.fam.activite"
    _description = 'Famille d\'activité'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _sql_constraints = [('unique_fam_activite', 'unique(code_activite,code_fam_prest)', "Cette famille d'activité existe déjà !"), ] 
    
    _columns = {
        'code_activite': fields.char('Code de l\'activite', size=10, required=True),
        'code_fam_prest': fields.integer('Code famille', required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
}
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
    }
    
mcisogem_fam_activite()
    
    
class mcisogem_fam_prest(osv.osv):
    _name = "mcisogem.fam.prest"
    _description = 'Famille d\'actes'
    
    _sql_constraints = [('unique_fam_prest', 'unique(code_langue,libelle_court_famille,code_gest)', "Cette famille d'activité existe déjà !"), ] 
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_famille': fields.integer('Code de la famille', required=True),
        'libelle_court_famille' : fields.char('Libellé court', size=10, required=True),
        'name' : fields.char('Libellé', size=60, required=True),
        'observation_famille' : fields.text('Observation', size=65),
        'type_liasse' : fields.char('type_liasse', size=1),
        'code_sup' : fields.char('cod_sup', size=1),
        'type_fam_act' : fields.integer('type_fam_act'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    _defaults = {
        'type_fam_act': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
  
    def create(self, cr, uid, vals, context=None):
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
        id_famille = super(mcisogem_fam_prest, self).create(cr, uid, vals, context=context)
        
        # Recuperation de l'enregistrement code famille crée
        famille_data = self.pool.get('mcisogem.fam.prest').browse(cr, uid, id_famille, context=context)
        vals1 = {}
        vals1['code_activite'] = famille_data['code_famille']
        vals1['code_fam_prest'] = famille_data['code_famille']
        # vals1['code_gest'] = utilisateur_data.code_gest.id
        # vals1['libelle_gest'] = utilisateur_data.code_gest.name
        self.pool.get('mcisogem.fam.activite').create(cr, uid, vals1, context=context)
        return id_famille    
    
mcisogem_fam_prest()


class mcisogem_nomen_prest(osv.osv):
    _name = "mcisogem.nomen.prest"
    _description = 'Actes'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _sql_constraints = [('unique_nomen_prest', 'unique(code_langue,libelle_court_acte)', "Cette famille d'activité existe déjà !"), ] 
    
    _columns = {
        'libelle_court_acte': fields.char('Code de l\'acte', size=10, required=True),
        'code_fam_prest': fields.many2one('mcisogem.fam.prest', "Code de la famille d'acte", required=True),
        'name' : fields.char('Libellé de l\'acte', size=100, required=True),
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
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
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
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        
}

mcisogem_nomen_prest()
    


class mcisogem_acte_entente_preal(osv.osv):

    _name = "mcisogem.acte.entente.prealable"
    _description = 'Actes soumis à entente préalable'
    
    _sql_constraints = [('unique_nomen_prest', 'unique(code_langue,code_famille)', "Cette famille d'activité figure déjà dans la liste des actes soumis à entente préalable, veuillez la modifier si vous désirez ajouter ou rétirer des actes !"), ] 
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id

    _columns = {
        # 'acte_ids': fields.one2many('mcisogem.nomen.prest','libelle_court_acte', 'Acte'),
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte"),
        'acte_ids': fields.many2many('mcisogem.nomen.prest',
                                       'mcisogem_acte_rel',
                                        'acte_entente_prealable_id',
                                        'code_acte',
                                        'Actes soumis à entente préalable'),
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
    }
        
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}

    def onchange_code_famille_entente(self, cr, uid, ids, code_famille, context=None):
        if not code_famille:
            return {'value': {'code_famille' : False}}
        else:
            # Vérifions si le code famille existe bien en base de données
            cr.execute('select id from mcisogem_acte_entente_prealable where code_famille=%s', (code_famille,))        
            lesactessoumis = cr.dictfetchall()
            if len(lesactessoumis) > 0 :
                raise osv.except_osv('Attention !', "Cette famille d'acte comporte des actes soumis à entente, veuillez procéder à leur modification !")
                return {'value': {'code_famille' : False}}
            else:
                return {'value': {'code_famille' : code_famille}}


mcisogem_acte_entente_preal()


class mcisogem_convention(osv.osv):
    _name = "mcisogem.convention"
    _description = 'Convention'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'numero_convention': fields.integer('Numéro convention', required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'date_debut_convention': fields.datetime('Date d\'effet', required=True),
        'date_fin_convention': fields.datetime('Date de résiliation'),
        'validite_convention': fields.boolean('Validité'),
        'code_sup' : fields.char('cod_sup', size=1),
        'description_convention': fields.text('Description', size=30),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),

    }
    
    _defaults = {
        'date_fin_convention': '1900-01-01 00:00:00',
        'validite_convention': True,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}

    
mcisogem_convention()


class mcisogem_spec_med(osv.osv):
    _name = "mcisogem.spec.med"
    _description = 'Spécialités'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'libelle_court_spec': fields.char('Libellé court spécialité', size=10, required=True),
        'name': fields.char('Libellé spécialité', size=30, required=True),
        'bl_prescr_autoris': fields.boolean('Prescription autorisée'),
        'code_sup' : fields.char('cod_sup', size=1),
        'Nbre_ctr': fields.integer('Nbre_ctr'),
        'code_specialite_reserve': fields.boolean('Spécialité reservée'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),

    }
    
    _sql_constraints = [('unique_spec_med', 'unique(libelle_court_spec,code_langue)', "Cette spécialité existe déjà !"), ]

    _defaults = {
        'Nbre_ctr': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
mcisogem_spec_med()


class mcisogem_prestat(osv.osv):
    _name = "mcisogem.prestat"
    _description = 'Prestataire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'libelle_court_prestat': fields.char('Libellé court', size=10, required=False),
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
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),

    }

    _defaults = {
        'pc_gratuit_prestat': 0,
        'capital': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
    def onchange_code_ville_prestat(self, cr, uid, ids, code_ville, context=None):
            return {'value': {'code_commune' : False}}
    
    def onchange_regl_centre_prestat(self, cr, uid, ids, nom, context=None):
        if not nom:
            return {'value': {'autre_ordre_prestat' : False}}
        if nom:
            return {'value': {'autre_ordre_prestat' : nom}}

    
    
    def create(self, cr, uid, vals, context=None):
        utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)

        # Recuperation de la spécialité
        specialite_data = self.pool.get('mcisogem.spec.med').browse(cr, uid, vals['code_specialite'], context=context)
        vals['nom_prestat'] = specialite_data.name
        print'------------------------------'
        vals['nom_prestat']
        print'------------------------------'
        print utilisateur_data.code_gest_id.id
        
        plage_centre = self.pool.get('mcisogem.plage.centre').search(cr, uid, [('code_centre', '=', vals['nom_prestat'][0]), ('ident_centre', '=', utilisateur_data.code_gest_id.id)], offset=0, limit=None, order=None, context=None, count=False)
        plage_centre_data = self.pool.get('mcisogem.plage.centre').browse(cr, uid, plage_centre[0], context=context)
        vals['libelle_court_prestat'] = vals['nom_prestat'][0] + str(plage_centre_data.code_plage) + str(plage_centre_data.dernier_numero)
        # incrémentation du dernier numero de la plage de centre
        dernier_num = plage_centre_data.dernier_numero + 1
        cr.execute("update mcisogem_plage_centre set dernier_numero=%s where id=%s", (dernier_num, plage_centre_data.id))
        return super(mcisogem_prestat, self).create(cr, uid, vals, context=context)
   
mcisogem_prestat()


class mcisogem_praticien(osv.osv):
    _name = "mcisogem.praticien"
    _description = 'Praticien'


    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'libelle_court_prestat': fields.char('Libellé court', size=10, required=False),
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
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),

    }

    _defaults = {
        'pc_gratuit_prestat': 0,
        'capital': 0,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
    def onchange_code_ville_praticien(self, cr, uid, ids, code_ville, context=None):
            return {'value': {'code_commune' : False}}
    
    def create(self, cr, uid, vals, context=None):
        
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
        return super(mcisogem_praticien, self).create(cr, uid, vals, context=context)
    
mcisogem_praticien()


class mcisogem_type_aff(osv.osv):
    _name = "mcisogem.type.aff"
    _description = 'Type affection'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_type_affection': fields.integer('Code famille', required=True),
        'libelle_court_affection': fields.char('Libellé court', size=10, required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
    
mcisogem_type_aff()


class mcisogem_affec(osv.osv):
    _name = "mcisogem.affec"
    _description = 'Affection'
        
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _columns = {
        'code_affection': fields.integer('Code affection', required=True),
        'type_affection': fields.many2one('mcisogem.type.aff', "Type d'affection", required=True),
        'libelle_court_affection': fields.char('Libellé court', size=10, required=True),
        'name': fields.char('Libellé', size=30, required=True),
        'observation_affection': fields.text('Observation', size=65),
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
  
mcisogem_affec()



class mcisogem_liste_dents(osv.osv):
    _name = "mcisogem.liste.dents"
    _description = 'Liste dents'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    
    _columns = {
        'numero_dent': fields.integer('Numéro dent', required=True),
        'name': fields.char('Libellé dent', size=150, required=True),
        'type_dent' : fields.selection([('1', 'Adulte'), ('2', 'Lait')], 'Type de dent'),
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
mcisogem_liste_dents()


class mcisogem_acte_absence_dents(osv.osv):
    _name = "mcisogem.acte.absence.dents"
    _description = 'Acte d\'extraction de dents'
    _columns = {
        'libelle_court_acte': fields.char('Libellé court', size=10, required=True),
        'name': fields.char('Libellé', size=150, required=True),
        'code_ext_dent' : fields.boolean('Code d\'extraction'),
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
mcisogem_acte_absence_dents()


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
        'code_sup' : fields.char('cod_sup', size=1),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
mcisogem_sous_actes()

class mcisogem_sous_actes_centre(osv.osv):
    _name = "mcisogem.sous.actes.centre"
    _description = 'Sous Actes Centre'
    _columns = {
        'code_centre': fields.many2one('mcisogem.centre', 'Centre', required=True),
        'code_sous_acte': fields.many2one('mcisogem.sous.actes', 'Sous actes', required=True),
        'lbc_sous_acte_interne' : fields.char('Libellé court sous acte interne', size=10, required=True),
        'code_acte': fields.many2one('mcisogem.nomen.prest', 'Actes', required=True),
        'code_fam_prest': fields.many2one('mcisogem.fam.prest', 'Famille d\'acte', required=True),
        'lb_nomen_prest' : fields.char('Libellé acte', size=100, required=True),
        'l_cle_nomen': fields.char('l_cle_nomen', size=3, required=False),
        'mnt_sous_acte': fields.integer('Montant', required=False),
        'sous_acte_autorise': fields.integer('sous_acte_autorise', required=False),
        'dt_deb_souacte': fields.datetime('Date d\'effet', required=True),
        'dt_fin_souacte': fields.datetime('Date de résiliation', required=True),
        'qte_cg' : fields.char('qte_cg', size=50, required=False),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _defaults = {
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}
    
mcisogem_sous_actes_centre()



class mcisogem_tarif_convention(osv.osv):
    _name = "mcisogem.tarif.convention"
    _description = 'Tarif convention'
    _columns = {
        'code_convention': fields.many2one('mcisogem.convention', "Convention", required=True),
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte", required=True),
        'code_acte': fields.many2one('mcisogem.nomen.prest', "Acte", required=False),
        'montant_brut_tarif': fields.integer('Montant brut tarif', required=False),
        'date_effet_tarif': fields.datetime("Date d'effet", required=True),
        'date_resiliation_tarif': fields.datetime("Date de résiliation"),
        'cod_res_conv': fields.integer('cod_res_conv'),
        'code_sup' : fields.char('cod_sup', size=1),
        'affichage' : fields.integer('affichage', required=False),
        'code_tarif_convention_temp': fields.many2many('mcisogem.tarif.convention.temp',
                                       'mcisogem_convention_temp_rel',
                                        'convention_temp_id',
                                        'code_convention',
                                        'Choix des actes', required=False),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=False),
        'code_gest': fields.char('libelle_gest', size=50, required=False),
        'code_langue': fields.char('code_langue', size=10, required=False),
}
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _defaults = {
        'affichage': 0  ,
        'date_resiliation_tarif' : '1900-01-01 00:00:00',
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
}    

    _sql_constraints = [('unique_tarif_convention', 'unique(code_acte,code_convention,date_effet_tarif,date_resiliation_tarif)', "Ce tarif convention existe déjà !"), ]



    def onchange_code_famille_tarif_convention(self, cr, uid, ids, code_famille, context=None):
        
        # Avant tout on vide la table temporaire des tarifs
        # Vidage des tables temporaires
        cr.execute("delete from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
        
        if not code_famille:
            return {'value': {'code_tarif_convention_temp': False}}
        if code_famille:
            data = []
            # Recuperation de la liste de tous les actes de la famille
            cr.execute("select * from mcisogem_nomen_prest where code_fam_prest=%s", (code_famille,))
            lesactes = cr.dictfetchall()
            if len(lesactes) > 0:
               # Insertion de la liste des actes dans la table mcisogem_tarif_convention_temp
               # Parcours de la liste et enregistrement des données en base
               for acte in lesactes:
                   cr.execute("insert into mcisogem_tarif_convention_temp (create_uid,choix,code_famille,code_acte,montant_brut_tarif, write_uid) values(%s, %s, %s, %s, %s, %s)", (uid, False, code_famille, acte['id'], 0, uid))
               cr.execute("select * from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
               lestarifstemp = cr.dictfetchall()
               for tarif in lestarifstemp:
                    data.append(tarif['id'])
               return{'value': {'code_tarif_convention_temp': data}}
            else:
                return {'value': {'code_tarif_convention_temp': False}}
    
    def create(self, cr, uid, vals, context=None):

      dernier_id = 0
        # Recuperation de la date du jour
      datedujour = time.strftime('%d-%m-%y %H:%M:%S', time.localtime())
  
      # Recuperation des lignes qui ont été cochées dans la table mcisogem_tarif_convention_temp
      cr.execute("select * from mcisogem_tarif_convention_temp where write_uid=%s and choix=%s", (uid, True))
      lesactes = cr.dictfetchall()
      if len(lesactes) > 0:
          
          # Recuperation des valeurs par défaut
          utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
          centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest_id.id, context=context)
          
          # Parcours de la liste des actes sélectionné
          for acte in lesactes:
              if not vals['date_resiliation_tarif']:
                  vals['date_resiliation_tarif'] = '1900-01-01 00:00:00'
                  
              # On va verifier pour voir en base de données si il n'existe pas deja un enregistrement pour cette convention et pour cet acte
              cr.execute("select * from mcisogem_tarif_convention where code_convention=%s and code_acte=%s order by id desc", (vals['code_convention'], acte['code_acte']))
              tarifsexistant = cr.dictfetchall()
              # Cas ou c'est la 1ere fois qu'on enregistre les données en base
                          
              if len(tarifsexistant) != 0:
                  # Cas ou la convention et l'acte existe déja - On le modifie avant d'inserer le nouveau
                  cr.execute("""update mcisogem_tarif_convention set date_resiliation_tarif=%s,
                  cod_res_conv=%s where id=%s""", (datedujour, 1, tarifsexistant[0]['id']))
               
              data = {}
              data['create_uid'] = uid      
              data['code_convention'] = vals['code_convention']      
              data['cod_res_conv'] = 0      
              data['code_acte'] = acte['code_acte']    
              data['code_famille'] = acte['code_famille']      
              data['date_effet_tarif'] = vals['date_effet_tarif']      
              data['write_uid'] = uid      
              data['montant_brut_tarif'] = acte['montant_brut_tarif']      
              data['write_date'] = datedujour      
              data['create_date'] = datedujour     
              data['date_resiliation_tarif'] = vals['date_resiliation_tarif']    
              data['affichage'] = 1
              data['code_gest'] = utilisateur_data.code_gest_id.name
              data['ident_centre'] = utilisateur_data.code_gest_id.id
              data['code_langue'] = centre_gestion_data.langue_id.name
              dernier_id = super(mcisogem_tarif_convention, self).create(cr, uid, data, context=context)
              
         # On vide la table des tarifs temporaires
          cr.execute("delete from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
          return dernier_id
      else:
          raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un acte!")
          return 0


    def write(self, cr, uid, ids, vals, context=None):
        if vals['date_resiliation_tarif'] == '1900-01-01 00:00:00':
            vals['cod_res_conv'] = 0
        else:
            vals['cod_res_conv'] = 1
        return super(mcisogem_tarif_convention, self).write(cr, uid, ids, vals, context=context) 

mcisogem_tarif_convention()


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

class mcisogem_tarif_convention_centre_temp(osv.osv):
    _name = "mcisogem.tarif.convention.centre.temp"
    _description = 'Tarif convention Centre Temp'
    _columns = {
        'choix': fields.boolean('Choix'),
        'code_centre': fields.many2one('mcisogem.centre', "Centre", readonly=True),
        'libelle_court_centre': fields.char('Code Centre', readonly=True),
}
    
mcisogem_tarif_convention_centre_temp()


class mcisogem_tarif_convention_centre(osv.osv):
    _name = "mcisogem.tarif.convention.centre"
    _description = 'Tarif convention centre'
    _columns = {
        'code_convention': fields.many2one('mcisogem.convention', "Convention", required=False),
        'code_centre': fields.many2one('mcisogem.centre', "Centre", required=False),
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d\'acte", required=False),
        'code_acte': fields.many2one('mcisogem.nomen.prest', "Acte", required=False),
        'montant_brut_tarif': fields.integer('Montant brut tarif', required=False),
        'montant_plafond_tarif': fields.integer('Montant brut tarif', required=False),
        'date_effet_tarif': fields.datetime("Date d'effet", required=True),
        'date_resiliation_tarif': fields.datetime("Date de résiliation"),
        'cod_res_conv': fields.integer('cod_res_conv'),
        'code_sup' : fields.char('cod_sup', size=1),
        'affichage' : fields.integer('affichage', required=False),
        'affichage_tab_centre' : fields.integer('affichage_tab_centre', required=False),
        'affichage_tab_acte' : fields.integer('affichage_tab_acte', required=False),
        'affichage_famille' : fields.integer('affichage_famille', required=False),
        'affichage_convention' : fields.integer('affichage_convention', required=False),
        'affichage_centre' : fields.integer('affichage_convention', required=False),
        'actions': fields.selection([('1', 'Association Centre - Convention'), ('2', 'Ajouter ou remplacer un acte dans la convention d\'un centre')], 'Quelle action souhaitez-vous mener ?'),
        'code_tarif_convention_temp': fields.many2many('mcisogem.tarif.convention.temp',
                                       'mcisogem_convention_acte_temp_rel',
                                        'convention_acte_temp_id',
                                        'code_convention_acte_temp',
                                        'Choix des actes', required=False),
        'code_tarif_convention_centre_temp': fields.many2many('mcisogem.tarif.convention.centre.temp',
                                       'mcisogem_convention_centre_temp_rel',
                                        'convention_centre_temp_id',
                                        'code_convention_centre_temp',
                                        'Choix des centres', required=False),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
}
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    _defaults = {
              'affichage_tab_centre':0,
              'affichage_tab_acte':0,
              'affichage_convention':0,
              'affichage_famille':0,
              'affichage_centre':0,
              'affichage':0,
              'date_resiliation_tarif' :'1900-01-01 00:00:00',
              'code_gest': _get_cod_gest,
              'ident_centre': _get_cod_gest_id,
              'code_langue': _get_cod_lang,
}    

    _sql_constraints = [('unique_tarif_convention_centre', 'unique(code_acte,code_centre,date_effet_tarif,cod_res_conv)', "Ce tarif centre existe déjà !"), ]


    def onchange_actions(self, cr, uid, ids, actions, context=None):
        
        if not actions:
            return {'value' : {'actions' :  False}}
        else:
            data = []
            if actions == '1':
                 # Recuperation de la liste des centre qui n'ont pas de convention
                # vidage de la table temporaire
                cr.execute("delete from mcisogem_tarif_convention_centre_temp where write_uid=%s", (uid,))
                # Recuperation de la liste de tous les centres
                cr.execute("select * from mcisogem_centre order by name")
                lescentres = cr.dictfetchall()
                if len(lescentres) > 0:
                   # Parcours des centres et insertion des données dans la table temporaire
                   for centre in lescentres:
                        cr.execute("""insert into mcisogem_tarif_convention_centre_temp (create_uid,choix,code_centre,libelle_court_centre,write_uid)
                        values(%s,%s,%s,%s,%s)""", (uid, False, centre['id'], centre['code_centre'], uid))
                   # Recuperation des centres enregistrés en base temporaires
                   cr.execute('select * from mcisogem_tarif_convention_centre_temp where write_uid=%s', (uid,))
                   lescentrestemp = cr.dictfetchall()
                   for ctemp in lescentrestemp:
                       data.append(ctemp['id'])
                   return {'value': {'code_tarif_convention_centre_temp': data, 'affichage_tab_centre': 1, 'affichage_tab_acte': 0,
                                   'affichage_convention':1, 'affichage_centre': 0, 'affichage_famille' : 0  }}
                else:
                    raise osv.except_osv('Attention !', "Veuillez enregistrer au moins un centre !")
                    return {'value': {'affichage_tab_centre': 1, 'affichage_tab_acte': 0}}
            else:
                cr.execute("delete from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
                return {'value': {'affichage_tab_centre': 0, 'affichage_tab_acte': 1, 'code_tarif_convention_temp': [], 'code_famille': False,
                                  'affichage_convention' :0, 'affichage_famille':1, 'affichage_centre' : 1}}
    

    def onchange_code_famille(self, cr, uid, ids, code_famille, context=None):

        # Avant tout on vide la table temporaire des tarifs
        # Vidage des tables temporaires
        cr.execute("delete from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
        
        if not code_famille:
            return {'value': {'code_tarif_convention_temp': False}}
        if code_famille:
            data = []
            # Recuperation de la liste de tous les actes de la famille
            cr.execute("select * from mcisogem_nomen_prest where code_fam_prest=%s", (code_famille,))
            lesactes = cr.dictfetchall()
            if len(lesactes) > 0:
               # Insertion de la liste des actes dans la table mcisogem_tarif_convention_temp
               # Parcours de la liste et enregistrement des données en base
               for acte in lesactes:
                   cr.execute("insert into mcisogem_tarif_convention_temp (create_uid,choix,code_famille,code_acte,montant_brut_tarif, write_uid) values(%s, %s, %s, %s, %s, %s)", (uid, False, code_famille, acte['id'], 0, uid))
               cr.execute("select * from mcisogem_tarif_convention_temp where write_uid=%s", (uid,))
               lestarifstemp = cr.dictfetchall()
               for tarif in lestarifstemp:
                    data.append(tarif['id'])
               return{'value': {'code_tarif_convention_temp': data}}
            else:
                raise osv.except_osv('Attention !', "Cette famille ne comporte aucun acte !")
                return {'value': {'code_tarif_convention_temp': False}}

            
    def create(self, cr, uid, vals, context=None):
        
        if not vals['date_resiliation_tarif']:
            vals['date_resiliation_tarif'] = '1900-01-01 00:00:00'
        
        # Recuperation de la date du jour
        dernier_id = 0
        datedujour = time.strftime('%d-%m-%y %H:%M:%S', time.localtime())
        print'------------------------'
        print datedujour
        
        if not vals['actions']:
            raise osv.except_osv('Attention !', "Veuillez sélectionner une action !")
            return False
        else:
            utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest_id.id, context=context)
            
            # Cas ou actions = 1 - Association centre - convention
            if vals['actions'] == '1':
                # Test pour voir s'il a bien sélectionné une convention
                if not vals['code_convention']:
                    raise osv.except_osv('Attention !', "Veuillez sélectionner une convention !")
                    return False
                else:
                    # Recuperation de la liste des centres sélectionnés
                    cr.execute('select * from mcisogem_tarif_convention_centre_temp where write_uid=%s and choix=%s', (uid, True))
                    lescentreselect = cr.dictfetchall()
                    if len(lescentreselect) > 0:
                        # Parcours de la liste des centres sélectionnés
                        for cs in lescentreselect:
                            cr.execute('select * from mcisogem_tarif_convention_centre where code_convention=%s and code_centre=%s', (vals['code_convention'], cs['code_centre']))
                            verifcentreconventionnes = cr.dictfetchall()
                            # Test le contenu du dictionnaire pour voir si le centre possède déjà une convention si oui on la desactive
                            if len(verifcentreconventionnes) > 0:
                                for cc in verifcentreconventionnes:
                                    cr.execute('update mcisogem_tarif_convention_centre set date_resiliation_tarif=%s, cod_res_conv=%s where id=%s', (datedujour, 1, cc['id']))
                                # Recuperation de la liste de tous les actes de la convention dont cod_res_conv est = 0
                        cr.execute('select * from mcisogem_tarif_convention where code_convention=%s and cod_res_conv=%s', (vals['code_convention'], 0))
                        lesactestarifs = cr.dictfetchall()
                        
                                # Test pour voir si il existe des actes pour cette convention
                        if len(lesactestarifs) > 0:
                            # Parcours de la liste des centres et enregistrement des actes pour le centre
                            for cent in lescentreselect:
                                # Pour chaque centre on va inserer les données relatives au cout des actes
                                # Parcours des actes tarifs
                                for at in lesactestarifs:
                                     data = {}
                                     data['code_convention'] = vals['code_convention']
                                     data['code_centre'] = cent['code_centre']
                                     data['code_acte'] = at['code_acte']
                                     data['montant_brut_tarif'] = at['montant_brut_tarif']
                                     data['date_effet_tarif'] = vals['date_effet_tarif']
                                     data['date_resiliation_tarif'] = vals['date_resiliation_tarif']
                                     data['cod_res_conv'] = 0
                                     data['affichage'] = 3
                                     data['affichage_convention'] = 1
                                     data['affichage_centre'] = 1
                                     data['affichage_famille'] = 0
                                     data['affichage_tab_centre'] = 0
                                     data['affichage_tab_acte'] = 0
                                      # Récuperation de l'utilisateur
                                     data['code_gest'] = utilisateur_data.code_gest_id.name
                                     data['ident_centre'] = utilisateur_data.code_gest_id.id
                                     data['code_langue'] = centre_gestion_data.langue_id.name
                                     dernier_id = super(mcisogem_tarif_convention_centre, self).create(cr, uid, data, context=context)
                            return dernier_id
                        else:
                            raise osv.except_osv('Attention !', "Cette convention ne comporte aucun acte !")
                            return False
                            
                    else:
                        raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un centre !")
                        return False  
                        
            else: 
                # Cas ajout ou remplacement d'un acte
                
                # Tentative de recuperation de la convention du centre
                conv_tarif_centre = {}
                cr.execute('select * from mcisogem_tarif_convention_centre where code_centre=%s and cod_res_conv=%s order by id desc', (vals['code_centre'], 0))
                laconventioncentre = cr.dictfetchall()
                if len(laconventioncentre) > 0:
                    conv_tarif_centre = laconventioncentre[0]
                    vals['code_convention'] = conv_tarif_centre['code_convention']
                    # Recuperation de tous les actes sélectionnés
                    cr.execute('select * from mcisogem_tarif_convention_temp where write_uid=%s and choix=%s', (uid, True))
                    lesactestarifs = cr.dictfetchall()
                    if len(lesactestarifs) > 0:
                        # Parcours des actes pour verification de leur présence ou non dans la liste des tarifs convention centre
                        cr.execute('select * from mcisogem_tarif_convention_centre where code_convention=%s and cod_res_conv=%s and code_centre=%s', (vals['code_convention'], 0, conv_tarif_centre['code_centre']))
                        lesactesconventionnes = cr.dictfetchall()
                        
                        # Si il existe des actes on doit les résilier avant de poursuivre
                        if len(lesactesconventionnes) > 0:
                            for cc in lesactesconventionnes:
                                cr.execute('update mcisogem_tarif_convention_centre set date_resiliation_tarif=%s, cod_res_conv=%s where id=%s', (datedujour, 1, cc['id']))
                         
                        print'----------------------------////*****'
                        print lesactestarifs 
                        for act in lesactestarifs:
                            # Insertion de la nouvelle ligne en base de données
                            data = {}
                            data['code_convention'] = conv_tarif_centre['code_convention']
                            data['code_centre'] = conv_tarif_centre['code_centre']
                            data['code_acte'] = act['code_acte']
                            data['montant_brut_tarif'] = act['montant_brut_tarif']
                            data['date_effet_tarif'] = vals['date_effet_tarif']
                            data['date_resiliation_tarif'] = vals['date_resiliation_tarif']
                            data['cod_res_conv'] = 0
                            data['affichage'] = 3
                            data['affichage_convention'] = 1
                            data['affichage_centre'] = 1
                            data['affichage_famille'] = 0
                            data['affichage_tab_centre'] = 0
                            data['affichage_tab_acte'] = 0  # Récuperation de l'utilisateur
                            data['code_gest'] = utilisateur_data.code_gest_id.name
                            data['ident_centre'] = utilisateur_data.code_gest_id.id
                            data['code_langue'] = centre_gestion_data.langue_id.name
                            dernier_id = super(mcisogem_tarif_convention_centre, self).create(cr, uid, data, context=context)
                             # Enregistrement des données en base
                        return dernier_id
                    else:
                        raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un acte !")
                        return False
                else:
                    raise osv.except_osv('Attention !', "Aucune convention n'a été définit pour ce centre !")
                    return False
                
    def write(self, cr, uid, ids, vals, context=None):
        if vals['date_resiliation_tarif'] == '1900-01-01 00:00:00':
            vals['cod_res_conv'] = 0
        else:
            vals['cod_res_conv'] = 1
        return super(mcisogem_tarif_convention_centre, self).write(cr, uid, ids, vals, context=context) 

mcisogem_tarif_convention_centre()


class mcisogem_bareme(osv.osv):
    _name = "mcisogem.bareme"
    _description = 'Barème Police'
    
    _sql_constraints = [('unique_tarif_convention_centre', 'unique(police_id,college_id,acte_id,date_effet_mod_bareme,territoire_id,cod_statut_benef)', "Ce barème existe déjà !"), ]

    _columns = {
        'police_id': fields.many2one('mcisogem.police', "Police", required=True),
        'college_id': fields.many2one('mcisogem.college', "Collège", required=False),
        'acte_id': fields.many2one('mcisogem.nomen.prest', "Acte", required=False),
        'date_effet_mod_bareme': fields.datetime('Date éffet', required=True),
        'categ_bar': fields.char('Code Centre', size=30, required=False),
        'plf_prest_assure': fields.integer('Plafond Transaction', required=True),
        'ticm_assure': fields.integer('Ticket modérateur', required=True),
        'bl_ticm_assure_tx': fields.boolean('',),
        'ticm_conj': fields.integer('ticm_conj', required=True),
        'bl_ticm_conj_tx': fields.integer('bl_ticm_conj_tx', required=True),
        'ticm_enfant': fields.integer('ticm_enfant', required=True),
        'bl_ticm_enfant_tx': fields.integer('bl_ticm_enfant_tx', required=True),
        'plf_prest_conj': fields.integer('plf_prest_conj', required=False),
        'plf_prest_enfant': fields.integer('plf_prest_enfant', required=False),
        'plf_prest_parent_autre': fields.integer('plf_prest_parent_autre', required=False),
        'plf_prest_parent': fields.integer('plf_prest_parent', required=False),
        'ticm_parent': fields.integer('ticm_parent', required=False),
        'bl_ticm_parent_tx': fields.integer('bl_ticm_parent_tx', required=False),
        'plf_prest_autre': fields.integer('plf_prest_autre', required=False),
        'ticm_autre': fields.integer('ticm_autre', required=False),
        'bl_ticm_autre_tx': fields.integer('bl_ticm_autre_tx', required=False),
        'nbre_plfd_tous': fields.integer('nbre_plfd_tous', required=False),
        'plf_prest_tous': fields.integer('plf_prest_tous', required=False),
        'nbre_plfd_parent_autre': fields.integer('nbre_plfd_parent_autre', required=False),
        'prest_espece_bar': fields.integer('prest_espece_bar', required=False),
        'plf_an_prest': fields.integer('Plafond annuel', required=False),
        'max_act_an_benef': fields.integer('Quantité', required=False),
        'bar_perio_prescrit': fields.integer('Périodicité de prescription', required=False),
        'bar_unite_period': fields.char('bar_unite_period', size=1, required=False),
        'num_ave': fields.char('Avenant', size=1, required=False),
        'plf_prest_fam': fields.integer('Plafond famille assuré', required=False),
        'nbre_plfd_pol': fields.integer('nbre_plfd_pol', required=False),
        'nbre_plfd_fam': fields.integer('nbre_plfd_fam', required=False),
        'cod_sup': fields.char('cod_sup', size=1, required=False),
        'territoire_id': fields.many2one('mcisogem.territoire', "Térritorialité", required=False),
        'cod_statut_benef': fields.many2one('mcisogem.stat.benef', "Statut Bénéficiaire", required=False),
        'date_resiliation_bareme': fields.datetime('Date de résiliation', required=True),
        'mode_bareme': fields.selection([('Q', 'Quantité autorisée'), ('D', 'Date Anniversaire'), ('A', 'Année')], 'Mode barème', required=True),
        'plf_an_fam_act': fields.integer('Plafond famille acte', required=False),
        'max_fam_act_an_benef': fields.integer('max_fam_act_an_benef', required=False),
        'plf_jour': fields.integer('Plafond jour', required=True),
        'unite_temps_id': fields.many2one('mcisogem.unite.temps', "Périodicité de prescription", required=True),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=50, required=True),
        'code_langue': fields.char('code_langue', size=10, required=True),
        
        # Champs pour le formatage de l'affichage
        'code_famille': fields.many2one('mcisogem.fam.prest', "Famille d'acte", required=True),
        'chp_date_effet_histo_police': fields.datetime('Date effet histo police', required=False, readonly=True),
        'chp_date_effet_police': fields.datetime('Date effet police', required=False, readonly=True),
        'chp_souscripteur': fields.char('Souscripteur', readonly=True),
        'chp_assureur': fields.char('Assureur', readonly=True),
        'chp_intermediaire': fields.char('Assur. Interm.', readonly=True),
        'chp_typecontrat': fields.char('Type de contrat', readonly=True),
        'chp_territorialite': fields.char('Térritorialité', readonly=True),
        'plafond_transaction_temp': fields.integer('Plafond Transaction', required=True),
        
        'cod_college_ids':fields.many2many('mcisogem.bareme.college.temp',
                                       'mcisogem_bareme_college_temp_rel',
                                        'college_temp_id',
                                        'code_college', 'Choix des collèges', required=False),
        'cod_statut_benef_ids':fields.many2many('mcisogem.bareme.stat.benef.temp',
                                       'mcisogem_bareme_stat_benef_temp_rel',
                                        'stat_benef_temp_id',
                                        'cod_statut_benef', 'Choix des statuts', required=False),
                
        'cod_acte_ids':fields.many2many('mcisogem.bareme.acte.temp',
                                       'mcisogem_bareme_acte_temp_rel',
                                        'acte_temp_id',
                                        'cod_acte', 'Choix des actes', required=False),
        'chp_affiche': fields.integer('affiche',),
                
}
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id    

    def _get_context(self, cr, uid, context):
        context = context or {}
        return context.get('police')
    

    _defaults = {
        'police_id': _get_context,
        'plf_prest_assure': 999999999,
        'num_ave': 0,
        'plf_prest_fam': 999999999,
        'nbre_plfd_pol': 0,
        'nbre_plfd_fam': 0,
        'date_resiliation_bareme': '1900-01-01 00:00:00',
        'plf_an_fam_act': 999999999,
        'max_fam_act_an_benef': 999999999,
        'plf_jour': 0,
        'plafond_transaction_temp': 999999999,
        'max_act_an_benef': 99,
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
        'code_langue': _get_cod_lang,
        'chp_affiche' : 0,
        'mode_bareme' : 'A',
}
    
    def onchange_code_police(self, cr, uid, ids, police_id, context=None):
        if not police_id:
            return False
        else:
            # Recuperation des inos sur la police pour affichage
            police_data = self.pool.get('mcisogem.police').browse(cr, uid, police_id, context=context)
            # Recuperation de la date de l'histo police
            cr.execute('select dt_eff_mod_pol from mcisogem_histo_police where num_police=%s order by id desc', (police_data.num_interne_police,))
            leshistopolice = cr.dictfetchall()
            if len(leshistopolice) > 0:
                histopolice = leshistopolice[0]
                return {'value': {'chp_date_effet_police': police_data.dt_effet, 'chp_souscripteur': police_data.souscripteur_id.name , 'chp_assureur' : police_data.garant_id.name,
                              'chp_intermediaire' : police_data.courtier_id.name, 'chp_typecontrat' : police_data.type_contrat_id.name, 'chp_territorialite' : police_data.territoire_id.name,
                              'chp_date_effet_histo_police' : histopolice['dt_eff_mod_pol']}}
            else:
                raise osv.except_osv('Attention !', "Aucune historique de police n'a été trouvée pour cette police !")
                return {'value': {'police_id': False }}
      
      
    def onchange_code_famille(self, cr, uid, ids, code_famille, police_id, context=None):
        
        tabcollege = []
        tabstatut = []
        tabacte = []
        
        if not code_famille:
            return False
        else:
            # Test pour voir si une police a bien été sélectionnée
            if not police_id:
                raise osv.except_osv('Attention !', "Veuillez sélectionner la police !")
                return {'value': {'code_famille': False }}
            else:
                # Recuperation de l'historique de police. C'est lui qui nous permettra de recuperer les colleges de la police
                 # Recuperation des infos sur la police
                 police_data = self.pool.get('mcisogem.police').browse(cr, uid, police_id, context=context)
                 # Recuperation de la date de l'histo police
                 cr.execute('select * from mcisogem_histo_police where num_police=%s order by id desc', (police_data.num_interne_police,))
                 leshistopolice = cr.dictfetchall()
                 histopolice = leshistopolice[0]
                 
                 # Recuperation des collèges de la police à partir de l'historique de police
                 cr.execute('select c.id as col,crel.code_college as codc  from college_rel crel,mcisogem_college c where crel.code_college=c.id and crel.name=%s', (histopolice['id'],)) 
                 lescollegespolice = cr.dictfetchall()
                 
                 if len(lescollegespolice) > 0:
                    # Vidage de la table temporaire
                    cr.execute("delete from mcisogem_bareme_college_temp where write_uid=%s", (uid,))
                     
                     # Insertion des collèges dans la table temporaire
                    for col in lescollegespolice:
                        college_data = self.pool.get('mcisogem.college').browse(cr, uid, col['codc'], context=context)
                        cr.execute("insert into mcisogem_bareme_college_temp (create_uid, choix, code, cod_college, write_uid) values (%s, %s, %s, %s, %s) ", (uid, False, college_data.code_college, col['codc'], uid,)) 
                    
                    # Recuperation des collèges enregistrés  
                    cr.execute("select * from mcisogem_bareme_college_temp where write_uid=%s", (uid,))
                    lescollegestemp = cr.dictfetchall()
                    for col in lescollegestemp:
                        tabcollege.append(col['id'])
                        
                    # Vidage de la table temporaire des statuts de bénéficiare
                    cr.execute("delete from mcisogem_bareme_stat_benef_temp where write_uid=%s", (uid,))
                    # Recuperation des statuts de bénéficiaires
                    cr.execute('select * from mcisogem_stat_benef')
                    lesstatutsbenef = cr.dictfetchall()
                    if len(lesstatutsbenef) > 0:
                        # Insertion des statuts de bénéficiaire dans la tabl temporaire
                        for st in lesstatutsbenef:
                            cr.execute("insert into mcisogem_bareme_stat_benef_temp (create_uid,choix, code, cod_statut_benef,write_uid) values(%s, %s, %s, %s, %s)", (uid, False, st['cod_statut_benef'], st['id'], uid))              
                        
                        # Recuperation des statuts de benef enregistrés
                        cr.execute("select * from mcisogem_bareme_stat_benef_temp where write_uid=%s", (uid,))
                        lesstatutstemp = cr.dictfetchall()
                        for st in lesstatutstemp:
                            tabstatut.append(st['id'])
                            
                        # Vidage de la table temporaire des actes
                        cr.execute("delete from mcisogem_bareme_acte_temp where write_uid=%s", (uid,))
                        
                        # Recuperation de la liste des actes appartenant à la famille sélectionnée
                        cr.execute("select * from mcisogem_nomen_prest where code_fam_prest=%s", (code_famille,))
                        lesactesfamille = cr.dictfetchall()
                        
                        if len(lesactesfamille) > 0:
                            # Parcours des actes et insertion dans la table temporaire
                            for act in lesactesfamille:
                                cr.execute("insert into mcisogem_bareme_acte_temp (create_uid, choix, code_acte, cod_acte, write_uid) values (%s, %s, %s, %s, %s)" , (uid, True, act['libelle_court_acte'], act['id'], uid))
                                
                            # Recuperation des actes temporaires enregistré en base
                            cr. execute("select * from mcisogem_bareme_acte_temp where write_uid=%s", (uid,))
                            lesactestemp = cr.dictfetchall()
                            for act in lesactestemp:
                                tabacte.append(act['id'])
                            
                            return {'value' : {'cod_college_ids' : tabcollege, 'cod_statut_benef_ids' : tabstatut, 'cod_acte_ids' : tabacte }}
                        else:
                            raise osv.except_osv('Attention !', "Aucun acte n'a été trouvé pour cette famille d'acte !")
                            return {'value': {'code_famille': False }}  
                    
                    else:
                        raise osv.except_osv('Attention !', "Aucun statut bénéficiaire n'a été trouvé en base de données !")
                        return {'value': {'code_famille': False }} 
                    
                 else:
                    raise osv.except_osv('Attention !', "Cette police ne comporte aucun collège !")
                    return {'value': {'code_famille': False }} 




    def create(self, cr, uid, vals, context=None):
        
        testTicket = True
        # Si bl_ticm_assure_tx est à True on doit s'assurer que le ticket modérateur est compris entre 0 et 100
        if vals['bl_ticm_assure_tx']:
            if vals['ticm_assure'] < 0 or vals['ticm_assure'] > 100:
                testTicket = False
                
        if not testTicket:
            raise osv.except_osv('Attention !', "La valeur du ticket modérateur doit être comprise entre 1 et 100 !")
            return False
        else:
            
            datedujour = time.strftime("%Y-%m-%d", time.localtime())

            utilisateur_data = self.pool.get('res.users').browse(cr, uid, uid, context=context)
            centre_gestion_data = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, utilisateur_data.code_gest_id.id, context=context)
            
            # Recuperation de la liste des statuts de bénéficiaire
            cr.execute("select * from mcisogem_bareme_stat_benef_temp where choix=%s and write_uid=%s", (True, uid))
            lesstatutbenefselect = cr.dictfetchall()
            
            # Recuperation de la liste des collèges sélectionnés
            cr.execute("select * from mcisogem_bareme_college_temp where choix=%s and write_uid=%s", (True, uid))
            lescollegesselect = cr.dictfetchall()
            
            # Recuperation de la liste des actes sélectionnés
            cr.execute("select * from mcisogem_bareme_acte_temp where choix=%s and write_uid=%s", (True, uid))
            lesactesselect = cr.dictfetchall()
            
            if len(lesstatutbenefselect) > 0 and len(lesactesselect) > 0 and len(lescollegesselect) > 0:
                dernier_id = 0
                # Parcours des données récupérées
                compteur_create = 0
                for st in lesstatutbenefselect:
                    for col in lescollegesselect:
                        for act in lesactesselect:
                            
                            # Recuperation des données de la police
                            police_data = self.pool.get('mcisogem.police').browse(cr, uid, vals['police_id'], context=context)
                            
                            #Avant insertion on va chercher à savoir si ce bareme n'existe pas déjà en base de données. Si oui on doit s'assurer que la nouvelle date d'effet est supérieur à la date d'effet du précédent barème
                            test_create = True
                            cr.execute("""select id, date_effet_mod_bareme from mcisogem_bareme where police_id=%s and college_id=%s and acte_id=%s and territoire_id=%s and cod_statut_benef=%s order by date_effet_mod_bareme desc""",
                                       (vals['police_id'],col['cod_college'],act['cod_acte'],police_data.territoire_id.id, st['cod_statut_benef']))
                            lesbaremes = cr.dictfetchall()
                            
                            if len(lesbaremes) > 0:
                                barem = lesbaremes[0]
                                if vals['date_effet_mod_bareme'] > barem['date_effet_mod_bareme']:
                                    #dt_resil = datetime.strptime(vals['date_effet_mod_bareme'], "%Y-%m-%d %H:%M:%S") - timedelta(1)
                                    cr.execute("update mcisogem_bareme set date_resiliation_bareme=%s where id=%s", (vals['date_effet_mod_bareme'],barem['id']))
                                    test_create = True
                                else:
                                    test_create = False 
                            
                            if test_create:
                                compteur_create = compteur_create + 1
                                data = {}
                                data['territoire_id'] = police_data.territoire_id.id
                                data['police_id'] = vals['police_id']
                                data['college_id'] = col['cod_college']
                                data['acte_id'] = act['cod_acte']
                                data['date_effet_mod_bareme'] = vals['date_effet_mod_bareme']
                                
                                if st['code'] == 'A':
                                    data['plf_prest_assure'] = vals['plafond_transaction_temp']
    
                                if st['code'] == 'C':
                                    data['plf_prest_conj'] = vals['plafond_transaction_temp']
                                    
                                if st['code'] == 'E':
                                    data['plf_prest_enfant'] = vals['plafond_transaction_temp'] 
                                    
                                data['ticm_assure'] = vals['ticm_assure']
                                data['bl_ticm_assure_tx'] = vals['bl_ticm_assure_tx']
                                data['ticm_conj'] = vals['ticm_assure']
                                data['bl_ticm_conj_tx'] = vals['bl_ticm_assure_tx']
                                data['ticm_enfant'] = vals['ticm_assure']
                                data['bl_ticm_enfant_tx'] = vals['bl_ticm_assure_tx']
                                
                                data['prest_espece_bar'] = 0
                                data['plf_an_prest'] = vals['plf_an_prest']
                                data['max_act_an_benef'] = vals['max_act_an_benef']
                                
                                # Recuperation de la periodicité de la prescription
                                unite_temps_data = self.pool.get('mcisogem.unite.temps').browse(cr, uid, vals['unite_temps_id'], context=context)
                                data['bar_unite_period'] = unite_temps_data.code_unite_temps
                                
                                data['unite_temps_id'] = vals['unite_temps_id']
                                
                                data['num_ave'] = 0
                                data['plf_prest_fam'] = vals['plf_prest_fam']
                                data['plf_prest_fam'] = vals['plf_prest_fam']
                                
                                data['nbre_plfd_pol'] = 0
                                data['nbre_plfd_fam'] = 0
                                
                                data['cod_statut_benef'] = st['cod_statut_benef']
                                data['date_resiliation_bareme'] = vals['date_resiliation_bareme']
                                data['mode_bareme'] = vals['mode_bareme']
                                data['plf_an_fam_act'] = vals['plf_an_fam_act']
                                data['max_fam_act_an_benef'] = 0
                                data['plf_jour'] = vals['plf_jour']
                                data['code_famille'] = vals['code_famille']
                                data['code_gest'] = utilisateur_data.code_gest_id.name
                                data['ident_centre'] = utilisateur_data.code_gest_id.id
                                data['code_langue'] = centre_gestion_data.langue_id.name
                                
                                data['chp_affiche'] = 1
                                
                                dernier_id = super(mcisogem_bareme, self).create(cr, uid, data, context=context)
                                
                if compteur_create == 0:
                    raise osv.except_osv('Attention !', "La date d'éffet du nouveau barème doit être supérieur à celui du précédent barème !")
                else:
                    return dernier_id                                 

            else:
                raise osv.except_osv('Attention !', "Veuillez sélectionner au moins un statut de bénéficaire, un acte et un collège !")
                return False
            
       
    def write(self, cr, uid, ids, vals, context=None):
        
        # Recuperation des données sur le bareme
        data = self.pool.get('mcisogem.bareme').browse(cr, uid, ids[0], context=context)
        print'-----------------------'
        print data
        print'-----------------------'
        
        if vals['cod_statut_benef']:
            # Recuperation du statut de 
            statut_benef_data = self.pool.get('mcisogem.stat.benef').browse(cr, uid, vals['cod_statut_benef'], context=context)
            if statut_benef_data.cod_statut_benef == 'A':
                if vals['plafond_transaction_temp']:
                    cr.execute("update mcisogem_bareme set plf_prest_assure=%s,  plf_prest_conj=%s, plf_prest_enfant=%s where id=%s", (vals['plafond_transaction_temp'], 0, 0, ids[0]))
                else:
                    cr.execute("update mcisogem_bareme set plf_prest_assure=%s,  plf_prest_conj=%s, plf_prest_enfant=%s where id=%s", (data['plafond_transaction_temp'], 0, 0, ids[0]))
          
            if statut_benef_data.cod_statut_benef == 'C':
                if vals['plafond_transaction_temp']:
                    cr.execute("update mcisogem_bareme set plf_prest_assure=%s,  plf_prest_conj=%s, plf_prest_enfant=%s where id=%s", (0, vals['plafond_transaction_temp'], 0, ids[0]))
                else:
                    cr.execute("update mcisogem_bareme set plf_prest_assure=%s,  plf_prest_conj=%s, plf_prest_enfant=%s where id=%s", (0, data['plafond_transaction_temp'], 0, ids[0]))

            if statut_benef_data.cod_statut_benef:
                if vals['plafond_transaction_temp']:
                    cr.execute("update mcisogem_bareme set plf_prest_assure=%s,  plf_prest_conj=%s, plf_prest_enfant=%s where id=%s", (0, 0, vals['plafond_transaction_temp'], ids[0]))
                else:
                    cr.execute("update mcisogem_bareme set plf_prest_assure=%s,  plf_prest_conj=%s, plf_prest_enfant=%s where id=%s", (0, 0, data['plafond_transaction_temp'], ids[0]))
                
        if vals['ticm_assure']:
            cr.execute("update mcisogem_bareme set ticm_assure=%s, ticm_conj=%s, ticm_enfant=%s where id=%s", (vals['ticm_assure'], vals['ticm_assure'], vals['ticm_assure'], ids[0]))   
            
        if vals['bl_ticm_assure_tx']:
            cr.execute("update mcisogem_bareme set bl_ticm_assure_tx=%s, bl_ticm_conj_tx=%s, bl_ticm_enfant_tx=%s where id=%s", (vals['bl_ticm_assure_tx'], vals['bl_ticm_assure_tx'], vals['bl_ticm_assure_tx'], ids[0]))   
           
        if vals['unite_temps_id']:
            unite_temps_data = self.pool.get('mcisogem.unite.temps').browse(cr, uid, vals['unite_temps_id'], context=context)
            cr.execute("update mcisogem_bareme set bar_unite_period=%s where id=%s", (unite_temps_data.code_unite_temps, ids[0]))
                
        return super(mcisogem_bareme, self).write(cr, uid, ids, vals, context=context) 


class mcisogem_bareme_stat_benef_temp(osv.osv):
    _name = "mcisogem.bareme.stat.benef.temp"
    _description = 'Statut du beneficiaire'
    
    _columns = {
        'choix': fields.boolean('Choix'),
        'code': fields.char('Code Statut', readonly=True),
        'cod_statut_benef':fields.many2one('mcisogem.stat.benef', 'name', 'Libellé', readonly=True),
    }
    
    def onchange_choix(self, cr, uid, ids, choix, context=None):
        cr.execute("update mcisogem_bareme_stat_benef_temp set choix=%s where id=%s", (choix, ids[0]))

class mcisogem_bareme_college_temp(osv.osv):
    _name = "mcisogem.bareme.college.temp"
    _description = 'Collège'
    
    _columns = {
       'choix': fields.boolean('Choix'),
       'code': fields.char('Code Collège', readonly=True),
       'cod_college':fields.many2one('mcisogem.college', 'name', 'Collège', readonly=True),
    }
    
    def onchange_choix(self, cr, uid, ids, choix, context=None):
        cr.execute("update mcisogem_bareme_college_temp set choix=%s where id=%s", (choix, ids[0]))

class mcisogem_bareme_acte_temp(osv.osv):
    _name = "mcisogem.bareme.acte.temp"
    _description = 'Famille d\'acte'
    
    _columns = {
       'choix': fields.boolean('Choix'),
       'code_acte': fields.char('Code de l\'acte', readonly=True),
       'cod_acte':fields.many2one('mcisogem.nomen.prest', 'name', 'Désignation de l \'acte', readonly=True),
    }
    
    def onchange_choix(self, cr, uid, ids, choix, context=None):
        cr.execute("update mcisogem_bareme_acte_temp set choix=%s where id=%s", (choix, ids[0]))

class mcisogem_college_temporaire(osv.osv):
    _name = "mcisogem.college.temporaire"

    _columns = {
        
        'name': fields.many2one('mcisogem.college','name','Collège'),
    }
        

class mcisogem_benef(osv.osv):
    _name = "mcisogem.benef"
    _description = 'beneficiaire'
    GROUPE = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    ]
    
    def _get_group(self, cr, uid, context=None):
        cr.execute('select gid from res_groups_users_rel where uid=%s', (uid,))
        group_id = cr.fetchone()[0]
        group_obj = self.pool.get('res.groups').browse(cr, uid, group_id, context=context)
        if group_obj.name == 'Financial Manager':
            return True
        else:
            return False
    
     
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, ids, name, value, args, context=None):
        return self.write(cr, uid, ids, {'image': tools.image_resize_image_big(value)}, context=context)
   
    _columns = {
        'police_id': fields.many2one('mcisogem.police', "Police", required=True),
        'college_id': fields.many2one('mcisogem.college.temporaire', 'Collège'),
        'col_id':fields.many2one('mcisogem.college','Collège'),
        'garant_id': fields.many2one('mcisogem.garant', "Garant",required=True),
        'avenant_id':fields.many2one('mcisogem.avenant', 'avenant'),
        'souscripteur_id': fields.many2one('mcisogem.souscripteur', 'Souscripteur', required=True),
        'matric_benef': fields.char('matricule',readonly=True),
        'name': fields.char('Nom', required=True),
        'nom_jeun_fille': fields.char('Nom de jeune fille'),
        'prenom_benef': fields.char('prenom',required=True),
        'adr_benef': fields.char('adresse'),
        'cod_bp_benef': fields.char('code BP'),
        'bp_benef': fields.char('Bp benef'),
        'tel_benef': fields.char('Téléphone'),
        'fax_benef': fields.char('Fax'),
        'matric_chez_souscr': fields.char('Matricule chez souscripteur'),
        'dt_naiss_benef': fields.date('Date de naissance', required=True),
        'lieu_naiss_benef':fields.char('Lieu de naissance'),
        'couverture': fields.integer('Couverture'),
        'rang': fields.integer('Rang'),
        'sexe_id': fields.many2one('mcisogem.sexe', "Genre",required=True),
        'mod_paiem_benef': fields.integer('mod_paiem_benef'),
        'num_banq_benef': fields.char('Code Banque'),
        'num_guichet_benef': fields.char('No Guichet'),
        'num_compt_benef': fields.char('No Compte Bancaire'),
        'cle_rib_benef': fields.char('Clé Rib'),
        'cum_an_recl_benef': fields.integer('cum_an_recl_benef'),
        'cum_an_recl_fam': fields.integer('cum_an_recl_fam'),
        'poids_benef': fields.char('Poids bénef'),
        'taille_benef': fields.char('Taille'),
        'dt_mensuration': fields.datetime('Date mensuration'),
        'group_sang_benef': fields.selection(GROUPE, 'Groupe Sanguin', select=True),
        'bl_trt_en_cours': fields.char('Bl. Traitement en cours'),
        'trt_en_cours_until':fields.char('Traitement en cours'),
        'specif_trav_benef': fields.char('Specifications travail'),
        'predisp_benef': fields.char('Predispositon'),
        'allergie_benef': fields.char('Allergie'),
        'anteced_medic': fields.char('Antecedant médical'), 
        'anteced_obstetric': fields.char('Antecedant obstetric'), 
        'anteced_fam': fields.char('Antecedants familiaux'),
        'anteced_chir': fields.char('Antecedant chirugical'), 
        'transfus_benef': fields.char('Transfusion'), 
        'prothese_benef': fields.char('Prothese'), 
        'obs_benef': fields.char('obs_benef'),
        'image': fields.binary("Image",
            help="This field holds the image used as image for the product, limited to 1024x1024px."),
        'image_medium': fields.function(_get_image, fnct_inv=_set_image,
            string="Medium-sized image", type="binary", multi="_get_image",
            store={
                'mcisogem.benef': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Medium-sized image of the product. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved, "\
                 "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        'image_small': fields.function(_get_image, fnct_inv=_set_image,
            string="Small-sized image", type="binary", multi="_get_image",
            store={
                'mcisogem.benef': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            },
            help="Small-sized image of the product. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required."),
        'numavenant': fields.integer('numero avenant'), 
        'numcarte': fields.char('numero carte'), 
        'tmp_stamp_photo': fields.char('tmp_stamp_photo'), 
        'cod_photo': fields.integer('cod_photo'),
        'photo_ben': fields.char('photo_ben'),
        'affiche': fields.boolean('',),
        'affiche_col':fields.boolean('',),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=10, required=True),
        'state': fields.selection([
            ('draft', "Nouveau"),
            ('sent', "Comptabilité"),
            ('done', "Informations Comptable"),
            ('cancel', "Annuler"),
            ('finish', "Terminer"),
        ], 'Status', required=True, readonly=True)
    }
      
    '''def _numero_matricule(self, cr, uid, context=None):
        cr.execute('select num_benef from mcisogem_numero')        
        numero = cr.fetchone()[0]
        print '*****************'
        print numero
        inc_num=numero + 1
        print '*****************'
        print inc_num
        return inc_num '''

    _defaults = {
        'state':'draft',
        'couverture':0,
        'rang':0,
        'affiche':_get_group,       
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
    }                

    def button2_to_sent(self, cr, uid, ids, context=None):
        """L utilisateur envoi la requete a la comptabilite pour ajouter les informations comptable"""
        # souscripteur = self.pool.get('mcisogem.souscripteur').browse(cr, uid, uid, context=context)
        # usr = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        message = 'Un souscripteur a ete creer veuillez renseigner les informations comptable'
        
        cr.execute('select id from res_groups where name=%s', ('Settings',))
        group_id = cr.fetchone()[0]
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        ident_centre = cr.fetchone()[0]
        res_users = self.pool('res.users')
        user_ids = res_users.search(
            cr, SUPERUSER_ID, [
                ('code_gest_id', '=', ident_centre),
                ('groups_id', 'in', group_id)
            ], context=context)     
        partner_id = []
        
        if user_ids:
            partner = self.pool.get('res.partner').browse(cr, uid, uid, context=context) 
            partner_id = list(set(u.partner_id.id for u in res_users.browse(cr, SUPERUSER_ID, user_ids, context=context)))
            partner.message_post(cr, uid, False,
                                 body=message,
                                 partner_ids=partner_id,
                                 subtype='mail.mt_comment', context=context
            )            
        return self.write(cr, uid, ids, {'state':'done'}, context=context)
    
    def button2_to_done(self, cr, uid, ids, context=None):
        """La comptabilite renseigne et valide les informations comptable"""
        compta = self.read(cr, uid, ids, ['num_banq_benef', 'num_compt_benef', 'num_compt_benef', \
                        'cle_rib_benef'])        
        if not compta['num_banq_benef'] or not compta['num_compt_benef'] or not compta['num_compt_benef'] or not compta['cle_rib_benef']:
            raise osv.except_osv('Attention !', "Vous devez renseigner tous les champs comptable avant de valider!")
            return False;
        self.write(cr, uid, ids, {'state':'finish'}, context=context)
        return True
    
    def button2_to_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'done'}, context=context)
        return True 


    def onchange_police(self, cr, uid, ids, police_id, context=None):        
        if not police_id:
            return False
        else:

            datedujour = time.strftime('%Y-%m-%d', time.localtime())
            cr.execute("select distinct code_college from mcisogem_histo_police where name=%s and dt_eff_histo_pol >=%s", (police_id, datedujour))
            lescollegespolices = cr.dictfetchall()

            cr.execute("delete from mcisogem_college_temporaire where create_uid=%s", (uid,))

            for col in lescollegespolices:                 
                 cr.execute("insert into mcisogem_college_temporaire (create_uid,write_uid,name) values(%s, %s, %s)", (uid, uid, col['code_college']))

        

 
    def create(self, cr, uid, vals, context=None):
        
        
         # Recuperation des informations relatives à l'exercice de la police
        cr.execute("select * from mcisogem_exercice_police where police_id=%s order by id desc", (vals['police_id'],))
        lesexercicespolices = cr.dictfetchall()       
        
        
        # Recuperation des données relatives à la police
        cr.execute("select * from mcisogem_police where id=%s", (vals['police_id'],))
        lapolice = cr.dictfetchall()[0]
        
        
         # Test pour voir si cette police possède un exercice de police
        if len(lesexercicespolices) > 0:
        
            #recuperation du numero auto dans la table avenant
            cr.execute("select * from mcisogem_avenant where name=%s order by id desc", (lapolice['typ_ave'],))
            numave = cr.dictfetchall()[0]

            #contraintes ajout benef
            cr.execute('select * from mcisogem_benef where name=%s and prenom_benef=%s and sexe_id=%s and dt_naiss_benef=%s', (vals['name'],vals['prenom_benef'],vals['sexe_id'],vals['dt_naiss_benef']))
            nbr_benef=cr.dictfetchall()

            cr.execute('select num_benef from mcisogem_numero')        
            numero = cr.fetchone()[0]
            benef = numero + 1

            if len(nbr_benef)==0:
                
                vals['matric_benef'] = benef
                vals['cum_an_recl_benef'] = 0
                vals['cum_an_recl_fam'] = 0
                vals['numcarte'] = 0  
                vals['state'] = 'done'                  
                    
                res = super(mcisogem_benef, self).create(cr, uid, vals, context)
                cr.execute("update mcisogem_numero set num_benef=%s", (benef,))
                return res
                
            else: 
                raise osv.except_osv('Attention !', "Ce beneficiaire existe déja !")
                return {'value': {'police_id': False}} 

            # Test pour voir si il s'agit d'une police par tranche d'age ou par statut de bénéficiaire
        
            #police par statut beneficiaire
            if lapolice['type_prime']=='1':                
                
                #insertion des donnees
                data = {}
                data['matric_benef']=benef
                data['police_id']=vals['police_id']
                data['col_id']=vals['college_id']
                data['garant_id']=vals['garant_id']
                data['avenant_id']=vals['eavenant_id']
                data['souscripteur_id']=vals['souscripteur_id']
                data['matric_benef']=vals['matric_benef']
                data['dt_eff_mod_benef']=lambda *a: time.strftime("%Y-%m-%d")
                data['police_id']=vals['police_id']
                data['lbc_souscr_id']=lapolice['souscripteur_id']
                
                data['sal_brut_benef']=0
                data['dt_entree_benef']=lambda *a: time.strftime("%Y-%m-%d")
                data['st_creat_incorpo']='C'
                data['st_retr_excl']='A'
                data['dt_sortie_benef']='01-01-1900 00:00:00'
                data['bl_excl_definitive']=2
                data['college_id']=vals['college_id']
                data['bl_remb_autorise']=1
                data['st_ace_benef']='A'
                data['ass_matric_benef']=vals['matric_benef']
                data['tmp_stamp']=lambda *a: time.strftime("%Y-%m-%d")
                data['num_ave']=numave['id']
                data['pc_sal_prime']=0
                data['bl_pc_sal_prime']=0
                data['num_ave_cal']=0
                data['num_ave_pol']=numave['num_ave_interne_police']
                data['num_ave_ret']=vals['typeavenant_id']
                data['histo_st_eleve']=0
                data['cod_statut_benef']=1
                data['matric_chez_souscr']=vals['matric_chez_souscr']
                data['activation']=0
                
                data['id_tran_age']=1
                data['cod_gesti']=vals['code_gest']
                data['mode_prime']=0
                data['valide_quittance']=0
                data['date_quittance']='01-01-1900 00:00:00'
                data['cod_util_quittance']=uid
                res = super(mcisogem_histo_benef, self).create(cr, uid, data, context)
                return res
            else:
                 #police par tranche d'age
                
                 #insertion des donnees
                data = {}
                data['police_id']=vals['police_id']
                data['college_id']=vals['college_id']
                data['garant_id']=vals['garant_id']
                data['avenant_id']=vals['avenant_id']
                data['souscripteur_id']=vals['souscripteur_id']
                data['matric_benef']=vals['matric_benef']
                data['dt_eff_mod_benef']=lambda *a: time.strftime("%Y-%m-%d")
                data['police_id']=vals['police_id']
                data['lbc_souscr_id']=lapolice['souscripteur_id']
                
                data['sal_brut_benef']=0
                data['dt_entree_benef']=lambda *a: time.strftime("%Y-%m-%d")
                data['st_creat_incorpo']='C'
                data['st_retr_excl']='A'
                data['dt_sortie_benef']='01-01-1900 00:00:00'
                data['bl_excl_definitive']=2
                data['college_id']=vals['college_id']
                data['bl_remb_autorise']=1
                data['st_ace_benef']='A'
                data['ass_matric_benef']=vals['matric_benef']
                data['tmp_stamp']=lambda *a: time.strftime("%Y-%m-%d")
                data['num_ave']=numave['id']
                data['pc_sal_prime']=0
                data['bl_pc_sal_prime']=0
                data['num_ave_cal']=0
                data['num_ave_pol']=numave['num_ave_interne_police']
                data['num_ave_ret']=vals['typeavenant_id']
                data['histo_st_eleve']=0
                data['cod_statut_benef']=1
                data['matric_chez_souscr']=vals['matric_chez_souscr']
                data['activation']=0
                
                data['id_tran_age']=0
                data['cod_gesti']=vals['code_gest']
                data['mode_prime']=0
                data['valide_quittance']=0
                data['date_quittance']='01-01-1900 00:00:00'
                data['cod_util_quittance']=uid
                result = super(mcisogem_histo_benef, self).create(cr, uid, data, context)                    
                  
                return res                  
                                 
        else:
            raise osv.except_osv('Attention !', "Cette police n'a pas été associée à un exercice de police !")
            return False
      
class mcisogem_sexe(osv.osv):
    _name = "mcisogem.sexe"
    _description = 'sexe'
    
    _columns = {
        
       'name':fields.char('Libellé'),
       'code':fields.char('code')
    }
    
class mcisogem_benef_college_temp(osv.osv):
    _name = "mcisogem.benef.college.temp"
    _description = 'College temporare'
    
    _columns = {
        
       'name':fields.many2one('mcisogem.college', 'name', 'College'),
       
    }
class mcisogem_typeavenant_temp(osv.osv):
    _name = "mcisogem.typeavenant.temp"
    _description = 'type avenant temporaire'
    
    _columns = {
        
       'name':fields.many2one('mcisogem.type.avenant', 'name', 'Type avenant'),
       
    }
    
class mcisogem_histo_benef(osv.osv):
    _name = "mcisogem.histo.benef"
    _description = 'historique de beneficiaire'
    
    def _get_cod_gest(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        return gest_obj.code_centre
    
    
    def _get_cod_lang(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))
        cod_gest_id = cr.fetchone()[0]
        gest_obj = self.pool.get('mcisogem.centre.gestion').browse(cr, uid, cod_gest_id, context=context)
        # lang_obj = self.pool.get('mcisogem.langue').browse(cr, uid, gest_obj.langue_id, context=context)
        return gest_obj.langue_id.name
    
    def _get_cod_gest_id(self, cr, uid, context=None):
        cr.execute('select code_gest_id from res_users where id=%s', (uid,))        
        cod_gest_id = cr.fetchone()[0]
        return cod_gest_id
    _columns = {
        'police_id': fields.many2one('mcisogem.police', "Police", required=True),
        'college_id': fields.many2one('mcisogem.benef.college.temp', "Collège"),
        'garant_id': fields.many2one('mcisogem.garant', "Garant",required=True),
        'avenant_id':  fields.many2one('mcisogem.avenant', "Type Avenant"),
        'matric_benef': fields.char('matricule',readonly=True),
        'name': fields.char('Nom', required=True),
        'prenom_benef': fields.char('prenom',required=True),
        'souscripteur_id': fields.many2one('mcisogem.souscripteur', 'Souscripteur', required=True),
        'matric_benef': fields.char('matricule',readonly=True),
        'dt_eff_mod_benef': fields.datetime('date de naissance', required=True),
        'police_id': fields.many2one('mcisogem.police', "Police", required=True),
        'lbc_souscr_id': fields.many2one('mcisogem.souscripteur', "Souscripteur", required=True),
        'lbc_crit_stat': fields.char('Nom', required=True),
        'zone_geo_id': fields.many2one('mcisogem.zone', 'Zone géographique'),
        'code_ville': fields.many2one('mcisogem.ville', "ville", required=True),
        'sal_brut_benef':  fields.integer('sal_brut_benef'),
        'dt_entree_benef': fields.datetime('Date entrée bénéficiaire'),
        'st_creat_incorpo': fields.char('st_creat_incorpo'),
        'st_retr_excl': fields.char('st_retr_excl'),
        'dt_sortie_benef': fields.datetime('dt_sortie_benef'),
        'bl_excl_definitive':  fields.integer('bl_excl_definitive'),
        'college_id': fields.many2one('mcisogem.benef.college.temp', "Collège"),
        'bl_remb_autorise':  fields.integer('bl_remb_autorise'),
        'st_ace_benef': fields.char('st_ace_benef'),
        'ass_matric_benef':  fields.integer('ass_matric_benef'),
        'tmp_stamp': fields.datetime('tmp_stamp'),
        'num_ave': fields.integer('num_ave'),
        'pc_sal_prime': fields.integer('pc_sal_prime'),
        'bl_pc_sal_prime': fields.integer('bl_pc_sal_prime'),
        'num_ave_cal': fields.integer('num_ave_cal'),
        'num_ave_pol': fields.integer('num_ave_pol'),
        'num_ave_ret': fields.integer('num_ave_ret'),
        'histo_st_eleve': fields.boolean('Statut Eleve'),
        'cod_statut_benef': fields.many2one('mcisogem.stat.benef', 'name', 'Libellé', readonly=True),
        'matric_chez_souscr': fields.char('matric_chez_souscr'),
        'activation': fields.boolean('activation'),
        'photo_ben_fam': fields.char('photo ben fam'),
        'id_tran_age': fields.many2one('mcisogem.tranche.age', 'Tranche d\'age', required=False),
        'cod_gesti': fields.integer('cod_gesti'),
        'mode_prime': fields.integer('Mode prime'),
        'valide_quittance': fields.integer('valide_quittance'),
        'date_quittance': fields.datetime('Date quittance'),
        'cod_util_quittance': fields.char('cod_util_quittance'),
        'ident_centre': fields.many2one('mcisogem.centre.gestion', 'Centre de gestion', required=True),
        'code_gest': fields.char('libelle_gest', size=10, required=True),
    }
    
    _defaults = {
         
        'code_gest': _get_cod_gest,
        'ident_centre': _get_cod_gest_id,
    }


    
