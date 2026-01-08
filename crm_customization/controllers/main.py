from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.form import WebsiteForm

class WebsiteFormInherit(WebsiteForm):

    def insert_record(self, request, model, values, custom, meta=None):
        if model.model == "crm.lead":
            env = request.env(context=dict(
                request.env.context,
                from_website_form=True,
                form_values=values,
                mail_create_nosubscribe=True,
                mail_auto_subscribe_no_notify=True,
                mail_notify_force_send=False,
            ))
        else:
            env = request.env

        record = env[model.model].create(values)
        return record.id