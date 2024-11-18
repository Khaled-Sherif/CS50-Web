def in_watchlist(user, list_id):
    if user.is_anonymous:
        return False
    else:
        in_watchlist = True if user.watchlist.filter(id=list_id) else False
        return in_watchlist
        