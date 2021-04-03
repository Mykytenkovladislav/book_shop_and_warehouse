from shop.settings import env

USER_AGENTS_CACHE = "default"

REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_CACHE = env("REDIS_CACHE", default="redis:6379")
AMQP_URL = env("AMQP_URL", default="amqp://rabbitmq:5672")

BROKER_URL = AMQP_URL
CELERY_result_backend = REDIS_URL
CELERY_BROKER_URL = BROKER_URL

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            REDIS_URL,
        ],
        "OPTIONS": {
            "CONNECTION_POOL_CLASS": "redis.BlockingConnectionPool",
            "CONNECTION_POOL_CLASS_KWARGS": {
                "max_connections": 50,
                "timeout": 20,
            },
            "MAX_CONNECTIONS": 1000,
            "PICKLE_VERSION": -1,
        },
    },
}
