from odoo import models, fields, api

class Matiere(models.Model):
    _name = 'school.matiere'
    _description = 'School Matiere'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=1)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    color = fields.Integer(string='Color')
    professor_ids = fields.Many2many('school.professor', string='Professors', compute='_compute_professor_ids')

    @api.depends('name')
    def _compute_professor_ids(self):
        for matiere in self:
            matiere.professor_ids = self.env['school.professor'].search([('matiere_ids', 'in', matiere.id)])
