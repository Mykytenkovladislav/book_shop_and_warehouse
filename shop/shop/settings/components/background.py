from datetime import timedelta

CELERY_TASK_RESULT_EXPIRES = 3600

CELERY_BEAT_SCHEDULE = {
    "celery.backend_cleanup": {
        "task": "celery.backend_cleanup",
        "schedule": timedelta(seconds=300),
        "args": (),
    },
    "periodic": {
        "task": "geo_data.tasks.add",
        "schedule": timedelta(seconds=5),
        "args": (4, 5),
    },
}
