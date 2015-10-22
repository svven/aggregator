"""
Utility functions such as:
- unicode  <-> utf-8;
- datetime <-> unixtime;
- unzip zipped list;
"""
import calendar
from datetime import datetime, timedelta
from itertools import chain

def munixtime(dt):
    "Convert datetime to unixtime."
    return calendar.timegm(dt.utctimetuple())

def mdatetime(ut):
    "Convert unixtime to datetime."
    return datetime.utcfromtimestamp(ut)

def timeago(**kvargs):
    "Time ago by time delta."
    return datetime.utcnow() - timedelta(**kvargs)


def encode(u):
    "If unicode, encode utf-8."
    try:
        if u is None:
            return u'' # avoid 'None'
        if isinstance(u, unicode):
            return u.encode('utf-8')
    except Exception, e:
        # pass
        print e
    return u

def decode(s):
    "If string, decode to utf-8."
    try:
        if s == '':
            return None
        if isinstance(s, basestring):
            return s.decode('utf-8')
    except Exception, e:
        # pass
        print e
    return s


def unzip(zl):
    "[(1,2),(3,4)] -> [1,2,3,4]"
    # return [i for s in zl for i in s]
    return list(chain.from_iterable(zl))
