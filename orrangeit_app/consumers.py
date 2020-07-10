from channels.generic.websocket import JsonWebsocketConsumer
from orrangeit_app.models import EventInfo, User
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from collections import defaultdict
from pyrogram import Client

notificated = defaultdict(list)


class TelegramGroupCreator:
    '''
    Class for telegram groups creator
    '''
    def __init__(self):
        self.app = Client(
            session_name="orrangeit",
            api_hash="90ef17db54b69f68e11de941198099ee",
            api_id=1342638,
            proxy=dict(
                hostname="185.166.216.20",
                port=45786,
                username="Selpiter2074",
                password="Q7y4AfJ"
            )
        )
        try:
            self.app.start()
            self.run = True
        except:
            self.run = False


group_creator = TelegramGroupCreator()


class TelegramConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        self.event_name = self.scope['url_route']['kwargs']['group_name']
        self.event_name = self.event_name.replace('_', ' ')
        if group_creator.run:
            self.group_id = group_creator.app.create_supergroup(self.event_name, "Group of {}. Find friends, "
                                                                                 "ask questions and have fun!".format(
                self.event_name)).id
            self.group_link = group_creator.app.export_chat_invite_link(self.group_id)
            self.send_json({
                "telegram_group_link": self.group_link
            })
            print(self.group_link)
        else:
            self.disconnect('Telegram chat creator can not be run')


class NotificationsConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = BackgroundScheduler()

    def connect(self):
        self.accept()

        self.user_id = str(self.scope['user'].id)
        self.upcoming_events = self.fetch_upcoming_events()
        self.checker()
        self.scheduler.add_job(self.checker, 'interval', seconds=60)
        self.scheduler.start()

    def disconnect(self, close_code):
        self.scheduler.shutdown()

    def fetch_upcoming_events(self):
        return EventInfo.objects.filter(event_participants__in=[User.objects.get(id=self.user_id)])

    def send_notification_json(self, e, when='now'):
        self.send_json({
            'type': 'notification_handler',
            'event_name': e.event_name,
            'event_id': e.id,
            'event_time_begin': e.event_begin.strftime('%H:%M'),
            'when': when
        })

    def checker(self):
        cur_date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M')
        for e in self.upcoming_events:
            if (e.event_begin + datetime.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M') == cur_date:
                self.send_notification_json(e)
            elif (e.event_begin + datetime.timedelta(hours=2, minutes=30)).replace(tzinfo=None) <= \
                    datetime.datetime.today() < (e.event_begin + datetime.timedelta(hours=3)).replace(tzinfo=None) and \
                    self.user_id not in notificated[e.id]:
                self.send_notification_json(e, 'soon')
                notificated[e.id].append(self.user_id)
