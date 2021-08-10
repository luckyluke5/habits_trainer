import json
import random
import string

import requests


def callMeasurementProtocolAPI(event_name, user_id, via_notification=False):
    endpoint = "https://www.google-analytics.com/mp/collect"

    # HttpRequest(url)

    auth = 'key=AAAA7-DDDtc:APA91bHbGdJ_ZEmrXB_39DYvr-6tZ9Yg25aYWqlGYnadoGXRBx60Tqwl5JRO6I2HntZ3NJWaZsyTti8XMJtMau8U6M5-in1dkaFohuPCxEM3sBpXNM4tJJqcDQOVr7PShvMSGpdXFzP-'

    headers = {'Content-Type': 'application/json'}

    # actions = [{'title': 'Done', 'action': reverse("habits_trainer:task_done", kwargs={'task_id': self.pk})},
    #
    #            {'title': 'Snoze', 'action': reverse("habits_trainer:task_snoze", kwargs={'task_id': self.pk})}]

    # actions = [{'title': 'Done', 'action': '/tas/145/done/'},
    #
    #           {'title': 'Snoze', 'action': '/tas/145/snoze/'}]

    payloaded = {"api_secret": 'zJqPOVkDRkC7hIpH9oOIuQ',
                 "measurement_id": 'G-9M0KYCKB3Y'}

    client_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))

    api_secret = 'zJqPOVkDRkC7hIpH9oOIuQ'
    measurement_id = 'G-9M0KYCKB3Y'

    events = [{'name': event_name, 'params': {'via_notification': via_notification}}]
    dict = {'client_id': client_id, 'user_id': str(user_id), 'events': events}
    # print(json.dumps(dict))
    response = requests.post(endpoint + "?measurement_id=" + measurement_id + "&api_secret=" + api_secret,
                             data=json.dumps(dict),
                             headers=headers)
    print(response)
