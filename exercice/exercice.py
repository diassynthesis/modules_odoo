# -*- coding:utf8 -*-
from pprint import pprint
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


class exercice_inscription(osv.osv):
    _name = "exercice.inscription"
    _description = 'Inscription'
    
    _columns = {
        'batiment_id': fields.many2one('exercice.batiment','batiment', required=True),
        'classe_id': fields.many2one('exercice.classe','classe', required=True),
        'etudiant_id': fields.many2one('exercice.etudiant','Matricule', required=True),
        'nom': fields.char('Nom' , readonly=True),
        'date_ins' :fields.date('Date inscription'),
        'prenom': fields.char('Prenoms' , readonly=True),
        'state': fields.selection([
            ('P', "Preinscription"),
            ('I', "Inscription"),
            ('D', "Diplome"),
        ],required=True),
    }

    _defaults = {
        'state' : 'P',
        'date_ins': datetime.today().strftime('%Y-%m-%d'),
    }

    _rec_name = 'etudiant_id'

    def button_to_preinscrire(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'P'}, context=context)
        return True 

    def button_to_inscrire(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'I'}, context=context)
        return True 

    def button_to_diplomer(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'D'}, context=context)
        return True 

    def onchange_etudiant(self, cr, uid, ids, etudiant_id):
        v = {}
        if etudiant_id:
            etudiant = self.pool.get('exercice.etudiant').search(cr, uid, [('id', '=', etudiant_id)])
            for etudiant_data in self.pool.get('exercice.etudiant').browse(cr, uid, etudiant):
                v = { 'nom': etudiant_data.nom, 'prenom': etudiant_data.prenom}
        return{'value':v}

class exercice_batiment(osv.osv):
    _name = "exercice.batiment"
    _description = 'Batiment'
    
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Libelle Batiment', required=True),
    }


class exercice_filiere(osv.osv):
    _name = "exercice.filiere"
    _description = 'Filiere'
    
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Libelle classe', required=True),
    }


class exercice_classe(osv.osv):
    _name = "exercice.classe"
    _description = 'Classe'
    
    _columns = {
        'code': fields.char('Code', required=True),
        'name': fields.char('Libelle classe', required=True),
        'filiere_id':fields.many2one('exercice.filiere' , 'filiere' , required=True),
        'batiment_id':fields.many2one('exercice.batiment' , 'Batiment' , required=True),
        'matiere_ids':fields.many2many('exercice.matiere' , 'exercice_classe_matiere_rel' ,'code_m' , 'code' ,'Matieres'),
    }

    _sql_constraints = [('unique_code_classe', 'unique(code)', "Ce code a déjà été utilisé !"),]
    def select_matiere_classe(self, cr, uid, ids, classe_id):
        matiere = self.pool.get('exercice.matiere').search(cr, uid, [('classe_id', '=', classe_id )])
        for matiere_data in self.pool.get('exercice.matiere').browse(cr, uid, matiere):
            v = { 'code_m': matiere_data.code_m, 'name': matiere_data.name}
        return {'value':v}


    def button_etudiant_classe(self , cr , uid , ids, context=None):
        ctx = (context or {}).copy()
        
        ctx['classe'] = ids[0]
        ctx['tree_view_ref'] = 'view_etudiant_tree'
        ctx['form_view_ref'] = 'view_etudiant_form'

        if ctx['classe'] :
            return {
                    'name':'Etudiants',
                    'view_type':'form',
                    'view_mode':'tree,form',
                    'res_model':'exercice.etudiant',
                    'view_id':False,
                    'target':'current',
                    'type':'ir.actions.act_window',
                    'domain':[('classe_id', '=', ids[0])],
                    'context':ctx,
                    'nodestroy':True,
                    }
        else : return True

