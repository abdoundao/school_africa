from odoo import models, fields, api
from datetime import timedelta

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
    tuition_fees = fields.Float(string='Tuition Fees')
    payment_line_ids = fields.One2many('school.payment.line', 'student_id', string='Payment Lines', readonly=True)
    note_ids = fields.One2many('school.note', 'student_id', string='Notes', readonly=True)
    absence_ids = fields.One2many('school.absence', 'student_id', string='Absences', readonly=True)

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

    @api.model
    def create(self, vals):
        student = super(Student, self).create(vals)
        if 'class_id' in vals:
            student._create_payment_lines()
        return student

    def write(self, vals):
        res = super(Student, self).write(vals)
        if 'class_id' in vals:
            self._create_payment_lines()
        return res

    def _create_payment_lines(self):
        for student in self:
            class_id = student.class_id
            school_year = class_id.school_year_id
            start_date = fields.Date.from_string(school_year.start_date)
            end_date = fields.Date.from_string(school_year.end_date)
            current_date = start_date

            while current_date <= end_date:
                month_start = current_date.replace(day=1)
                next_month = month_start + timedelta(days=32)
                month_end = next_month.replace(day=1) - timedelta(days=1)

                self.env['school.payment.line'].create({
                    'student_id': student.id,
                    'amount': student.tuition_fees,
                    'start_date': month_start,
                    'end_date': month_end,
                    'class_id': class_id.id,
                    'school_year_id': school_year.id,
                })

                current_date = next_month

    @api.onchange('class_id')
    def _onchange_class_id(self):
        if self.class_id:
            self.tuition_fees = self.class_id.tuition_fees

    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Generate Report',
            'res_model': 'student.report.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_id': self.id},
        }