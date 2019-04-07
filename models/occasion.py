from odoo import fields, models


class Occasion(models.Model):
    _name = 'myosotis.occasion'
    type = fields.Char(required=True)
    date = fields.Date()
    remarks = fields.Text()
    location_id = fields.Many2one('myosotis.location')
