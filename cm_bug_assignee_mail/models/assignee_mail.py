from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, values):
        # Create the project

        project = super(ProjectTask, self).create(values)

        # Send email notification to assignees
        if project.assignee_ids:
            self.send_notification_email_to_assignee(project.assignee_ids, project)

        return project

    def write(self, values):
        # Update the project
        result = super(ProjectTask, self).write(values)

        # Send email notification to assignees if assignee_ids is updated
        if 'assignee_ids' in values:
            self.send_notification_email_to_assignee(self.assignee_ids, self)

        return result

    def send_notification_email_to_assignee(self, assignees, project):
        subject = "You have been assigned to a project: {}".format(project.name)

        # Get a comma-separated list of assignee names
        assignee_names = ", ".join(assignee.name for assignee in assignees)

        # Include the description if it exists
        if project.description:
            body = "Dear {},<br><br>You have been assigned to the Task!<br><br>Task Name: {}<br><br>Description: {}<br>Thank You.".format(
                assignee_names, project.name, project.description)
        else:
            body = "Dear {},<br><br>You have been assigned to the Task!<br><br>Task Name: {}<br><br>Thank You.".format(
                assignee_names, project.name)

        # Send the email to the assignees
        partner_ids = [assignee.partner_id.id for assignee in assignees]
        project.message_post(body=body, subject=subject, partner_ids=partner_ids,
                             subtype_id=self.env.ref('mail.mt_comment').id)

    # def send_notification_email_to_assignee(self, assignees, project):
    #     # Customize the email content as needed
    #     subject = "Project Issue Report: %s" % project.name
    #     body = "Dear {},<br>You have been assigned to the Task!<br>Task Name: {}<br>Expected Date: {}<br>Description: {}<br>Thank You.".format(
    #         project.assignee_ids.name, project.name, project.date_deadline, project.description)
    #
    #     # Send the email to each assignee
    #     partner_ids = [assignee.partner_id.id for assignee in assignees]
    #     project.message_post(body=body, subject=subject, partner_ids=partner_ids,
    #                          subtype_id=self.env.ref('mail.mt_comment').id)
