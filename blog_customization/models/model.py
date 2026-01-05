from odoo import models, fields

class BlogPost(models.Model):
    _inherit = "blog.post"

    card_image = fields.Binary()

    def _get_background(self, height=None, width=None):
        self.ensure_one()

        # if custom card image exists → use it
        if self.card_image:
            url = f"/web/image/blog.post/{self.id}/card_image"
            params = []
            if height:
                params.append(f"height={height}")
            if width:
                params.append(f"width={width}")
            if params:
                url += "?" + "&".join(params)
            return f"url({url})"

        # fallback to standard behavior
        return super()._get_background(height=height, width=width)