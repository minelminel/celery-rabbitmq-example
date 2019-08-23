import math


def requests_per_minute(uptime, hits):
    '''
    ARGS::
        uptime => "0:13:32" <str> (hr:min:sec)
        hits   => 7 <int>
    # NOTE: uptime 'hours' never roll over for days!

    RETURNS::
        rate <int>
    # whatever the rate is calculated to be, we want to
    #    round the value UP to the nearest integer.
    '''
    if not hits:
        return 'unavailable'
    h, m, s = [int(n) for n in uptime.split(':')]
    as_minutes = (h*60) + (m) + (s/60)
    if as_minutes < 1:
        as_minutes = 1
    rpm = math.ceil(hits/as_minutes)
    return rpm
