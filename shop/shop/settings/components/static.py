from warehouse.settings.components import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (
    BASE_DIR.joinpath("static"),
)
STATIC_ROOT = BASE_DIR.joinpath("static")
MEDIA_ROOT = BASE_DIR.joinpath("media")
