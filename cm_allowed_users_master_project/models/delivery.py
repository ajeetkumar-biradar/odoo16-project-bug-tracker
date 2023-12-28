from odoo import models, fields

class Project(models.Model):
    _inherit = 'project.project'

    allowed_user_ids = fields.Many2many(
        'res.users',
        string='Project Team',
        domain=[('share', '=', False), ('active', '=', True)],
    )
    assignee_ids = fields.Many2many(
        'res.users',
        relation='project_user_rel',
        column1='project_id',
        column2='user_id',
        string='Assignees',
        context={'active_test': False},
        tracking=True,
    )

    def _compute_allowed_users(self):
        for project in self:
            allowed_users = project.assignee_ids.filtered(lambda user: not user.share)
            project.allowed_user_ids = allowed_users
