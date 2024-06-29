from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def find_post_by_id(post_id, data):
    for post in data:
        if post['id'] == post_id:
            return post
    return None


def validate_post_data(data):
    if "title" not in data or "content" not in data:
        return False
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'GET':
        return jsonify(POSTS)

    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_post_data(new_post):
            return jsonify({"error": "Invalid post data"}), 400
        new_id = max(post['id'] for post in POSTS) + 1
        new_post['id'] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = find_post_by_id(post_id, POSTS)
    if post is not None:
        POSTS.remove(post)
        return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200
    else:
        return jsonify({"error": "Post not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
