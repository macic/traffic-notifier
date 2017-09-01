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

    def send_notification(self, traffic):
        simplified_response = self.parse_response(traffic)
        message = ""
        for route in simplified_response:
            addition = self.config.message_format.format(**route)
            message += addition
        params = {"token": self.config.pushover_key,
                  "user": self.config.users_to_send_msg_to,
                  "title": self.config.default_msg_title,
                  "message": message}
        response = requests.post(self.config.pushover_url, params)
        if response.json().get("status") == 1:
            return True
        else:
            return response.status_code, response.json()
