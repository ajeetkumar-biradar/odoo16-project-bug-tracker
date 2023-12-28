from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    progress = fields.Integer(tracking=True)
    progress_percentage = fields.Float(compute='_compute_progress_percentage')
