from odoo import models, fields, api

class Professor(models.Model):
    _name = 'school.professor'
    _description = 'School Professor'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=1)
    birth_date = fields.Date(string='Birth Date', required=True)
    hire_date = fields.Date(string='Hire Date', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    salary = fields.Float(string='Salary')
    department = fields.Char(string='Department')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    color = fields.Integer(string='Color')
    matiere_ids = fields.Many2many('school.matiere', string='Matieres Taught')


    @api.depends('name', 'matiere_ids')
    def name_get(self):
        result = []
        for record in self:
            matieres = ''.join([m.name[:3].upper() for m in record.matiere_ids])
            name = f"{record.name} ({matieres})"
            result.append((record.id, name))
        return result