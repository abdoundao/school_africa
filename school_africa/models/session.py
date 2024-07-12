from odoo import models, fields, api

class Session(models.Model):
    _name = 'school.session'
    _description = 'Course Session'

    course_id = fields.Many2one('school.course', string='Course', required=True)
    start_datetime = fields.Datetime(string='Start Date and Time', required=True)
    end_datetime = fields.Datetime(string='End Date and Time', required=True)
    professor_id = fields.Many2one('school.professor', string='Professor', related='course_id.professor_id', store=True, readonly=True)
    class_id = fields.Many2one('school.class', string='Class', related='course_id.class_id', store=True, readonly=True)
    color = fields.Integer(string='Color', related='course_id.matiere_id.color', store=True, readonly=True)
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    @api.depends('course_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.class_id.name} - {record.course_id.matiere_id.name} - {record.professor_id.name}"

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.class_id.name} - {record.course_id.matiere_id.name} - {record.professor_id.name}"
            result.append((record.id, name))
        return result
