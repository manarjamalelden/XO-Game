# -*- coding: utf-8 -*-

from odoo import fields, models, api

class GameDetails(models.Model):
    _name = "game.details"
    _inherit = ['mail.thread']
    _description = 'Game Details'

    name = fields.Char(string="Game ID", compute="_get_game_code")
    date = fields.Date(string="Date", required=True, default=fields.Date.today(), track_visibility='True')

    player_1 = fields.Many2one("player.profile", string="Player #1", required=True, track_visibility='True')
    player_2 = fields.Many2one("player.profile", string="Player #2", required=True, track_visibility='True')

    start_game = fields.Datetime(readonly=True, string="Start Game")
    end_game = fields.Datetime(readonly=True, string="End Game")
    duration = fields.Float("Duration", readonly=True, help="duration (in Seconds)")

    winner = fields.Selection([('player1', 'Player #1'),
                             ('player2', 'Player #2'),
                             ('tie', 'Tie')], string="winner", track_visibility='True')

    state = fields.Selection([('draft', 'Draft'),
                              ('in_progress', 'In Progress'),
                              ('finished', 'Finished'),
                              ], default="draft", track_visibility='True')

    def action_start_game(self):
        for rec in self:
            rec.state = 'in_progress'
            self.start_game = fields.Datetime.now()

    def action_end_game(self):
        for rec in self:
            rec.state = 'finished'
            self.end_game = fields.Datetime.now()
            delta = rec.end_game - rec.start_game
            seconds = delta.total_seconds()
            self.duration = seconds

    @api.onchange('player_1')
    def _player1_domain(self):
        return {
            'domain': {
                'player_2': [('id', '!=', self.player_1.id)],
            },
        }

    @api.onchange('player_2')
    def _player2_domain(self):
        return {
            'domain': {
                'player_1': [('id', '!=', self.player_2.id)],
            },
        }

    def _get_game_code(self):
        for rec in self:
            rec.name = "#Game00" + str(rec.id)
