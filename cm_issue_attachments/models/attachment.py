from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    document_ids = fields.Many2many('ir.attachment', string='Upload Files')

    assignee_ids = fields.Many2many('res.users', relation='allowed_project_user_rel', column1='task_id',
                                    column2='user_id', string='Assignees', context={'active_test': False},
                                    tracking=True)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            allowed_user_ids = self.project_id.allowed_user_ids.ids
            return {
                'domain': {'assignee_ids': [('id', 'in', allowed_user_ids)]}
            }

    @api.onchange('assignee_ids')
    def _onchange_assignee_ids(self):
        if self.project_id:
            allowed_user_ids = self.project_id.allowed_user_ids.ids
            return {
                'domain': {'assignee_ids': [('id', 'in', allowed_user_ids)]}
            }