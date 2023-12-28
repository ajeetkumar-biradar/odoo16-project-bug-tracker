from odoo import models, fields, api

PRIORITIES = [
    ('0', 'Very Low'),
    ('1', 'Low'),
    ('2', 'Normal'),
    ('3', 'High'),
    ('4', 'Very High'),
]


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # priority = fields.Selection([
    #     ('low', 'Low'),
    #     ('medium', 'Medium'),
    #     ('high', 'High'),
    # ], string='Priority', default='medium')

    issue_raised_by_id = fields.Many2one('res.users', string='Issue Raised By')

    issue_raiser_department_id = fields.Many2one('hr.department', string='Issue Raiser Department')

    application = fields.Selection([
        ('mobile_application', 'Mobile Application'),
        ('web_application', 'Web Application'),
    ], string='Application')

    priority = fields.Selection(PRIORITIES, default='1', help='Priority of the'
                                                              ' Ticket')

    criticality = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Criticality', default='medium')

    issue_creator = fields.Many2one(
        'res.users',  # Reference to the 'res.users' model
        string='Issue Creator',
        default=lambda self: self.env.user.id,  # Set the default value to the current user
        readonly=True,  # Make the field readonly
    )

    @api.onchange('issue_raised_by_id')
    def _onchange_issue_raised_by_id(self):
        if self.issue_raised_by_id:
            self.issue_raiser_department_id = self.issue_raised_by_id.department_id.id
        else:
            self.issue_raiser_department_id = False
