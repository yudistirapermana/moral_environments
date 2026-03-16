from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'moral_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
