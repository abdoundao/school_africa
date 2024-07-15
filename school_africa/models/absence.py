from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Absence(models.Model):
    _name = 'school.absence'
    _description = 'Student Absence'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    student_id = fields.Many2one('school.student', string='Student', required=True, domain="[('class_id', '=', class_id)]")
    session_id = fields.Many2one('school.session', string='Session', required=True)
    start_datetime = fields.Datetime(string='Start Date and Time', related='session_id.start_datetime', store=True, readonly=True)
    end_datetime = fields.Datetime(string='End Date and Time', related='session_id.end_datetime', store=True, readonly=True)
    class_id = fields.Many2one('school.class', string='Class', related='session_id.class_id', store=True, readonly=True)
    justified = fields.Boolean(string='Justified')
    justification_attachment_id = fields.Many2many('ir.attachment', string='Attachments')

    @api.constrains('student_id', 'session_id')
    def _check_student_class(self):
        for record in self:
            if record.student_id.class_id != record.session_id.class_id:
                raise ValidationError("The student must belong to the same class as the session.")

    @api.onchange('justification_attachment_id')
    def _onchange_class_id(self):
        if self.justification_attachment_id:
            self.justified = True

    @api.depends('student_id', 'class_id', 'start_datetime')
    def _compute_name(self):
        for record in self:
            month = record.start_datetime.strftime('%B') if record.start_datetime else ''
            record.name = f"Absence {record.student_id.name} - {record.class_id.name} - {month}"