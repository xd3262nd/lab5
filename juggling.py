from peewee import *

db = SqliteDatabase('juggling.sqlite')


# Model
class Record(Model):
    name = CharField(unique=True)
    country = CharField()
    num_catches = IntegerField()

    class Meta:
        database = db

    def __str__(self):
        return f'Name: {self.name}, Country: {self.country}, Number of Catches: {self.num_catches}'


# Connect and create db
db.connect()
db.create_tables([Record])


# Main
def add_new_record():
    new_name = input('What is the name of the record holder? ')
    new_country = input('Which country this person come from? ')
    new_record = input('What is the score for their catches? ')

    if new_name.strip().isalpha == False or len(new_name.strip()) < 1 or new_country.strip().isalpha() == False or len(
            new_country.strip()) < 1 or new_record.isnumeric() == False or len(new_record) == 0:
        print('Please enter the player full name, correct country name and number of the player score')
        return add_new_record()

    try:
        juggler = Record(name=new_name, country=new_country, num_catches=new_record)
        juggler.save()
        print(f'Added {juggler.name} to the record handler list.')
        return
    except IntegrityError as e:
        print(f'Error in adding record - {e}')
        return


def get_record_holder(player_name=None):
    if player_name is None or len(player_name) == 0:
        player_name = input('Please enter the juggler name here: ')

        while player_name.strip().isalpha() == False or len(player_name) < 1:
            player_name = input('Invalid input. Please enter the juggler full name: ')

    data = Record.select().where(Record.name == player_name)

    if not data.exists():
        print(f'Unable to find a juggler that named {player_name}.\n')
    else:
        for i in data:
            print('\n'+str(i)+'\n')


def get_all_record_holder():
    data = Record.select()

    if data.exists():
        for each in data:
            print(str(each) + '\n')


def update_selected_record():
    name = input('Please enter the juggler\'s name: ')
    juggler = Record.get(Record.name == name)
    if juggler:
        num_catches = int(input(f'Please enter the new number of catches for {name}:   '))
        try:
            Record.update(num_catches=num_catches).where(Record.name == name).execute()
            print(f'Updated {name} record on the system')
            return get_record_holder(name)
        except IntegrityError as e:
            print(f'Error in updating the juggler record - {e}')
            return
    else:
        print('Sorry invalid name. Please enter an existing name from the list. ')


def delete_record():
    player_name = input('Please enter the juggler\'s name: ')

    juggler = Record.get(Record.name == player_name)

    if juggler:
        try:
            Record.delete().where(Record.name == player_name).execute()
            print(f'Successfully deleted {player_name} from the list')
            return
        except IntegrityError as e:
            print(f'Error in deleting the juggler -  e')
    else:
        print('Sorry invalid name. Please enter an existing name from the list.')


def main():
    print('Welcome to the Chainsaw Juggling Application! ')
    print('Menu:')

    running = True

    while running:
        print(
            '1. Add New Record\n2. Search For An Existing Record Holder by Name\n3. Show All Record Holders\n4. '
            'Update '
            'Information of Existing Record Holder\n5. Delete a Record Holder\nQ. Quit the Program\n')
        user_selection = get_selection()

        if user_selection is None:
            print('\n\nThanks for using the program')
            running = False
        else:
            if user_selection == 1:
                add_new_record()
            elif user_selection == 2:
                get_record_holder()
            elif user_selection == 3:
                get_all_record_holder()
            elif user_selection == 4:
                update_selected_record()
            elif user_selection == 5:
                delete_record()


def get_selection():
    selection = input('Enter one of the menu option or \'q\' to quit the program. ')

    if selection.upper() == 'Q':
        return None

    try:
        selection_int = int(selection)
        if selection_int > 5 or selection_int < 0:
            print('Invalid option. Please enter one of the menu option, from number 1 to 5 or \'q\' to quit the '
                  'program.\n ')
            return get_selection()
        return selection_int
    except ValueError:
        print('Please enter one of the menu option, from number 1 to 5 or \'q\' to quit the program.\n')
        return get_selection()


main()
