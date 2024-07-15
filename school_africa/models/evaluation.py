from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Evaluation(models.Model):
    _name = 'school.evaluation'
    _description = 'School Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    max_note = fields.Integer(string='Max note', required=True, default=20)
    course_id = fields.Many2one('school.course', string='Course', required=True)
    class_id = fields.Many2one('school.class', string='Class', related='course_id.class_id', store=True, readonly=True)
    period_id = fields.Many2one('school.period', string='Period', related='course_id.period_id',
                                store=True, readonly=True)
    matiere_id = fields.Many2one('school.matiere', string='Matiere', related='course_id.matiere_id')
    professor_id = fields.Many2one('school.professor', string='Professor', related='course_id.professor_id')
    evaluation_date = fields.Date(string='Evaluation Date', required=True)
    supervisor_id = fields.Many2one('res.users', string='Supervisor', required=False)
    other_supervisor = fields.Char(string='Other Supervisor')
    note_ids = fields.One2many('school.note', 'evaluation_id', string='Notes')
    coefficient_evaluation = fields.Float(string='Coefficent Evaluation', default=1.0, required=True)
    max_score = fields.Float(string='Max Score', compute='_compute_max_score')
    min_score = fields.Float(string='Min Score', compute='_compute_min_score')
    @api.constrains('evaluation_date', 'course_id')
    def _check_evaluation_date_within_period(self):
        for record in self:
            if record.course_id:
                period = record.course_id.period_id
                if record.evaluation_date < period.start_date or record.evaluation_date > period.end_date:
                    raise ValidationError('The evaluation date must be within the period of the associated course.')

    @api.model
    def create(self, vals):
        evaluation = super(Evaluation, self).create(vals)
        if evaluation.course_id.class_id:
            notes = []
            students = self.env['school.student'].search([('class_id', '=', evaluation.course_id.class_id.id)])
            for student in students:
                notes.append((0, 0, {
                    'evaluation_id': evaluation.id,
                    'student_id': student.id,
                }))
            evaluation.note_ids = notes
        return evaluation

    def _compute_max_score(self):
        for rec in self:
            rec.max_score = rec.note_ids and max(rec.note_ids.mapped('result')) or 0

    def _compute_min_score(self):
        for rec in self:
            rec.min_score = rec.note_ids and min(rec.note_ids.mapped('result')) or 0
