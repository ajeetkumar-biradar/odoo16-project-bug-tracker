from odoo import models, fields

class Project(models.Model):
    _inherit = 'project.project'

    assignee_ids = fields.Many2many('res.users',string='Assignees',tracking=True)
