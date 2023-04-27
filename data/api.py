import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs
from .news import News

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in news]
        }
    )


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(
                    only=('team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'user.name')) for item in
                    jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=["GET"])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=(
                'team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'user.name'))

        }
    )


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/jobs', methods=["POST"])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'collaborators', 'work_size', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Jobs).get({'id': request.json['id']}):
        return ({'error': 'Job ID already exists'})
    job = Jobs(team_leader=request.json['team_leader'],
               job=request.json['job'],
               collaborators=request.json['collaborators'],
               work_size=request.json['work_size'],
               is_finished=request.json['is_finished'],
               id=request.json['id'])
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=["DELETE"])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PATCH'])
def edit_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'collaborators', 'work_size', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Job does not exist'})
    job.team_leader = request.json['team_leader']
    job.job = request.json['job']
    job.collaborators = request.json['collaborators']
    job.work_size = request.json['work_size']
    job.is_finished = request.json['is_finished']
    db_sess.commit()
    return jsonify({'success': 'OK'})
