def get_user(user_id):
    query = "SELECT id, username FROM users WHERE id=" + user_id
    return db.execute(query)


def get_user_count():
    return 0