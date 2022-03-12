from app import client
from app.models import Movie
from datetime import datetime


def test_get():
    res = client.get('/api')

    assert res.status_code == 200

    assert len(res.get_json()) == len(Movie.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'body': "post.body",
        'timestamp': datetime(2022, 2, 18, 11, 2, 3, 000000),
        'user_id': 1
    }

    res = client.post('/api', json=data)

    assert res.status_code == 200


# def test_put():

#     res = client.put('/api/2', json={'body': "UPD"})

#     assert res.status_code == 200
#     assert Post.query.get(2).body == "UPD"


# def test_update():
#     res = client.delete('/api/2')

#     assert res.status_code == 204

#     assert Post.query.get(2) is None



# def test_simple():
#     mylist = [1, 2, 3, 4, 5]

#     assert 1 in mylist


# def test_get():
#     res = client.get('/tutorials')

#     assert res.status_code == 200

#     assert len(res.get_json()) == len(Video.query.all())
#     assert res.get_json()[0]['id'] == 1


# def test_post():
#     data = {
#         'name': 'Unit Tests',
#         'description': 'Pytest tutorial'
#     }

#     res = client.post('/tutorials', json=data)

#     assert res.status_code == 200

#     assert res.get_json()['name'] == data['name']


# def test_put():
#     res = client.put('/tutorials/1', json={'name': 'UPD'})

#     assert res.status_code == 200
#     assert Video.query.get(1).name == 'UPD'


# def test_delete():
#     res = client.delete('/tutorials/1')

#     assert res.status_code == 204
#     assert Video.query.get(1) is None