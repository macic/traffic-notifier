import baker
from database.models import Input
from integra.integra import get_name, check_state


@baker.command
def fill_inputs(end_number):
    """
    Deletes all existing input names in db and recreates them
    :param end_number: number of input to check
    :return: number of rows inserted
    """
    Input.create_table(True)
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
        #insert many with db.atomic failed for tests: s peewee issue?: O
    return len(data_source)

@baker.command
def get_input_state(number):
    name = Input.get(Input.number==int(number)).name
    return name, check_state(number)

if __name__ == "__main__":
    baker.run()
