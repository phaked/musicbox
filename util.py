import mpd

def exec_mpc_func(mpc, func, *args):
    try:
        mpc.ping()
    except mpd.ConnectionError:
        mpc.connect("localhost", 6600)
    return func(*args)
