def strfdelta(tdelta):
    h, rem = divmod(tdelta.seconds, 3600)
    m, s = divmod(rem, 60)
    match h,m,s:
        case h,_,_ if h != 0:
            return f"{h}:{m:0>2}:{s:0>2}"
        case _:
            return f"{m:0>2}:{s:0>2}"