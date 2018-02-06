from Contact import Contact
import pickle

# 1. Fetch the data from FS and deserialize it
# 2. Display the list of Contacts
# 3. Ask User to choose an option for i.CREATE ii.UPDATE iii.DELETE iv.SEARCH v.Exit

backup_file_name = 'addressbook.data'

def fetch_contact_list():
    '''This will fetch whole list of contacts from FS'''
    f = None
    try:
        f = open(backup_file_name, 'rb')
        if f:
            contact_list = pickle.load(f)
            return contact_list
    except IOError:
        print 'Couldn\'t find any contact file, first create one'
    except EOFError:
        print 'EOF error occured'
    finally:
        if f:
            f.close()
            print 'closing the file'

def display_contact_list():
    '''This will display the list of contacts'''
    contact_list = fetch_contact_list()
    if contact_list:
        for contact_name in contact_list:
            contact_obj = contact_list[contact_name]
            display_contact( contact_name, contact_obj)
    else:
        print 'No contact list found!'

def display_contact( name, contact ):
    if name and contact:
        print name + '::'
        for key, value in contact.__dict__.iteritems():
            print '\t',key,':',value

def backup_contact_list( contact_list ):
    f = None
    try:
        f = open(backup_file_name, 'wb')
        pickle.dump(contact_list, f)
        return True
    except IOError:
        print 'Couldn\'t find any contact file, first create one'
        return False
    except EOFError:
        print 'EOF error occured'
        return False
    finally:
        if f:
            f.close()
 
def add_contact(contact):
    contact_list = fetch_contact_list()
    status = None
    if contact and contact.name:
        if not contact_list:
            contact_list = {}
        contact_list[contact.name] = contact
        status = backup_contact_list( contact_list )
    return status
            
def create_new_contact():
    print 'Enter new contact details'
    contact_name = raw_input('Name: ')
    contact_group = raw_input('Category: ')
    contact_email = raw_input('Email: ')
    contact_phone = raw_input('Phone: ')

    contact = Contact(contact_name, contact_group, contact_email, contact_phone)
    status = add_contact(contact)
    if status:
        print 'Contact created successfully'
    else:
        print 'There is some problem creating new contact'

def update_contact():
    contact_name = raw_input('Enter the Contact Name that you want to update: ')
    contact_list = fetch_contact_list()
    status = None
    if contact_list and contact_name in contact_list:
        contact_group = raw_input('New Group for {}: '.format(contact_name))
        contact_email = raw_input('New Email for {}: '.format(contact_name))
        contact_phone = raw_input('New Phone for {}: '.format(contact_name))
        contact = Contact(contact_name, contact_group, contact_email, contact_phone)
        contact_list[contact_name] = contact
        status = backup_contact_list( contact_list )
    else:
        status = False
    return status

def delete_contact():
    contact_name = raw_input('Enter the Contact Name that you want to delete: ')
    contact_list = fetch_contact_list()
    status = None
    if contact_list and contact_name in contact_list:
        del contact_list[contact_name]
        status = backup_contact_list( contact_list )
    else:
        status = False
    return status

def search_contact( contact_name ):
    contact_list = fetch_contact_list()
    if contact_list and contact_name in contact_list:
        contact = contact_list[contact_name]
        display_contact(contact_name, contact)
    else:
        print 'Contact not found'

def main():
    display_contact_list()
    while True:
        user_option = raw_input('Choose an option for 1.CREATE 2.UPDATE 3.DELETE 4.SEARCH 5.LIST 6.Exit :: ')
        if int(user_option) == 1:
            create_new_contact()
        elif int(user_option) == 2:
            status = update_contact()
            if status:
                print 'Contact updated successfully'
            else:
                print 'Some problem occured during contact updation'
        elif int(user_option) == 3:
            status = delete_contact()
            if status:
                print 'Contact deleted successfully'
            else:
                print 'Some problem occured during contact deletion'
        elif int(user_option) == 4:
            contact_name = raw_input('Enter the contact name that you want to see: ')
            search_contact(contact_name)
        elif int(user_option) == 5:
            display_contact_list()
        elif int(user_option) == 6:
            break

if __name__ == '__main__':
    main()
