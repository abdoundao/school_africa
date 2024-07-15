from odoo import models, fields, api


class StudentReportWizard(models.TransientModel):
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    student_id = fields.Many2one('school.student', string='Student')
    note_ids = fields.One2many('school.note', string='Notes', compute='_compute_notes')
    absence_ids = fields.One2many('school.absence', string='Absences', compute='_compute_absences')

    @api.depends('start_date', 'end_date', 'student_id')
    def _compute_notes(self):
        for record in self:
            record.note_ids = self.env['school.note'].search([
                ('student_id', '=', record.student_id.id),
                ('evaluation_id.evaluation_date', '>=', record.start_date),
                ('evaluation_id.evaluation_date', '<=', record.end_date)
            ])

    @api.depends('start_date', 'end_date', 'student_id')
    def _compute_absences(self):
        for record in self:
            record.absence_ids = self.env['school.absence'].search([
                ('student_id', '=', record.student_id.id),
                ('start_datetime', '>=', record.start_date),
                ('end_datetime', '<=', record.end_date)
            ])

    def generate_report(self):
        self.ensure_one()
        self.student_id = self.env['school.student'].browse(self.env.context.get('active_id'))
        self._compute_notes()
        self._compute_absences()

        return self.env.ref('school_africa.student_report_action').report_action(self)
