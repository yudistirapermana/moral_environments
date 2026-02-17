from os import environ

SESSION_CONFIGS = [
    # dict(
    #     display_name='Moral Environment',
    #     name='moral_environments',
    #     app_sequence=[
    #         'instruction',
    #         'risk_task',
    #         'ambiguity_task',
    #         'company_task',
    #         'moral_survey',
    #         'payment_page',
    #         'survey_demographic'
    #     ],
    #     num_demo_participants=1,
    # ),
    dict(
        display_name='Moral Environment',
        name='moral_environments',
        app_sequence=[
            'instruction',
            'risk_task',
            'ambiguity_task',
            'company_task',
            'moral_survey',
            'payment_page',
            'survey_player'
        ],
        num_demo_participants=1,
    ),
    # dict(
    #     display_name='Moral Environment',
    #     name='moral_environments',
    #     app_sequence=['ambiguity_task'],
    #     num_demo_participants=1,
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=20000.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'Rp'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
    Selamat datang di eksperimen kami
"""

SECRET_KEY = '4515626958046'
