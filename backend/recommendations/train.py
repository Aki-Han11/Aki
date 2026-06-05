"""
Train KNNBaseline model for book recommendations.
"""
import os
import pickle
import pandas as pd
from surprise import KNNBaseline, Dataset, Reader


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')


def train_model():
    from ratings.models import Rating

    ratings = Rating.objects.all()
    if ratings.count() < 5:
        return {'error': 'Not enough ratings to train model. Need at least 5 ratings.'}

    data = []
    for r in ratings:
        data.append({
            'user_id': r.user_id,
            'book_id': r.book_id,
            'rating': r.rating,
        })

    df = pd.DataFrame(data)
    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(df[['user_id', 'book_id', 'rating']], reader)
    trainset = dataset.build_full_trainset()

    sim_options = {
        'name': 'pearson_baseline',
        'user_based': True,
    }
    algo = KNNBaseline(sim_options=sim_options)
    algo.fit(trainset)

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(algo, f)

    return {
        'message': 'Model trained successfully',
        'ratings_used': len(data),
        'users': df['user_id'].nunique(),
        'books': df['book_id'].nunique(),
    }
