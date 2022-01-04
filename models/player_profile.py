# -*- coding: utf-8 -*-

from odoo import fields, models,api

class PlayerProfile(models.Model):

    _name = "player.profile"
    _inherit = ['mail.thread']
    _description = 'Player Profile'

    # Player Information
    name = fields.Char('Name', required=True)
    active = fields.Boolean(default=True)
    image = fields.Binary(string='Image', widget='image')
    street = fields.Char(track_visibility='True')
    street2 = fields.Char(track_visibility='True')
    zip = fields.Char(change_default=True, track_visibility='True')
    city = fields.Char(track_visibility='True')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', track_visibility='True', required=True)
    email = fields.Char(track_visibility='True')
    phone = fields.Char(track_visibility='True')
    player_code = fields.Char(string="Player ID", compute="_get_player_code")
    classification = fields.Selection(
        [('entry', 'ENTRY'),
         ('bronze', 'BRONZE'),
         ('silver', 'SILVER'),
         ('gold', 'GOLD'),
         ], string='Classification',
        compute="_get_game_details",
        default='entry', store=True,
        help="""Every time you win you will increase your points to reach in a higher level.
           You will begin with the entry level, if you win 5 time you will reach Bronse level. If you win 7 time you will reach Silver level.
           And if you win 10 times will reach highest level Gold level .""")
    state = fields.Selection([('unregistered', 'Unregistered'),
                              ('Registered', 'Registered'),
                              ('idle', 'Idle'),
                              ('panned', 'Panned')],
                             default="unregistered",
                             readonly=True)
    # Game details
    game_ids = fields.Many2many("game.details", 'game_id', compute="_get_all_games")
    win_ids = fields.Many2many("game.details", 'win_id', compute="_get_all_games")
    loss_ids = fields.Many2many("game.details", 'loss_id', compute="_get_all_games")
    tie_ids = fields.Many2many("game.details", 'tie_id', compute="_get_all_games")

    games_number = fields.Integer(string="Number of Games", compute="_get_all_games", store=True)
    win_games_number = fields.Integer(string="Number of win Games", compute="_get_all_games", store=True)
    loss_games_number = fields.Integer(string="Number of loss Games", compute="_get_all_games", store=True)
    tie_games_number = fields.Integer(string="Number of tie Games", compute="_get_all_games", store=True)

    win_rate = fields.Float(string="Win Rate", compute="_get_game_details")
    game_duration = fields.Float(string="Average Game Duration", compute="_get_game_details")
    match_time = fields.Float(string="Match Times", compute="_get_game_details")
    wins = fields.Char(string="Wins", compute="_get_game_details")
    losses = fields.Char(string="Losses", compute="_get_game_details")
    tie = fields.Char(string="Tie", compute="_get_game_details")


    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "THE NAME MUST BE UNIQUE !"),
    ]

    def _get_player_code(self):
        for rec in self:
            rec.player_code = "#00" + str(rec.id)

    def _get_all_games(self):
        for rec in self:
            rec.win_ids = False
            rec.loss_ids = False
            rec.tie_ids = False
            rec.game_ids = False
            data = self.env['game.details'].search([])
            for i in data:
                if rec.id == i.player_1.id or rec.id == i.player_2.id:
                    rec.write({'game_ids': [(4, i.id)]})
                    if i.winner == 'tie':
                        rec.write({'tie_ids': [(4, i.id)]})
                    if i.winner == 'player1':
                        if i.player_1.id == rec.id :
                            rec.write({'win_ids': [(4, i.id)]})
                        if i.player_2.id == rec.id :
                            rec.write({'loss_ids': [(4, i.id)]})
                    if i.winner == 'player2':
                        if i.player_2.id == rec.id:
                            rec.write({'win_ids': [(4, i.id)]})
                        else:
                            rec.write({'loss_ids': [(4, i.id)]})
                rec.win_games_number = len(rec.win_ids)
                rec.loss_games_number = len(rec.loss_ids)
                rec.tie_games_number = len(rec.tie_ids)
                rec.games_number = len(rec.game_ids)

    def _get_game_details(self):
        for rec in self:
            rec.classification = 'entry'
            if rec.win_games_number >= 5 and rec.win_games_number < 7 :
                rec.classification = 'bronze'
            if rec.win_games_number >= 7 and rec.win_games_number < 10 :
                rec.classification = 'silver'
            if rec.win_games_number >= 10:
                rec.classification = 'gold'

            rec.wins = str(rec.win_games_number) + " Of " + str(rec.games_number)
            rec.losses = str(rec.loss_games_number) + " Of " + str(rec.games_number)
            rec.tie = str(rec.tie_games_number) + " Of " + str(rec.games_number)
            rec.match_time = sum(i.duration for i in rec.game_ids)
            if rec.games_number:
                rec.win_rate = (rec.win_games_number/rec.games_number)*100
                rec.game_duration = rec.match_time/rec.games_number

            else:
                rec.win_rate = 0
                rec.game_duration = 0


    def action_view_all_games(self):
        for rec in self:
            return {
                'name': "All Games",
                'type': 'ir.actions.act_window',
                'res_model': 'game.details',
                'view_mode': 'tree,form',
                'target': 'new',
                'domain': [('id', 'in', rec.game_ids.ids)],
            }

    def action_view_win_games(self):
        for rec in self:
            return {
                'name': "Win Games",
                'type': 'ir.actions.act_window',
                'res_model': 'game.details',
                'view_mode': 'tree,form',
                'target': 'new',
                'domain': [('id', 'in', rec.win_ids.ids)],
            }

    def action_view_loss_games(self):
        for rec in self:
            return {
                'name': "loss Games",
                'type': 'ir.actions.act_window',
                'res_model': 'game.details',
                'view_mode': 'tree,form',
                'target': 'new',
                'domain': [('id', 'in', rec.loss_ids.ids)],
            }

    def action_view_tie_games(self):
        for rec in self:
            return {
                'name': "Win Games",
                'type': 'ir.actions.act_window',
                'res_model': 'game.details',
                'view_mode': 'tree,form',
                'target': 'new',
                'domain': [('id', '=', rec.tie_ids.ids)],
            }
