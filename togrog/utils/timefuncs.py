import datetime
import time
from gettext import gettext, ngettext


def timesince(d, now=None):
    """
    Takes two datetime objects and returns the time between d and now
    as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
    then "0 minutes" is returned.

    Units used are years, months, weeks, days, hours, and minutes.
    Seconds and microseconds are ignored.  Up to two adjacent units will be
    displayed.  For example, "2 weeks, 3 days" and "1 year, 3 months" are
    possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

    """
    chunks = (
      (60 * 60 * 24 * 365, lambda n: ngettext('year', 'years', n)),
      (60 * 60 * 24 * 30, lambda n: ngettext('month', 'months', n)),
      (60 * 60 * 24 * 7, lambda n : ngettext('week', 'weeks', n)),
      (60 * 60 * 24, lambda n : ngettext('day', 'days', n)),
      (60 * 60, lambda n: ngettext('hour', 'hours', n)),
      (60, lambda n: ngettext('minute', 'minutes', n))
    )
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    if now and not isinstance(now, datetime.datetime):
        now = datetime.datetime(now.year, now.month, now.day)

    if not now:
        now = datetime.datetime.utcnow()

    # ignore microsecond part of 'd' since we removed it from 'now'
    delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since <= 0:
        # d is in the future compared to now, stop processing.
        return u'0 ' + gettext('minutes')
    for i, (seconds, name) in enumerate(chunks):
        count = since // seconds
        if count != 0:
            break
    s = gettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
    if i + 1 < len(chunks):
        # Now get the second item
        seconds2, name2 = chunks[i + 1]
        count2 = (since - (seconds * count)) // seconds2
        if count2 != 0:
            s += gettext(', %(number)d %(type)s') % {'number': count2, 'type': name2(count2)}
    return s

def timeuntil(d, now=None):
    """
    Like timesince, but returns a string measuring the time until
    the given time.
    """
    if not now:
        now = datetime.datetime.utcnow()
    return timesince(now, d)
