from datetime import datetime, timedelta
import requests
from database.models import Input, InputState
from integramod.integra import check_state


class TrafficNotifer:
    def __init__(self, config):
        self.config = config

    def check_input_state(self, number):
        input = Input.get(Input.number == int(number))
        state = check_state(self.config, int(number))
        if state:
            InputState.create(input=input, state=state)
            return True

    def compare_last_state(self, number, minutes):
        input = Input.get(Input.number == int(number))
        state = check_state(self.config, int(number))
        if state:
            ts = datetime.now() - timedelta(minutes=int(minutes))
            in_last_period = InputState.select().where((InputState.input == input) & (InputState.datetime >= ts))
            if in_last_period:
                InputState.create(input=input, state=state)
                return True
            InputState.create(input=input, state=state)

    def check_traffic(self):
        params = {"departure_time": "now",
                  "origin": self.config.start_localization,
                  "destination": self.config.end_localization,
                  "key": self.config.google_api_key,
                  "alternatives": "true"}
        response = requests.get(self.config.google_directions_url, params)
        if response.status_code == 200:
            return response.json()

    @staticmethod
    def parse_response(traffic_response):
        routes = traffic_response.get("routes", [])
        response = []
        for route in routes:
            response.append({
                'route_name': route.get("summary"),
                'duration': route.get("legs")[0].get("duration_in_traffic",
                                                     route.get("legs")[0].get("duration").get("text")).get("text")
            })
        return response

    def prepare_traffic_msg(self, traffic):
        simplified_response = self.parse_response(traffic)
        message = ""
        for route in simplified_response:
            addition = self.config.message_format.format(**route)
            message += addition
        return message

    def send_notification(self, message, title):
        params = {"token": self.config.pushover_key,
                  "user": self.config.users_to_send_msg_to,
                  "title": title,
                  "message": message}
        response = requests.post(self.config.pushover_url, params)
        if response.json().get("status") == 1:
            return True
        else:
            return response.status_code, response.json()
