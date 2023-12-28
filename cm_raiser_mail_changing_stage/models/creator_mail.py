from odoo.exceptions import UserError
from odoo import models, fields, api


class CustomProjectTask(models.Model):
    _inherit = 'project.task'

    issue_raised_by_id = fields.Many2one('res.users', string='Issue Raised By')
    old_stage_name = fields.Char(string='Old Stage Name', store=True, readonly=True)
    has_stage_changed = fields.Boolean(string='Has Stage Changed', default=False, copy=False)

    @api.model
    def create(self, values):
        if 'stage_id' in values:
            new_stage_id = values.get('stage_id')
            old_stage = self.env['project.task.type'].browse(new_stage_id).name if new_stage_id else 'N/A'

            values['old_stage_name'] = old_stage
            task = super(CustomProjectTask, self).create(values)
            return task

    def write(self, values):
        if 'stage_id' in values:
            values['old_stage_name'] = self.stage_id.name
            values['has_stage_changed'] = True

        result = super(CustomProjectTask, self).write(values)

        if 'stage_id' in values and values['has_stage_changed']:
            # Send email only after the first stage change
            self.send_email_on_stage_change_raiser(values['old_stage_name'], values['stage_id'])

        return result

    def send_email_on_stage_change_raiser(self, old_stage, new_stage_id):
        try:
            new_stage = self.env['project.task.type'].browse(new_stage_id).name if new_stage_id else 'N/A'
            user_name = self.issue_raised_by_id.name if self.issue_raised_by_id else 'User'

            email_content = {
                'subject': f'Task {self.name} - Stage Changed - {new_stage}',
                'body_html': f'Dear {user_name},<br><br>'
                             f'The status of the task: {self.name} has been changed from <br><br> {old_stage} -> {new_stage} stage.<br><br>'
                             f'Thank You.',
                'email_to': self.issue_raised_by_id.email,
            }

            self.env['mail.mail'].create(email_content).send()

        except Exception as e:
            raise UserError(f"Error sending email: {str(e)}")
