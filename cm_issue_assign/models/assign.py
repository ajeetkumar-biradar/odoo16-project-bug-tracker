from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    user_ids = fields.Many2many(
        'res.users',
        string='Assign',
        # Replace with your actual group name
    )

    manager_id = fields.Many2one('res.users', string='Project Manager', readonly=True)

    project_id = fields.Many2one('project.project', string='Project')

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            # Assuming that the project manager is stored in the project record
            self.manager_id = self.project_id.user_id.id
            # Send an email notification to the project manager
