import baker
from database.models import Input, InputState
from integramod.integra import get_name, check_state


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
def fill_inputs(end_number):
    """
    Deletes all existing input names in db and recreates them
    :param end_number: number of input to check
    :return: number of rows inserted
    """
    data_source = []
    for i in range(1, int(end_number) + 1):
        if i % 8 != 0:
            name = get_name(i)
            if name:
                data_source.append({'name': name, 'number': i})
    query = Input.delete()
    query.execute()

    for data in data_source:
        Input.create(name=data.get('name'), number=data.get('number'))
        # insert many with db.atomic failed for tests: s peewee issue?: O
    return len(data_source)


def get_input_state(number):
    input = Input.get(Input.number == int(number))
    return input, check_state(int(number))

@baker.command
def run_all(number):
    input, state = get_input_state(number)
    if state:
        InputState.create(input=input, state=state)


if __name__ == "__main__":
    baker.run()
