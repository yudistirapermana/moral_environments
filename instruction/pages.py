from otree.api import *


class welcome(Page):
    pass


class instruction(Page):
    pass


class risk_task_example(Page):
    pass


class ambiguity_task_example(Page):
    pass


class company_task_example(Page):
    pass


class practice_session(Page):
    pass


page_sequence = [
    welcome,
    instruction,
    risk_task_example,
    ambiguity_task_example,
    company_task_example,
    practice_session,
]
