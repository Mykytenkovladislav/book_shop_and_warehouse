# drf-yasg
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization"
        }
    },
    "DEFAULT_API_URL": None,
}

# drf
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "PAGINATE_BY": 10,
    "PAGINATE_BY_PARAM": "page_size",
    "MAX_PAGINATE_BY": 100,
}
