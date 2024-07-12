from odoo import models, fields, api

class SchoolYear(models.Model):
    _name = 'school.year'
    _description = 'School Year'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True, tracking=1)
    start_date = fields.Date(string='Start Date', required=True, tracking=2)
    end_date = fields.Date(string='End Date', required=True, tracking=3)
    period_ids = fields.One2many('school.period', 'school_year_id', string='Periods')
    message_ids = fields.One2many('mail.message', 'res_id', domain=[('model', '=', 'school.year')], string='Messages')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
