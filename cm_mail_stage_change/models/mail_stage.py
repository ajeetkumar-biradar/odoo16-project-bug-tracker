from odoo.exceptions import UserError
from odoo import models, fields, api


class CustomProjectTask(models.Model):
    _inherit = 'project.task'

    issue_creator_id = fields.Many2one('res.users', string='Issue Creator')
    old_stage_name = fields.Char(string='Old Stage Name', store=True, readonly=True)
    is_first_stage = fields.Boolean(string='Is First Stage', default=True, copy=False)

    @api.model
    def create(self, values):
        if 'stage_id' in values:
            new_stage_id = values.get('stage_id')
            old_stage = self.env['project.task.type'].browse(new_stage_id).name if new_stage_id else 'N/A'

            values['old_stage_name'] = old_stage
            task = super(CustomProjectTask, self).create(values)
            # Send email only if it's not the first stage after creating the task
            if not task.is_first_stage:
                task.send_email_on_stage_change(old_stage, new_stage_id)
            # Set the flag to False after the first stage
            task.is_first_stage = False

            return task

    def write(self, values):
        if 'stage_id' in values:
            values['old_stage_name'] = self.stage_id.name

        result = super(CustomProjectTask, self).write(values)

        if 'stage_id' in values:
            # Send email only if it's not the first stage after creating the task
            if not self.is_first_stage:
                self.send_email_on_stage_change(values['old_stage_name'], values['stage_id'])
            # Set the flag to False after the first stage
            self.is_first_stage = False

        return result

    def send_email_on_stage_change(self, old_stage, new_stage_id):
        try:
            new_stage = self.env['project.task.type'].browse(new_stage_id).name if new_stage_id else 'N/A'
            user_name = self.issue_creator_id.name if self.issue_creator_id else 'User'

            email_content = {
                'subject': f'Task {self.name} - Stage Changed - {new_stage}',
                'body_html': f'Dear {user_name},<br><br>'
                             f'The status of the task: {self.name} has been changed from <br><br> {old_stage} -> {new_stage} stage.<br><br>'
                             f'Thank You.',
                'email_to': self.issue_creator_id.email,
            }

            self.env['mail.mail'].create(email_content).send()

        except Exception as e:
            raise UserError(f"Error sending email: {str(e)}")
