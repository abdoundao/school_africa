from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Course(models.Model):
    _name = 'school.course'
    _description = 'School Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Course Name', compute='_compute_name', store=True)
    class_id = fields.Many2one('school.class', string='Class', required=True, track_visibility='onchange')
    matiere_id = fields.Many2one('school.matiere', string='Matiere', required=True, track_visibility='onchange')
    professor_id = fields.Many2one('school.professor', string='Professor', required=True, track_visibility='onchange')
    course_line_ids = fields.One2many('school.course.line', 'course_id', string='Course Lines')
    period_id = fields.Many2one('school.period', string='Period', required=True)
    visible = fields.Boolean(string='Visible', default=True)
    active = fields.Boolean(string='Active', default=True)
    session_ids = fields.One2many('school.session', 'course_id', string='Sessions')
    coefficient = fields.Float(string='Coefficent', default=1.0, required=True)

    @api.depends('matiere_id', 'class_id', 'professor_id', 'period_id')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.matiere_id.name} - {record.class_id.name} - {record.professor_id.name} - {record.period_id.name}"

    @api.constrains('period_id', 'class_id')
    def _check_period_in_school_year(self):
        for record in self:
            if record.class_id and record.period_id:
                if record.period_id.school_year_id != record.class_id.school_year_id:
                    raise ValidationError("The selected period is not within the same school year as the class.")

    def action_create_evaluation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Evaluation',
            'res_model': 'school.evaluation',
            'view_mode': 'form',
            'context': {
                'default_course_id': self.id,
                'default_name': self.name,
            },
            'target': 'new',
        }

    def action_generate_sessions(self):
        for course in self:
            # Delete existing sessions with start date greater than today
            course.session_ids.filtered(lambda s: s.start_datetime > fields.Datetime.now()).unlink()

            period_start_date = fields.Date.from_string(course.period_id.start_date)
            if period_start_date and period_start_date < fields.Date.today():
                period_start_date = fields.Date.today()
            period_end_date = fields.Date.from_string(course.period_id.end_date)

            for course_line in course.course_line_ids:
                current_date = period_start_date
                while current_date <= period_end_date:
                    if current_date.weekday() == int(course_line.day_of_week):
                        start_datetime = (datetime.combine(current_date, datetime.min.time()) +
                                          timedelta(hours=course_line.start_hour, minutes=course_line.start_minute))
                        end_datetime = (datetime.combine(current_date, datetime.min.time()) +
                                        timedelta(hours=course_line.end_hour, minutes=course_line.end_minute))
                        self.env['school.session'].create({
                            'course_id': course.id,
                            'start_datetime': start_datetime,
                            'end_datetime': end_datetime,
                        })
                    current_date += timedelta(days=1)
