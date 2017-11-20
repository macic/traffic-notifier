class Config:
    # Integra values
    usercode = "1111"
    host = "yourip"
    port = 7094
    encoding = "cp1250"

    # mysql instance link
    db_link = 'mysql://user:pw@ip/db_name'

    # google API keys and configuration
    google_directions_url = "https://maps.googleapis.com/maps/api/directions/json"
    google_api_key = "AIzaSyAQLNYW_GMpJB3NoQCVJpg6LtFAwC6kplA"  # restricted to IP so can be public
    start_localization = "50.270289, 18.815758"
    end_localization = "Sobieskiego 2, Katowice"

    # pushover API keys and configuration
    pushover_url = "https://api.pushover.net/1/messages.json"
    pushover_key = "register_at_pusherover_com_and_get_it_for_free"
    users_to_send_msg_to = "u7m35sadasdasdasdk" # you register the device and get this kind of id


    # traffic message configuration
    default_msg_title = "TrafficNotifier"
    message_format = "Czas przejazdu {route_name} - {duration}.\n"

    # periodic check of some input state configuration on notification
    periodic_check_msg_title = "IntegraNotifier"
    periodic_msg = "Garaż otwarty!"

