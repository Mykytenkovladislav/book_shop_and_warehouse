from warehouse.settings import env

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"
