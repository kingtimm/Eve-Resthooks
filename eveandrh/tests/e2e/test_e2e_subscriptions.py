import json
from threading import Thread
from flask import Flask, request
import requests
from eve.render import render_json as eve_render_json
from eveandrh.tests.test_subscriptions import TestSubscriptions

subscribed_app = Flask(__name__)
subscribed_app.__called__ = False


@subscribed_app.route("/dummy", methods=['GET', 'POST'])
def dummy_endpoint():
    subscribed_app.__called__ = True

    return "OK"


@subscribed_app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def start_server():
    subscribed_app.run(port=6000)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


class TestE2ESubscriptions(TestSubscriptions):

    def setUp(self):
        super().setUp()
        self.tc = self.apiapp.test_client()
        subscribed_app.__called__ = False

        self.subscribed_app_thread = Thread(target=start_server)
        self.subscribed_app_thread.start()

        self.apiapp.on_inserted__jobs += self.on_eve_event_handle

    def tearDown(self):
        result = requests.post('http://localhost:6000/shutdown')
        self.subscribed_app_thread.join(timeout=3)
        subscribed_app.__called__ = False
        super().tearDown()

    def post_dummy_book_created_subscription(self):
        payload = dict(
            event="devices.created",
            target_url="http://localhost:6000/dummy",
        )
        return self.tc.post("/api/v1/subscriptions", data=json.dumps(payload), headers=self.headers)

    def on_eve_event_handle(self, items):
        """Makes a request on a new job. Normally this would be done by a pool of workers.

        :param items: Items passed in by an eve on_inserted
        :return:
        """

        return [
            requests.post(url=item['target_url'], data=eve_render_json(item['payload']), headers=self.headers)
            for item in items
        ]

    def test_gets_called(self):
        response = requests.get("http://localhost:6000/dummy")
        self.assertTrue(subscribed_app.__called__)

    def test_not_called(self):
        self.assertFalse(subscribed_app.__called__)

    def test_add_subscription_calls_hook_target(self):
        sub_result = self.post_dummy_book_created_subscription()

        self.assertFalse(subscribed_app.__called__)

        payload = dict(
            name="device master",
        )
        self.tc.post("/api/v1/devices", data=json.dumps(payload), headers=self.headers)

        self.assertTrue(subscribed_app.__called__)