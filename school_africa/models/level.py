from odoo import models, fields

class SchoolLevel(models.Model):
    _name = 'school.level'
    _description = 'School Level'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, track_visibility='onchange')
    level = fields.Integer(string='Level', required=True, track_visibility='onchange')
