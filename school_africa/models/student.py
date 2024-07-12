from odoo import models, fields, api

class Student(models.Model):
    _name = 'school.student'
    _description = 'School Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=1)
    birth_date = fields.Date(string='Birth Date', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Char(string='Address')
    class_id = fields.Many2one('school.class', string='Class', required=True, tracking=2)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    color = fields.Integer(string='Color')

    # Parent fields
    parent1_name = fields.Char(string='Parent 1 Name')
    parent1_phone = fields.Char(string='Parent 1 Phone')
    parent1_email = fields.Char(string='Parent 1 Email')
    parent1_address = fields.Char(string='Parent 1 Address')

    parent2_name = fields.Char(string='Parent 2 Name')
    parent2_phone = fields.Char(string='Parent 2 Phone')
    parent2_email = fields.Char(string='Parent 2 Email')
    parent2_address = fields.Char(string='Parent 2 Address')

    @api.depends('name', 'class_id')
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} ({record.class_id.name})"
            result.append((record.id, name))
        return result