class exercice_evaluer(osv.osv):
    _name = "exercice.evaluer"
    _description = 'Evaluation des Etudiants'
    
    _columns = {
        'code':fields.char('Code' , required=True),
        'matiere_id' : fields.many2one('exercice.matiere','Matiere',required=True),
        'note' : fields.float('Note'),
        'etudiant_id' : fields.many2one('exercice.etudiant' , 'Etudiant')
    }

    _sql_constraints = [('unique_code_evaluer', 'unique(code)', "Ce code a déjà été utilisé !"),]
    _rec_name = 'note'

    def onchange_etudiant(self, cr, uid, ids, etudiant_id):
        v = {}
        if etudiant_id:
            etudiant = self.pool.get('exercice.etudiant').search(cr, uid, [('id', '=', etudiant_id)])
            for etudiant_data in self.pool.get('exercice.etudiant').browse(cr, uid, etudiant):
                v = { 'nom': etudiant_data.nom, 'prenom': etudiant_data.prenom , 'classe_id' : etudiant_data.classe_id}
        return{'value':v}

class exercice_etudiant(osv.osv):
    _name = "exercice.etudiant"
    _description = 'Etudiant'

    def _calcul_moyenne(self, cr, uid, ids, name, args, context):

        res = {}
        print('**********************++++++++++++++++******************')
        print(context.get('active_id',False))
        for idd in ids:
            re={}
            print('*********************************************************')
            print(idd)
            etu_en_cours  = self.search(cr, uid, [('id', '=', idd)])
            etudiant_data = self.browse(cr , uid ,etu_en_cours)
        
            i=0
            notes=0
            moyenne=0
            ses_notes = self.pool.get('exercice.evaluer').search(cr, uid, [('etudiant_id', '=', etudiant_data.name)])

            print('********************************** les notes ************************')
            for ses_notes_data in  self.pool.get('exercice.evaluer').browse(cr , uid ,ses_notes):
                notes += ses_notes_data.note 
                i+=1
                
                print(ses_notes_data.note)
                moyenne = notes / i
            print('************************ la moyenne **************************')
            print(moyenne)
                
            for elmt in self.browse(cr, uid, ids,context):
               re[elmt.id]=moyenne
            return re
            res +=re
        return res

    _columns = {
        'name': fields.char('Matricule', required=True),
        'nom': fields.char('Nom', required=True),
        'prenom': fields.char('prenom(s)'),
        'sexe': fields.selection([('M', 'masculin'), ('F', 'feminin')], 'Sexe'),
        'dnaiss' :fields.date('Date  de Naissance'),
        'classe_id' :fields.many2one('exercice.classe' , 'classe' , required=True),
        'note_id' :fields.one2many('exercice.evaluer','etudiant_id','Notes'),
        'moyenne' : fields.function(_calcul_moyenne, string='Moyenne' , type='float'),
    }

    _sql_constraints = [('unique_name', 'unique(name)', "Ce matricule existe déjà !"),]


    # fonction permettant de modifier le sexe d un etudiant a la volee
    def button_modifier_sexe(self,cr,uid,ids,context=None):
        etudiant = self.pool.get('exercice.etudiant').search(cr, uid, [('id', '=', ids)])
        etudiant_data = self.pool.get('exercice.etudiant').browse(cr, uid, etudiant)

        if etudiant_data.sexe == 'M' :
            return self.write(cr ,uid ,ids, {'sexe' : 'F'} , context)
        elif etudiant_data.sexe == 'F':
            return self.write(cr ,uid ,ids, {'sexe' : 'M'} , context)

    def create(self, cr, uid, vals, context=None):
        masculin = self.pool.get('exercice.etudiant.masculin')
        feminin  = self.pool.get('exercice.etudiant.feminin')
        if vals['sexe']=='M':
            masculin.create(cr,uid,vals,context)
        elif vals['sexe']=='F':
            feminin.create(cr,uid,vals,context)
        return super(exercice_etudiant, self).create(cr, uid, vals, context=context)

   
    # def write(self , cr , uid ,ids, vals , context=None):
    #     matricule=""
    #     masculin = self.pool.get('exercice.etudiant.masculin')
    #     feminin  = self.pool.get('exercice.etudiant.feminin')

    #     # selection de l etudiant en cours de modif 
    #     etudiant = self.pool.get('exercice.etudiant').search(cr, uid, [('id', '=', ids)])

    #     # on recupere toutes ses infos
    #     for etudiant_data in self.pool.get('exercice.etudiant').browse(cr, uid, etudiant):
    #         v = { 'id' : etudiant_data.id,'name' : etudiant_data.name,'nom': etudiant_data.nom, 'prenom': etudiant_data.prenom , 'sexe' : etudiant_data.sexe ,'dnaiss' : etudiant_data.dnaiss }


    #     if masculin.search_count(cr, uid, [('name','=',v['name'])]) > 0:
    #         # si l etudiant est de sexe masculin alors on le selectionne dans la table masculin
    #         rech_masculin = masculin.search(cr, uid, [('name','=',v['name'])])

    #         # recuperation de son id
    #         for masculin_data in masculin.browse(cr, uid, rech_masculin):
    #             id_etu = masculin_data.id
            
    #         if vals['sexe']=='M':

    #             # si il n y a aucune modif sur le sexe alors on mert a jour l element
    #             masculin.write(cr, uid,ids,vals, context=context) # Aucune modif sur le sexe
    #         else:
    #             v['sexe']='F'

    #             #si le sexe a ete modifie on cree l element 
    #             masculin.unlink(cr,uid,id_etu,context=context)
    #             #cr.execute('delete from exercice_etudiant_masculin where id=%s', (id_etu,))
    #             feminin.create(cr,uid,v,context)  # modif d'un masculin en feminin
                
    #     elif feminin.search_count(cr, uid, [('name', '=', v['name'])]) > 0:
    #         # si l etudiant est de sexe feminin alors on le selectionne dans la table feminin
    #         rech_feminin = feminin.search(cr, uid, [('name','=',v['name'])])

    #          # recuperation de son id
    #         for feminin_data in feminin.browse(cr, uid, rech_feminin):
    #             id_etu = feminin_data.id


    #         if vals['sexe']=='F':
    #           # si il n y a aucune modif sur le sexe alors on mert a jour l element
    #             feminin.write(cr, uid,ids[0],vals,context=context)
    #         else:
    #             v['sexe']='M'
                
    #             feminin.unlink(cr,uid,id_etu,context=context)
    #             #cr.execute('delete from exercice_etudiant_feminin where id=%s', (id_etu,))
    #             masculin.create(cr,uid,v,context) ##modif d'un feminin en masculin 
                
            

    #     return super(exercice_etudiant, self).write(cr, uid,ids,vals, context=context)
        
