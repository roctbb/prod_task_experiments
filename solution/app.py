from helpers import *
from manage import *
from methods.countries import *
from methods.auth import *
from methods.friends import *
from methods.posts import *


@app.route('/api/ping', methods=['GET'])
def send():
    return jsonify({"status": "ok"}), 200


@app.route('/api/countries', methods=['GET'])
@creates_response
@validate()
def get_countries(query: CountriesRequest):
    return jsonify(as_dict(fetch_countries(query.region))), 200


@app.route('/api/countries/<alpha2>', methods=['GET'])
@creates_response
@validate()
def get_country(alpha2: str):
    return jsonify(find_country(alpha2).as_dict()), 200


@app.route('/api/auth/register', methods=['POST'])
@creates_response
@validate()
def register_user(body: RegisterUserRequest):
    user = create_user(body)
    return jsonify({"profile": user.as_dict()}), 201


@app.route('/api/auth/sign-in', methods=['POST'])
@creates_response
@validate()
def sign_in(body: LoginRequest):
    token = authorize_user(body.login, body.password)
    return jsonify(token.as_dict()), 201


@app.route('/api/me/profile')
@creates_response
@requires_auth
def get_profile(user):
    return jsonify(user.as_dict()), 200


@app.route('/api/me/profile', methods=['PATCH'])
@creates_response
@requires_auth
@validate()
def patch_profile(user, body: PatchUserRequest):
    return jsonify(patch_user(user, body).as_dict()), 200


@app.route('/api/me/updatePassword', methods=['POST'])
@creates_response
@requires_auth
@validate()
def change_password(user, body: ChangePasswordRequest):
    change_user_password(user, body.oldPassword, body.newPassword)
    return jsonify({"status": 'ok'}), 200


@app.route('/api/profiles/<login>')
@creates_response
@requires_auth
def search_profile(user, login):
    return jsonify(find_public_profile(login).as_dict()), 200


@app.route('/api/friends/add', methods=['POST'])
@creates_response
@requires_auth
@validate()
def add_friend(user, body: FriendRequest):
    friend = find_profile(body.login)
    add_to_friends(user, friend)
    return jsonify({"status": 'ok'}), 200


@app.route('/api/friends/remove', methods=['POST'])
@creates_response
@requires_auth
@validate()
def remove_friend(user, body: FriendRequest):
    try:
        friend = find_profile(body.login)
        remove_from_friends(user, friend)
    except:
        pass
    return jsonify({"status": 'ok'}), 200


@app.route('/api/friends', methods=['GET'])
@creates_response
@requires_auth
@validate()
def get_friends(user, query: PaginationRequest):
    return jsonify(as_dict(get_user_friends(user, query))), 200


@app.route('/api/posts/new', methods=['POST'])
@creates_response
@requires_auth
@validate()
def add_post(user, body: AddPostRequest):
    return jsonify(add_post_from_user(user, body).as_dict()), 200


@app.route('/api/posts/<post_id>', methods=['GET'])
@creates_response
@requires_auth
@validate()
def get_post(user, post_id):
    post = find_post_by_id(post_id)

    if not has_access_to_feed(user, post.author):
        return NotFound

    return jsonify(post.as_dict()), 200


@app.route('/api/posts/feed/my', methods=['GET'])
@creates_response
@requires_auth
@validate()
def get_self_posts(user, query: PaginationRequest):
    return jsonify(as_dict(get_posts_for_user(user, query))), 200


@app.route('/api/posts/feed/<login>', methods=['GET'])
@creates_response
@requires_auth
@validate()
def get_other_user_posts(user, login, query: PaginationRequest):
    author = find_profile(login)

    if has_access_to_feed(user, author):
        return jsonify(as_dict(get_posts_for_user(author, query))), 200

    raise NotFound


@app.route('/api/posts/<post_id>/like', methods=['POST'])
@creates_response
@requires_auth
@validate()
def like_post(user, post_id):
    post = find_post_by_id(post_id)

    if has_access_to_feed(user, post.author):
        set_reaction(post, user, "like")
        return jsonify(find_post_by_id(post_id).as_dict()), 200

    raise NotFound


@app.route('/api/posts/<post_id>/dislike', methods=['POST'])
@creates_response
@requires_auth
@validate()
def dislike_post(user, post_id):
    post = find_post_by_id(post_id)

    if has_access_to_feed(user, post.author):
        set_reaction(post, user, "dislike")
        return jsonify(find_post_by_id(post_id).as_dict()), 200

    raise NotFound


if __name__ == "__main__":
    app.run(port=SERVER_PORT, debug=APP_DEBUG)
