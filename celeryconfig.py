from datetime import timedelta

beat_schedule = {
    'check-overdue-books-every-day': {
        'task': 'tasks.check_and_revoke_overdue_books',
        'schedule': timedelta(days=1),
    },
}
