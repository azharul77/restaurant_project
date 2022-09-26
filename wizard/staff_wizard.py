
from odoo import models, fields

class RestStaffWizard(models.TransientModel):
    _name = 'rest.staff.wizard'
    _description = 'This is a wizard which will update the information of staff'

    full_name = fields.Char(string="Name", size=50)
    age = fields.Integer(string="Age")
    dob = fields.Date(string="DOB")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    country_id = fields.Many2one('res.country', string="Country")
    country_ids = fields.Many2many('res.country', string="Countries")
    country_code = fields.Char(string = "Country Code", related="country_id.code")
    gender = fields.Selection([('male', 'Male'),('female', 'Female')], string="Gender")
    staff_line_ids = fields.One2many('rest.staff.wizard.lines', 'connecting_field', string="Staff Line")
    image = fields.Binary(string="Image")
    hand_salary = fields.Float(string="In Hand Salary")
    epf_esi = fields.Float(string="EPF+ESI")
    ctc_salary = fields.Float(string="CTC")

    def update_info_fun(self):
        active_id = self._context.get('active_id')
        upd_var = self.env['rest.staff'].browse(active_id)
        country_lst = []
        for vals in self.country_ids:
            country_lst.append(vals.id)

        lst2 = []


        for vals2 in self.staff_line_ids:
             lst2.append((0,0,{
                'name': vals2.name,
                'product_id': vals2.product_id.id
             }))


        upd_var.staff_line_ids = [(5,0,0)]        
        vals = {'full_name': self.full_name,
                'age': self.age,
                'mobile': self.mobile,
                'dob': self.dob,
                'email': self.email,
                # for Manytoone field
                'country_id': self.country_id.id,
                # for Manytomany fileds 
                'country_ids': [(6,0,country_lst)],
                # for Onetomany 
                'staff_line_ids': lst2
        }
        upd_var.write(vals)



class RestStaffWizardLine(models.TransientModel):
    _name = 'rest.staff.wizard.lines'

    connecting_field = fields.Many2one('rest.staff.wizard', string="Staff ID")
    name = fields.Char(string="Name")
    product_id = fields.Many2one("product.product", string="Product")
    sequence = fields.Integer(string="Seq.")         