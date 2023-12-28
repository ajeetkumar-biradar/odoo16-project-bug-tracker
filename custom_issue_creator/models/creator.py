from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', string='Department',
                                    default=lambda self: self._get_department_id(), readonly=True)

    date_deadline = fields.Date(string="Expected Date")

    tag_ids = fields.Many2many(string="issue type")

    @api.model
    def _get_department_id(self):
        user = self.env.user
        if user.department_id:
            return user.department_id.id
        return False

    def send_email_to_creator(self):
        for task in self:
            if task.issue_creator:
                subject = "Issue resolved: {}".format(task.name)
                body = "The Created Issue Has been resolved Check it out : {}\n\nDescription: {}".format(task.name,
                                                                                                         task.description)

                # Create a message to send as an email
                task.message_post(body=body, subject=subject, partner_ids=[task.issue_creator.partner_id.id])
