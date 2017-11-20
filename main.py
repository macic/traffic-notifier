import baker

from controller import TrafficNotifer
from database.models import Input, InputState
from integramod.integra import get_name
from config import Config


@baker.command
def create_tables():
    Input.create_table(True)
    InputState.create_table(True)


@baker.command
def list_inputs():
    inputs = Input.select().execute()
    for input in inputs:
        print(input.number, input.name)


@baker.command
def fill_inputs_table(end_number):
    """
    Deletes all existing input names in db and recreates them
    :param end_number: number of input to check
    :return: number of rows inserted
    """
    data_source = []
    for i in range(1, int(end_number) + 1):
        if i % 8 != 0:
            name = get_name(Config, i)
            if name:
                data_source.append({'name': name, 'number': i})
    query = Input.delete()
    query.execute()

    for data in data_source:
        Input.create(name=data.get('name'), number=data.get('number'))
        # insert many with db.atomic failed for tests: s peewee issue?: O
    return len(data_source)


@baker.command
def route_check():
    tn = TrafficNotifer(Config)
    response = tn.check_traffic()
    print(tn.send_notification(response))


@baker.command
def cron_job(number):
    """
    Main method to execute preferably in crontab
    :param number: input number
    :return: 
    """
    tn = TrafficNotifer(Config)

    # 1. connect to integra
    # 2. get state of input no
    # 3. save it to db if positive
    integra_input_state = tn.check_input_state(number)

    # 4. check traffic
    if integra_input_state:
        traffic = tn.check_traffic()
        # 5. prepare msg based on traffic response from google
        msg = tn.prepare_traffic_msg(traffic)
        # 6. send notification
        tn.send_notification(msg, Config.default_msg_title)

@baker.command
def cron_job_state_true_for_too_long(number, minutes):
    """
    If state of some input is set to True for too long it sends notification
    :param number: input number
    :param minutes: period between checks in minutes
    :return:
    """

    tn = TrafficNotifer(Config)
    send_notification = tn.compare_last_state(number, minutes)

    if send_notification:
        tn.send_notification(Config.periodic_msg, Config.periodic_check_msg_title)


if __name__ == "__main__":
    baker.run()
