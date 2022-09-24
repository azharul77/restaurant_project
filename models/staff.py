# from pyexpat import model,api,_
from copy import copy
from email.policy import default
from  odoo.exceptions import ValidationError, UserError
import string
from odoo import models, fields,api,_

class RestStaff(models.Model):
    _name = 'rest.staff'
    _description = 'This model will store the data of our staff'
    _rec_name = 'full_name'
    _inherit = ['mail.thread','mail.activity.mixin']
    _order = 'age desc'

    def new_fun(self):
        print("Executed a function by object button.....")

    def delete_one2many(self):
        for record in self:
            if record.staff_line_ids:
                record.staff_line_ids = [(5, 0, 0)]
                return {
                    'effect':{
                        'fadeout': 'slow',
                        'type': 'rainbow_man',
                        'message': 'Record has been deleted successfully'
                    }
                }

    def check_orm(self):
        search_var = self.env.ref('restaurant_project.rest_staff_form_view_id')
        print("Ref is-----------------",search_var.type,"name--------",search_var.name)
       

    def do_resign(self):
        for rec in self:
            rec.status = "resgined"

    @api.constrains('age')
    def val_age(self):
        for record in self:
            if record.age <= 18:
                raise ValidationError(_('The age must be above than 18'))

    @api.model
    def create(self,vals):
        if vals.get("seq_num", ('New')) == ('New'):
            vals['seq_num'] = self.env['ir.sequence'].next_by_code('rest.seq.staff') or _('New')
        res = super(RestStaff,self).create(vals)
        if vals.get('gender') == 'male':
            res['full_name'] = "Mr. " + res['full_name']
            print("res['full_name']----", res['full_name'])
        elif vals.get('gender') == 'female':
            res['full_name'] = "Mrs." + res['full_name']
            print("res['full_name']----", res['full_name'])
        else:
            return res      
        return res


    def write(self,vals):
        res = super(RestStaff, self).write(vals)
        print("res----",res,"self-------",self, "vals------",vals)
        return res     
    
    def unlink(self):
        for rec in self:
            if rec.status == 'active':
                raise UserError(_("Record can not be deleted, if it is in active state"))
        return super(RestStaff, self).unlink()


    full_name = fields.Char(string="Name", size=50,track_visibility='always')
    age = fields.Integer(string="Age")
    dob = fields.Date(string="DOB")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    country_id = fields.Many2one('res.country', string="Country")
    country_ids = fields.Many2many('res.country', string="Countries")
    country_code = fields.Char(string = "Country Code", related="country_id.code")
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], string="Gender")
    staff_line_ids = fields.One2many('rest.staff.lines', 'connecting_field', string="Staff Line")
    sequence = fields.Integer(string="Seq.")
    status = fields.Selection([('active','Avtive'),('resgined', 'Resgined')], string="Status", readonly=True, default="active")
    image = fields.Binary(string="Image")
    hand_salary = fields.Float(string="In Hand Salary")
    epf_esi = fields.Float(string="EPF+ESI")
    ctc_salary = fields.Float(string="CTC", compute="calc_ctc")
    seq_num = fields.Char(string="Secquence no.",readonly=True,copy=False,index=True,default= lambda self: _('New'))
    rating = fields.Selection([('0', 'Very Low'),('1', 'Low'),('2','Normal'),('3','High'),('4','Very High'),('5','Excellent')], string="Rate me")

    @api.depends('hand_salary','epf_esi')
    def calc_ctc(self):
        for record in self:
            ctc = 0
            if record.hand_salary:
                ctc = ctc + record.hand_salary
            if record.epf_esi:
                ctc = ctc + record.epf_esi
            record.ctc_salary = ctc    


   

class RestStaffLine(models.Model):
    _name = 'rest.staff.lines'

    connecting_field = fields.Many2one('rest.staff', string="Staff ID")
    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", string="Product")
    sequence = fields.Integer(string="Seq.")     
