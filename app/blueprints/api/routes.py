from . import api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.blueprints.blog.models import Post
from app.blueprints.auth.models import User


@api.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token, 'expiration': user.token_expiration})


# Create a user
@api.route('/users/create', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    username = data['username']
    email = data['email']
    password = data['password']
    new_user = User(username=username, email=email, password=password)
    return jsonify(new_user.to_dict()), 201


# Get all posts
@api.route('/posts')
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


# Get a single post by id
@api.route('/posts/<int:post_id>')
def get_single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


# Create a post
@api.route('/posts/create', methods=['POST'])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get data from request body
    data = request.json
    # Check to make sure all required fields are present
    for field in ['title', 'body']:
        if field not in data:
            # if not return a 400 response with error
            return jsonify({'error': f'{field} must be in request body'}), 400
    # Get fields from data dict
    title = data['title']
    body = data['body']
    user_id = token_auth.current_user().id
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201


# Edit a post by post id
@api.route('/edit-posts/<int:post_id>', methods=['PUT'])
@token_auth.login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = token_auth.current_user()
    if post.author != current_user:
        return jsonify({'error': 'You do not have authorization to edit this post'}), 403
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data = request.json
    for key in data.keys():
        if key not in {'title', 'body'}:
            return jsonify({'error': f'{key} is not an acceptable property'}), 400
    post.update(**data)
    return jsonify(post.to_dict())


# Delete a post by post id
@api.route('/delete-posts/<int:post_id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = token_auth.current_user()
    if post.author != current_user:
        return jsonify({'error': 'You do not have authorization to delete this post'}), 403
    post.delete()
    return jsonify({}), 204
