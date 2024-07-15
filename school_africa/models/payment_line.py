from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PaymentLine(models.Model):
    _name = 'school.payment.line'
    _description = 'Payment Line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('school.student', string='Student', required=True, tracking=1)
    payment_date = fields.Date(string='Payment Date', tracking=2)
    start_date = fields.Date(string='Start Date', required=True, tracking=3)
    end_date = fields.Date(string='End Date', required=True, tracking=4)
    status = fields.Selection([
        ('cancelled', 'Cancelled'),
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Status', default='unpaid', tracking=5)
    class_id = fields.Many2one('school.class', string='Class', required=True, tracking=6)
    school_year_id = fields.Many2one('school.year', string='School Year', related='class_id.school_year_id', store=True)
    amount = fields.Float(string='Amount', required=True, tracking=7)

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    @api.depends('student_id', 'class_id', 'start_date')
    def _compute_name(self):
        for record in self:
            month = record.start_date.strftime('%B') if record.start_date else ''
            record.name = f"{record.student_id.name} - {record.class_id.name} - {month}"

    @api.depends('student_id', 'class_id', 'start_date')
    def _compute_name(self):
        for record in self:
            if record.start_date:
                month_year = record.start_date.strftime('%B %Y')
                record.name = f"{record.student_id.name} - {record.class_id.name} - {month_year}"
            else:
                record.name = f"{record.student_id.name} - {record.class_id.name}"
