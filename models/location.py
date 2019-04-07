from odoo import models, fields


class Location(models.Model):
    _name = 'myosotis.location'

    city = fields.Char(required=True)
    area = fields.Char(required=True)
    remarks = fields.Text()
