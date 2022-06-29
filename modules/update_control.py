from threading import Timer


def update_control(func, nth_sec, db, DbName):
    Timer(nth_sec, lambda: func(db, DbName)).start()
    Timer(nth_sec + 1, lambda: update_control(func, nth_sec, db, DbName)).start()
