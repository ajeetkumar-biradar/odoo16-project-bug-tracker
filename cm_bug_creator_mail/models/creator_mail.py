from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, values):
        project = super(ProjectTask, self).create(values)

        # Send email notifications to the manager and issue_creator
        if project.issue_raised_by_id:
            self.send_notification_email_to_issue_raiser(project.issue_raised_by_id, project)

        return project

    def write(self, values):
        result = super(ProjectTask, self).write(values)

        # Send email notifications to the manager and issue_creator if manager_id or issue_creator is updated
        if 'issue_raised_by_id' in values:
            self.send_notification_email_to_issue_raiser(self.issue_raised_by_id, self)

        return result

    def send_notification_email_to_issue_raiser(self, issue_raised_by_id, project):
        # Check if issue_raised_by_id is present and has an email address
        if issue_raised_by_id and issue_raised_by_id.email:
            subject = "Your issue has been created: {}".format(project.name)

            # Include the description if it exists
            if project.description:
                body = f"Dear {issue_raised_by_id.name},<br><br>Your request has been recorded and assigned to the concerned person. We will update you soon.<br><br>Task Name: {project.name}.<br><br>Description: {project.description}.<br>Thank You."
            else:
                body = f"Dear {issue_raised_by_id.name},<br><br>This task has been assigned to the concerned/appropriate assignee.<br><br>Task Name: {project.name}.<br>Thank You."

            # Send the email to the issue_creator
            partner_ids = [issue_raised_by_id.partner_id.id]
            project.message_post(body=body, subject=subject, partner_ids=partner_ids,
                                 subtype_id=self.env.ref('mail.mt_comment').id)
