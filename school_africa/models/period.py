from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class Period(models.Model):
    _name = 'school.period'
    _description = 'School Period'
    _order = 'position'

    name = fields.Char(string='Name', required=True)
    position = fields.Integer(string='Position', required=True)
    school_year_id = fields.Many2one('school.year', string='School Year', required=True)
    start_date = fields.Date(string='Start Date', required=True, default=lambda self: date.today())
    end_date = fields.Date(string='End Date', required=True, default=lambda self: date.today() + timedelta(days=30))

    _sql_constraints = [
        ('unique_position_per_year', 'unique(school_year_id, position)', 'The position must be unique per school year!')
    ]

    @api.constrains('position')
    def _check_position_unique(self):
        for record in self:
            if self.search_count([('school_year_id', '=', record.school_year_id.id), ('position', '=', record.position)]) > 1:
                raise ValidationError('The position must be unique per school year!')

    @api.constrains('start_date', 'end_date', 'school_year_id')
    def _check_dates_within_school_year(self):
        for record in self:
            if record.start_date < record.school_year_id.start_date or record.end_date > record.school_year_id.end_date:
                raise ValidationError('The period dates must be within the school year dates.')

    @api.depends('name', 'school_year_id')
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} ({record.school_year_id.name})"
            result.append((record.id, name))
        return result
