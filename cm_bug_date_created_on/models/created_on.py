from odoo import models, fields, api
from datetime import date


class ProjectTask(models.Model):
    _inherit = 'project.task'

    created_on = fields.Date(string="created on", readonly=True, default=date.today(), format='%d-%m-%y')