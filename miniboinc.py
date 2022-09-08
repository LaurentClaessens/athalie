

import time
from utilities import human_timestamp


def rest(h, m, pc):
    done_mins = h*60 + m
    tot_mins = (done_mins * 100) / pc
    remain_mins = tot_mins - done_mins
    remain_hours = remain_mins / 60

    i_hours = int(remain_hours)
    i_mins = int((remain_hours - i_hours) * 60)
    str_remain = f"{i_hours}h {i_mins}m".ljust(7)
    end_ts = time.time() + remain_mins * 60

    print(f"{str_remain} -> {human_timestamp(end_ts)}")
