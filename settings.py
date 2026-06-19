from os import environ

DEBUG = environ.get('OTREE_PRODUCTION') != '1'

SESSION_CONFIGS = [
    # --- Full experiment (1 link, treatment diacak otomatis seimbang) ---
    dict(
        display_name='Moral Environment - Random Assignment (GUNAKAN INI)',
        name='moral_env',
        app_sequence=[
            'instruction',
            'practice',
            'risk_task',
            'ambiguity_task',
            'company_task',
            'moral_survey',
            'survey_player',
            'payment_page'
        ],
        num_demo_participants=4,
        # Tidak ada 'treatment' key → oTree acak otomatis di creating_session
    ),
    # --- Sesi terpisah (opsional, jika perlu kontrol manual) ---
    dict(
        display_name='Moral Environment - By Return (manual)',
        name='moral_env_by_return',
        app_sequence=[
            'instruction',
            'practice',
            'risk_task',
            'ambiguity_task',
            'company_task',
            'moral_survey',
            'survey_player',
            'payment_page'
        ],
        num_demo_participants=1,
        treatment='by_return',
    ),
    dict(
        display_name='Moral Environment - By Capitalisation',
        name='moral_env_by_capitalisation',
        app_sequence=[
            'instruction',
            'practice',
            'risk_task',
            'ambiguity_task',
            'company_task',
            'moral_survey',
            'survey_player',
            'payment_page'
        ],
        num_demo_participants=1,
        treatment='by_capitalisation',
    ),
    # --- Testing sessions (individual apps) ---
    dict(
        display_name='[TEST] Risk Task',
        name='test_risk_task',
        app_sequence=['risk_task'],
        num_demo_participants=2,
        treatment='by_return',
    ),
    dict(
        display_name='[TEST] Ambiguity Task',
        name='test_ambiguity_task',
        app_sequence=['ambiguity_task'],
        num_demo_participants=2,
        treatment='by_return',
    ),
    dict(
        display_name='[TEST] Company Task - By Return',
        name='test_company_task_return',
        app_sequence=['company_task'],
        num_demo_participants=2,
        treatment='by_return',
    ),
    dict(
        display_name='[TEST] Company Task - By Capitalisation',
        name='test_company_task_cap',
        app_sequence=['company_task'],
        num_demo_participants=2,
        treatment='by_capitalisation',
    ),
    dict(
        display_name='[TEST] Moral Survey',
        name='test_moral_survey',
        app_sequence=['moral_survey'],
        num_demo_participants=2,
        treatment='by_return',
    ),
    dict(
        display_name='[TEST] Survey Player',
        name='test_survey_player',
        app_sequence=['survey_player'],
        num_demo_participants=2,
        treatment='by_return',
    ),
    dict(
        display_name='[TEST] Payment Page - Combined',
        name='test_payment_page',
        app_sequence=['risk_task', 'ambiguity_task', 'company_task', 'payment_page'],
        num_demo_participants=2,
    ),
    dict(
        display_name='[TEST] Full Flow - Combined (2 players)',
        name='test_full_combined',
        app_sequence=[
            'instruction',
            'practice',
            'risk_task',
            'ambiguity_task',
            'company_task',
            'moral_survey',
            'survey_player',
            'payment_page'
        ],
        num_demo_participants=2,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
    Selamat datang di eksperimen kami
"""

SECRET_KEY = '4515626958046'

ROOMS = [
    dict(
        name='eksperimen_moral',
        display_name='Eksperimen Moral Environment',
        participant_label_file='_rooms/eksperimen.txt',
    ),
]
