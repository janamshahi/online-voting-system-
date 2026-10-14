
from pathlib import Path

# ==================================================
# BASE CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "replace-this-development-key-before-deployment"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# ==================================================
# INSTALLED APPLICATIONS
# Jazzmin must be before django.contrib.admin
# ==================================================

INSTALLED_APPS = [
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "voting",
]


# ==================================================
# JAZZMIN SETTINGS
# ==================================================

JAZZMIN_SETTINGS = {
    "site_title": "Western Crystal Academy Admin",
    "site_header": "Western Crystal Academy",
    "site_brand": "WCA Voting System",
    "site_logo": None,
    "login_logo": None,
    "site_icon": None,

    "welcome_sign": "Welcome to the Voting Administration Panel",
    "copyright": "Western Crystal Academy",

    # Sidebar and navigation
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": True,
    "show_theme_switcher": False,
    "show_search": True,

    "search_model": [
        "auth.User",
        "voting.Election",
        "voting.Candidate",
        "voting.VoterProfile",
    ],

    # Custom static files
    "custom_css": "css/admin-white.css",
    "custom_js": None,

    # Icons for admin models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.group": "fas fa-users",

        "voting": "fas fa-vote-yea",
        "voting.election": "fas fa-calendar-check",
        "voting.candidate": "fas fa-user-tie",
        "voting.voterprofile": "fas fa-id-card",
        "voting.participation": "fas fa-check-circle",
        "voting.ballot": "fas fa-vote-yea",
    },

    # Sidebar order
    "order_with_respect_to": [
        "auth",
        "voting",
    ],

    # Custom Voting Results link
    # Requires the custom admin URL named "voting_results"
    "custom_links": {
        "voting": [
            {
                "name": "Voting Results",
                "url": "admin:voting_results",
                "icon": "fas fa-chart-bar",
            },
        ],
    },

    # Display settings
    "related_modal_active": True,
    "use_google_fonts_cdn": False,
    "changeform_format": "horizontal_tabs",

    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "collapsible",
    },

    # Top menu
    "topmenu_links": [
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"],
        },
        {
            "name": "Voting Website",
            "url": "/",
            "new_window": False,
        },
        {
            "name": "Voting Results",
            "url": "admin:voting_results",
            "new_window": False,
        },
    ],

    # Footer/user menu links
    "usermenu_links": [
        {
            "name": "Voting Website",
            "url": "/",
            "new_window": False,
        },
        {
            "name": "Voting Results",
            "url": "admin:voting_results",
            "new_window": False,
        },
    ],
}


# ==================================================
# JAZZMIN UI TWEAKS
# ==================================================

JAZZMIN_UI_TWEAKS = {
    "theme": "default",

    # White navigation bar
    "navbar": "navbar-white navbar-light",
    "brand_colour": "navbar-white",
    "accent": "accent-primary",

    # Light blue sidebar
    "sidebar": "sidebar-light-primary",

    # Layout
    "navbar_fixed": True,
    "sidebar_fixed": True,
    "footer_fixed": False,
    "body_small_text": False,
    "brand_small_text": False,

    # Sidebar navigation
    "sidebar_nav_small_text": False,
    "sidebar_nav_flat_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_child_indent": True,

    # Control panel
    "control_sidebar": False,
    "control_sidebar_color": "primary",
    "navbar_small_text": False,

    # Buttons
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "success": "btn-success",
        "warning": "btn-warning",
        "danger": "btn-danger",
    },

    # Forms and tables
    "actions_sticky_top": True,
    "related_modal_active": True,
    "select2_dropdown": True,
}


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==================================================
# URL CONFIGURATION
# ==================================================

ROOT_URLCONF = "online_voting_system.urls"


# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==================================================
# WSGI / ASGI
# ==================================================

WSGI_APPLICATION = "online_voting_system.wsgi.application"
ASGI_APPLICATION = "online_voting_system.asgi.application"


# ==================================================
# DATABASE
# ==================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ==================================================
# INTERNATIONALIZATION
# ==================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True
USE_TZ = True


# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# ==================================================
# MEDIA FILES
# Candidate photos
# ==================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==================================================
# DEFAULT PRIMARY KEY
# ==================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==================================================
# LOGIN / LOGOUT REDIRECTS
# ==================================================

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"
