from odoo import models, fields

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'School Class'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=1)
    school_year_id = fields.Many2one('school.year', string='School Year', required=True, tracking=2)
    main_professor_id = fields.Many2one('school.professor', string='Main professor', tracking=3)
    level_id = fields.Many2one('school.level', string='Niveau de la classe', required=True, tracking=4)
    student_ids = fields.One2many('school.student', 'class_id', string='Students')
    tuition_fees = fields.Float(string='Tuition Fees')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    color = fields.Integer(string='Color')
