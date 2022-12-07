from flask.views import MethodView
from db import User, Post, Session
from flask import jsonify, request
from errors import ApiException
from sqlalchemy.exc import IntegrityError
from validate import validate, UserCreateValidate, PostCreateValidate
from auth import hash_password, total_check_authentication


class PostView(MethodView):
    def get(self, post_id=None):
        if post_id:
            with Session() as session:
                post = session.query(Post).get(post_id)
                if post is None:
                    raise ApiException(404, 'post not found')
                return jsonify({'id': post.id,
                                'title': post.title,
                                'content': post.content,
                                'created': post.created,
                                'user_id': post.user_id
                                })
        else:
            with Session() as session:
                posts_query = session.query(Post).all()
                posts = []
                for p in posts_query:
                    post = {'id': p.id,
                            'title': p.title,
                            'content': p.content,
                            'created': p.created,
                            'user_id': p.user_id}
                    posts.append(post)
                return jsonify(posts)

    def post(self):
        post_data = validate(request.json, PostCreateValidate)
        auth_from_headers = request.headers.get('Authorization')
        if auth_from_headers:
            user_id = total_check_authentication(auth_from_headers)
            with Session() as session:
                if post_data.get('user_id') != user_id:
                    raise ApiException(403, f'you are not allowed to set non-your user_id')
                new_post = Post(**post_data)
                session.add(new_post)
                session.commit()
                return jsonify({'id': new_post.id,
                                'title': new_post.title,
                                'content': new_post.content,
                                'created': new_post.created,
                                'user_id': new_post.user_id})
        else:
            raise ApiException(401, 'authentication data has not been received')

    def patch(self, post_id: int):
        post_data = request.json
        auth_from_headers = request.headers.get('Authorization')
        if auth_from_headers:
            user_id = total_check_authentication(auth_from_headers)
            with Session() as session:
                post = session.query(Post).get(post_id)
                if post is None:
                    raise ApiException(404, 'post not found')
                elif user_id == post.user_id:
                    for field, value in post_data.items():
                        if field == 'user_id' and value != user_id:
                            raise ApiException(403, f'you are not allowed to change the user_id')
                        setattr(post, field, value)
                    session.add(post)
                    session.commit()
                    return jsonify({'id': post.id,
                                    'title': post.title,
                                    'content': post.content,
                                    'created': post.created,
                                    'user_id': post.user_id
                                    })
                else:
                    raise ApiException(403, 'you do not have access rights to change this post')
        else:
            raise ApiException(401, 'authentication data has not been received')

    def delete(self, post_id: int):
        auth_from_headers = request.headers.get('Authorization')
        if auth_from_headers:
            user_id = total_check_authentication(auth_from_headers)
            with Session() as session:
                post = session.query(Post).get(post_id)
                if post is None:
                    raise ApiException(404, 'post not found')
                elif user_id == post.user_id:
                    session.delete(post)
                    session.commit()
                    return jsonify({'status': 'post deleted'})
                else:
                    raise ApiException(403, 'you do not have access rights to delete this post')
        else:
            raise ApiException(401, 'authentication data has not been received')


class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            user = session.query(User).get(user_id)
            if user is None:
                raise ApiException(404, 'user not found')
            return jsonify({'id': user.id,
                            'username': user.username,
                            })

    def post(self):
        user_data = validate(request.json, UserCreateValidate)
        user_data['password'] = hash_password(user_data['password'])
        with Session() as session:
            new_user = User(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, 'field is not unique')
            return jsonify({'id': new_user.id,
                            'username': new_user.username,
                            'email': new_user.email
                            })
