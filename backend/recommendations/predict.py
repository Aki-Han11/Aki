"""
Get top-N book recommendations for a user using trained KNNBaseline model.
"""
import os
import pickle
from books.models import Book

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')


def get_recommendations(user_id, n=12):
    """Return list of recommended book IDs for the given user."""
    if not os.path.exists(MODEL_PATH):
        return []

    with open(MODEL_PATH, 'rb') as f:
        algo = pickle.load(f)

    from ratings.models import Rating
    from django.db.models import Q

    # Get books the user has already rated
    rated_book_ids = set(
        Rating.objects.filter(user_id=user_id).values_list('book_id', flat=True)
    )

    # Get all books the user hasn't rated
    all_books = Book.objects.exclude(id__in=rated_book_ids)
    if not all_books.exists():
        return []

    # Predict ratings for unrated books
    predictions = []
    for book in all_books:
        try:
            pred = algo.predict(uid=user_id, iid=book.id)
            predictions.append((book.id, pred.est))
        except Exception:
            predictions.append((book.id, algo.default_prediction()))

    # Sort by predicted rating and return top N
    predictions.sort(key=lambda x: x[1], reverse=True)
    return [book_id for book_id, _ in predictions[:n]]
