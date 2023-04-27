from requests import get, post, delete, patch

# print(get('http://localhost:5000/api/news').json())
#
# print(get('http://localhost:5000/api/news/1').json())
#
# print(get('http://localhost:5000/api/news/999').json())
# # новости с id = 999 нет в базе
#
# print(get('http://localhost:5000/api/news/q').json())
#
# print(post('http://localhost:5000/api/news').json())
#
# print(post('http://localhost:5000/api/news',
#            json={'title': 'Заголовок'}).json())
#
# print(post('http://localhost:5000/api/news',
#            json={'title': 'Заголовок',
#                  'content': 'Текст новости',
#                  'user_id': 1,
#                  'is_private': False}).json())
# #
# print(delete('http://localhost:5000/api/news/999').json())
# # новости с id = 999 нет в базе
#
# print(delete('http://localhost:5000/api/news/1').json())

# print(get('http://localhost:5000/api/jobs').json())
# print(get('http://localhost:5000/api/jobs/1').json())
# print(get('http://localhost:5000/api/jobs/999').json())
# print(get('http://localhost:5000/api/jobs/q').json())

# print(post('http://localhost:5000/api/jobs').json())
# # No json data
#
# print(post('http://localhost:5000/api/jobs',
#            json={'team_leader': 1}).json())
# # Incorrect json data
# print(post('http://localhost:5000/api/jobs',
#            json={'team_leader': 1,
#                  'job': 'Main job',
#                  'work_size': 15,
#                  'is_finished': False,
#                  'collaborators': '2, 3',
#                  'id': 1}).json())
# #ID already exists
# print(post('http://localhost:5000/api/jobs',
#            json={'team_leader': 1,
#                  'job': 'Main job',
#                  'work_size': 15,
#                  'is_finished': False,
#                  'collaborators': '2, 3',
#                  'id': 998}).json())
# #Correct
# print(delete('http://localhost:5000/api/jobs/999').json())
# # новости с id = 999 нет в базе
#
# print(delete('http://localhost:5000/api/jobs/1').json())
#
# print(patch('http://localhost:5000/api/jobs/3').json())  # No JSON data
# print(patch('http://localhost:5000/api/jobs/3',  # Insufficient JSON Data
#             json={'team_leader': 2}
#             ).json())

print(get('http://localhost:5000/api/v2/user').json())
print(get('http://localhost:5000/api/v2/user/1').json())
print(get('http://localhost:5000/api/v2/user/98').json())
print(get('http://localhost:5000/api/v2/user/g').json())
print(delete('http://localhost:5000/api/v2/user/1').json())
print(delete('http://localhost:5000/api/v2/user/98').json())
print(delete('http://localhost:5000/api/v2/user/q').json())
print(get('http://localhost:5000/api/v2/user/98').json())
print(post('http://localhost:5000/api/v2/user', json={
    'name': 'Stas',
    'surname': 'Stupko',
    'age': 17,
    'position': 'middle',
    'speciality': 'cook',
    'address': 'idk',
    'email': 'stas@stas.stas'
}))
print(post('http://localhost:5000/api/v2/user', json={
    'name': 'Stas',
    'surname': 'Stupko',
    'age': 17
}))
print(post('http://localhost:5000/api/v2/user'))
