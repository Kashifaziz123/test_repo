from odoo import models, fields, api
import json


class Lead(models.Model):
    _inherit = "crm.lead"

    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)

        if self.env.context.get("from_website_form"):
            form = self.env.context.get("form_values", {})
            for lead in leads:
                lead._send_contact_us_email(form)

        return leads

    def _get_crm_team_emails(self):
        team = self.team_id
        users = (team.member_ids | team.user_id)
        users = users.filtered(lambda u: u.email)
        return ','.join(users.mapped('email'))

    def _send_contact_us_email(self, form):
        recipients = self._get_crm_team_emails()

        subject = "New Customer Request from ANS Website"

        body = f"""
        <p>Hello Team,</p>

        <p>You have received a new customer inquiry through the website.</p>

        <p><strong>Customer Information:</strong></p>
        <ul>
            <li><strong>Name:</strong> {form.get('name')}</li>
            <li><strong>Email:</strong> {form.get('email_from')}</li>
            <li><strong>Phone:</strong> {form.get('phone')}</li>
            <li><strong>Company:</strong> {form.get('partner_name')}</li>
            <li><strong>Subject:</strong> {form.get('name')}</li>
        </ul>

        <p><strong>Inquiry Details:</strong></p>
        <p>{form.get('description')}</p>
        """

        mail = self.env['mail.mail'].create({
            'subject': subject,
            'body_html': body,
            'email_from': self.env.company.email,
            'email_to': recipients,
            'reply_to': form.get('email'),
            'auto_delete': False,
        })

        mail.send()
