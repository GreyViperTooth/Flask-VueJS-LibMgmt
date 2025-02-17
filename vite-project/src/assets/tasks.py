from celery import shared_task
from models import Borrow, db
from datetime import datetime
from celery import Celery

# Define the Celery instance
celery = Celery('tasks', broker='redis://localhost:6379/0')

@shared_task
def test_task():
    return "Celery is working!"

@shared_task
def auto_return_books():
    """
    This task automatically returns overdue books. It finds all books that are overdue
    (past their due date) and updates their return date in the database.
    """
    overdue_borrows = Borrow.query.filter(Borrow.due_date < datetime.now().date(), Borrow.return_date.is_(None)).all()

    for borrow in overdue_borrows:
        borrow.return_date = datetime.now().date()
        db.session.add(borrow)

    db.session.commit()

    return f"Auto-returned {len(overdue_borrows)} books."
