__author__ = 'Jason Unrein'
__copyright__ = 'Copyright 2014'
__credits__ = ['Jason Unrein']
__license__ = 'GPL'
__version__ = '0.0.1'  # project version
__maintainer__ = 'Jason Unrein'
__email__ = 'JasonAUnrein@gmail.com'
__status__ = 'Development'

from datetime import date
from time import sleep
from giantbomb import giantbomb
from .keys import GIANT_BOMB_KEY
from .gcal import CalendarControl


def get_games():
    offset = 0
    games = 1
    cur_year = date.today().year
    game_list = []
    for year in (cur_year, cur_year + 1, cur_year + 2):
        while games:
            games = GB.getGames(filter={'expected_release_year': year},
                                offset=offset)
            if not games:
                continue

            offset += len(games)
            game_list.extend(games)

    return game_list


def get_uniq_platforms(games):
    uniq_platforms = set()
    for game in games:
        if game.platforms is None:
            continue
        uniq_platforms = uniq_platforms.union(set([x.name
                                                   for x in game.platforms]))
    return uniq_platforms


if __name__ == "__main__":
    cal_str = "GiantBomb - %s games"

    # Connect to gcal
    print "Connecting to Google Calendar API"
    calendar = CalendarControl()

    # Connect to Giant Bomb
    print "Connecting to Giant Bomb API"
    GB = giantbomb.Api(GIANT_BOMB_KEY)

    # Get all games being released this year and the next two years
    print "Geting all the games"
    upcoming_games = get_games()

    # Verify/Create and calendars needed
    platforms = get_uniq_platforms(upcoming_games)

    print "Getting google calendars"
    calendars = calendar.list()

    print "Verifying Calendars are present"
    plat_cal_lkup = {}
    for platform in platforms:
        str = cal_str % platform
        for calendar_list_entry in calendars:
            if str == calendar_list_entry.summary.encode('utf8'):
                entry = calendar_list_entry
                break
        else:
            print " - Needed calendar %s" % str
            entry = calendar.add_calendar(str.encode("utf8"))
        plat_cal_lkup[platform] = entry
        entry.event_list(refresh=True)

    print "Going through games/calendars and adding events as appropriate"
    for game in upcoming_games:
        if game.expected_release_day is None or \
           game.expected_release_month is None or \
           game.expected_release_year is None:
            continue
        present = False
        for game_plat in game.platforms:
            cal = plat_cal_lkup[game_plat.name]
            for event in cal.events:
                if game.name.encode('utf8') == event.summary.encode('utf8'):
                    present = True
                    break
            if present:
                break
            else:
                print(" - Adding calendar event for %s on %04d-%02d-%02d" %
                      (game.name.encode('utf8'), game.expected_release_year,
                       game.expected_release_month,
                       game.expected_release_day))
                cal.add_event(game.name,
                              "%04d-%02d-%02d" % (game.expected_release_year,
                                                  game.expected_release_month,
                                                  game.expected_release_day),
                              game.description)
                sleep(5)