class exercice_etudiant_masculin(osv.osv):
    _name = "exercice.etudiant.masculin"
    _description = 'Etudiant masculins'
    
    _columns = {
        'name': fields.char('Matricule', required=True),
        'nom': fields.char('Nom', required=True),
        'prenom': fields.char('prenom(s)'),
        'sexe': fields.selection([('M', 'masculin'), ('F', 'feminin')], 'Sexe'),
        'dnaiss' :fields.date('Date  de Naissance'),
        'classe_id' :fields.many2one('exercice.classe' , 'classe'),
    }

class exercice_etudiant_feminin(osv.osv):
    _name = "exercice.etudiant.feminin"
    _description = 'Etudiant feminins'
    
    _columns = {
        'name': fields.char('Matricule', required=True),
        'nom': fields.char('Nom', required=True),
        'prenom': fields.char('prenom(s)'),
        'sexe': fields.selection([('M', 'masculin'), ('F', 'feminin')], 'Sexe'),
        'dnaiss' :fields.date('Date de Naissance'),
        'classe_id' :fields.many2one('exercice.classe' , 'classe'),
    }

class exercice_matiere(osv.osv):
    _name =  "exercice.matiere"
    _description = "Matiere"

    _columns = {
        'code_m' : fields.char('Code matiere' , required=True),
        'name' : fields.char('Matiere' , required=True),
    }


