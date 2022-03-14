from app import client
from app.models import Movie
from datetime import datetime
from flask_login import current_user

# def test_get():
#     res = client.get('/api')

#     assert res.status_code == 302

#     assert len(res.get_json()) == len(Movie.query.all())
#     assert res.get_json()[0]['id'] == 1


# def test_post():
#     data = {
#         'title': "title",
#         'genres_id': 1,
#         'release_date': datetime(2022, 2, 18, 11, 2, 3, 000000),
#         'producer_id': 1,
#         'body': "body",
#         'poster': "",
#         'user_id': current_user.id,
#         'publication': datetime(2022, 2, 18, 11, 2, 3, 000000),
#     }

#     res = client.post('/api', json=data)

#     assert res.status_code == 200

#     assert res.get_json()['name'] == data['name']


def test_put():
    res = client.put('/api/2', json={'title': 'second'})

    assert res.status_code == 200
    # assert Movie.query.get(1).name == 'UPD'


# def test_delete():
#     res = client.delete('/api/2')

#     assert res.status_code == 204
#     assert Movie.query.get(1) is None