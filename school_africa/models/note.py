from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Note(models.Model):
    _name = 'school.note'
    _description = 'School Note'

    evaluation_id = fields.Many2one('school.evaluation', string='Evaluation', required=True, ondelete='cascade')
    student_id = fields.Many2one('school.student', string='Student', required=True)
    class_id = fields.Many2one('school.class', string='Class', related='student_id.class_id', store=True, readonly=True)
    period_id = fields.Many2one('school.period', string='Period', related='evaluation_id.course_id.period_id', store=True, readonly=True)
    max_note = fields.Integer(string='Max note', related='evaluation_id.max_note', store=True, readonly=True)
    coefficient_evaluation = fields.Float(string='Coefficent Evaluation', related='evaluation_id.coefficient_evaluation', store=True, readonly=True)
    result = fields.Float(string='Result')

    @api.constrains('student_id', 'class_id')
    def _check_student_class(self):
        for record in self:
            if record.student_id.class_id != record.evaluation_id.class_id:
                raise ValidationError('The selected student does not belong to the class of this note.')

    @api.constrains('result', 'max_note')
    def _check_result(self):
        for record in self:
            if record.result < 0 or record.result > record.max_note:
                raise ValidationError('The result must be between 0 and the maximum note of the evaluation.')
