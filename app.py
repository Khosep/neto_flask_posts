from flask import Flask, jsonify
from views import PostView, UserView
from errors import ApiException

app = Flask('app')


@app.errorhandler(ApiException)
def error_handler(error: ApiException):
    response = jsonify({
        'status': 'error',
        'message': error.message
    })
    response.status_code = error.status_code
    return response


@app.route('/')
@app.route('/index')
def index():
    return jsonify({'check': 'Ok'})


app.add_url_rule('/posts/', view_func=PostView.as_view('posts'), methods=['GET', 'POST'])
app.add_url_rule('/posts/<int:post_id>', view_func=PostView.as_view('post_detail'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST', ])
app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('user_detail'), methods=['GET', ])

app.run()
