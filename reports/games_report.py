
from odoo import api, fields, models, _


class GamesReport(models.AbstractModel):
    _name = 'report.xo_game.games_report'

    @api.model
    def _get_report_values(self, docids,data=None):
        form = data['form']
        date_from = form.get('date_from')
        date_to = form.get('date_to')
        all_games = self.get_games(date_from, date_to)
 
        return {
            'doc_ids': self.ids,
            'doc_model': 'games.report.wizard',
            'date_from': date_from,
            'date_to': date_to,
            'all_games': all_games,
            'data': data['form'],
            }
   
    def get_games(self, date_from, date_to):
        search_list = []
        if date_from:
            search_list.append(('create_date', '>=', date_from), )
        if date_to:
            search_list.append(('create_date', '<', date_to), )
        games = self.env['game.details'].search(search_list)
        return games