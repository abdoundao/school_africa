from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CourseLine(models.Model):
    _name = 'school.course.line'
    _description = 'School Course Line'

    course_id = fields.Many2one('school.course', string='Course', required=True)
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday')
    ], string='Day of the Week', required=True)
    start_hour = fields.Integer(string='Start Hour', required=True)
    start_minute = fields.Integer(string='Start Minute', required=True)
    end_hour = fields.Integer(string='End Hour', required=True)
    end_minute = fields.Integer(string='End Minute', required=True)

    @api.constrains('start_hour', 'start_minute', 'end_hour', 'end_minute')
    def _check_time_validity(self):
        for record in self:
            if not (0 <= record.start_hour < 24):
                raise ValidationError('Start hour must be between 0 and 23.')
            if not (0 <= record.end_hour < 24):
                raise ValidationError('End hour must be between 0 and 23.')
            if not (0 <= record.start_minute < 60):
                raise ValidationError('Start minute must be between 0 and 59.')
            if not (0 <= record.end_minute < 60):
                raise ValidationError('End minute must be between 0 and 59.')
            start_time = record.start_hour * 60 + record.start_minute
            end_time = record.end_hour * 60 + record.end_minute
            if start_time >= end_time:
                raise ValidationError('Start time must be before end time.')
