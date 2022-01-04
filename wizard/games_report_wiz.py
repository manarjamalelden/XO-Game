from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError


class GamesReportWiz(models.TransientModel):
    _name = 'games.report.wizard'

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    @api.constrains('date_from', 'date_to')
    def onchange_date_to(self):
        for each in self:
            if each.date_from and each.date_to :
                if each.date_from > each.date_to:
                    raise Warning('Date To must be greater than Date From')

    def print_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            },
        }

        return {'type': 'ir.actions.report',
                'report_name': 'xo_game.games_report',
                'report_type': "qweb-pdf",
                'data': data, }


    


