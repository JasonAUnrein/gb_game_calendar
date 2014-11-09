import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run
from time import sleep
from game_calendar import __version__
from .keys import GCAL_CLIENT_ID, GCAL_CLIENT_SECRET, GCAL_DEV_KEY


def update(obj, args):
    if not args:
        return

    for key, value in args.items():
        setattr(obj, key, value)


class Event(object):
    def __init__(self, service, event_list_data=None, event_data=None):
        self.service = service
        update(self, event_list_data)
        update(self, event_data)


class Calendar(object):
    events = set()

    def __init__(self, service, cal_list_data=None, cal_data=None):
        self.service = service
        update(self, cal_list_data)
        update(self, cal_data)

    def event_list(self, refresh=False):
        if self.events and not refresh:
            return self.events

        page_token = None
        while True:
            sleep(.2)
            events = self.service.events().list(calendarId=self.id,
                                                pageToken=page_token).execute()
            event_objs = [Event(self.service, event_list_data=x)
                          for x in events['items']]
            # print len(event_objs)
            # print set(event_objs)
            self.events = self.events.union(set(event_objs))
            page_token = events.get('nextPageToken')
            if not page_token:
                break

        return self.events

    def add_event(self, event_name, event_date, event_description):
        sleep(.2)
        event = {
            'summary': event_name,
            'start': {'date': event_date},
            'end': {'date': event_date},
            'description': event_description
        }
        created_event = self.service.events().insert(
            calendarId=self.id,
            body=event
        ).execute()
        created_event = Event(self.service, event_data=created_event)
        self.events.add(created_event)
        print created_event
        return created_event


class CalendarControl(object):
    flags = gflags.FLAGS
    name = 'GameCalendars'
    calendars = set()

    def __init__(self):
        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        # The client_id and client_secret can be found in Google Developers
        # Console
        self.flow = OAuth2WebServerFlow(
            client_id=GCAL_CLIENT_ID,
            client_secret=GCAL_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/calendar',
            user_agent='%s/%s' % (self.name, __version__))

        # To disable the local server feature, uncomment the following line:
        # FLAGS.auth_local_webserver = False

        # If the Credentials don't exist or are invalid, run through the
        # native client flow. The Storage object will ensure that if
        # successful the good Credentials will get written back to a file.
        self.storage = Storage('calendar.dat')
        self.credentials = self.storage.get()
        if self.credentials is None or self.credentials.invalid:
            self.credentials = run(self.flow, self.storage)

        # Create an httplib2.Http object to handle our HTTP requests and
        # authorize it with our good Credentials.
        self.http = httplib2.Http()
        self.http = self.credentials.authorize(self.http)

        # Build a service object for interacting with the API. Visit
        # the Google Developers Console
        # to get a developerKey for your own application.
        self.service = build(serviceName='calendar', version='v3',
                             http=self.http,
                             developerKey=GCAL_DEV_KEY)

    def list(self, refresh=False):
        if self.calendars and not refresh:
            return self.calendars

        sleep(.2)
        calendar_list = self.service.calendarList().list().execute()
        self.calendars.update([Calendar(self.service, x)
                               for x in calendar_list['items']])
        return self.calendars

    def add_calendar(self, name):
        sleep(.2)
        calendar = {
            'summary': name,
            'timeZone': 'America/Chicago'
        }

        calendars = self.service.calendars()
        created_calendar = calendars.insert(body=calendar).execute()
        created_calendar = Calendar(self.service, cal_data=created_calendar)
        self.calendars.add(created_calendar)
        return created_calendar
