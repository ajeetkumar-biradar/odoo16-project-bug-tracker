from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, values):
        # Create the project
        project = super(ProjectTask, self).create(values)

        # Send email notification to the manager
        if project.manager_id:
            self.send_notification_email_to_manager(project.manager_id, project)

        return project

    def write(self, values):
        # Update the project
        result = super(ProjectTask, self).write(values)

        # Send email notification to the manager if manager_id is updated
        if 'manager_id' in values:
            self.send_notification_email_to_manager(self.manager_id, self)

        return result

    def send_notification_email_to_manager(self, manager, project):
        subject = "You have been assigned as a Project Manager for: {}".format(project.project_id.name)

        # Get a list of assignee names or display "Unassigned" if there are no assignees
        assignee_names = [assignee.name for assignee in project.assignee_ids] or ["Unassigned"]

        # Customize the email body with the list of assignee names and check for description
        if project.description:
            body = "Dear {},<br><br>The issue has been raised with the following team members: {}<br><br>Task Name: {}.<br><br> Description: {}.<br> Thank You.".format(
                manager.name, ", ".join(assignee_names), project.name, project.description)
        else:
            body = "Dear {},<br><br>The issue has been raised with the following team members: {}<br><br>Task Name: {}.<br><br> Thank You.".format(
                manager.name, ", ".join(assignee_names), project.name)

        # Send the email to the manager
        partner_ids = [manager.partner_id.id]
        project.message_post(body=body, subject=subject, partner_ids=partner_ids,
                             subtype_id=self.env.ref('mail.mt_comment').id)
