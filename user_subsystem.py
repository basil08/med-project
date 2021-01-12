# builtins
import math
import time

# installed
from consolemenu import *
from consolemenu.items import *

# my modules
import login
import view

def show_submenu(menu):
    menu.show()

def initialize():
    rcd = login.login()
    if rcd == None: # shouldn't be needed, but a security check
        pass
    else:
        # setup a menu
        # and welcome the patient
        export_bin_item = FunctionItem("Export Your Data To Binary", view.export_to_bin, [rcd])
        export_csv_item = FunctionItem("Export Your Data To CSV", view.export_to_csv, [rcd])
        basic_info_item = FunctionItem("View General Information", view.basic_info, [rcd])
        body_data_item = FunctionItem("View Body Data", view.body_data, [rcd])

        record_data_subitem = FunctionItem("Record Body Data", view.record_data, [rcd])

        # NOTE: THIS rcd NOW HAS TO POINT TO THE NEW UPDATED RECORD OF THE PATIENT
        edit_data_subitem = FunctionItem("Edit Your Profile", view.edit_pfp, [rcd])

        menu = ConsoleMenu("Welcome, {0}".format(rcd['fname']), "I am med, your personal health asistance program.")

        appointment_menu = ConsoleMenu("Appointments", "Everything related to appointments in one place.")
        apppointment_item = FunctionItem("Appointments", show_submenu, [appointment_menu])
        
        notifications_menu = ConsoleMenu("Notifications", "Be updated, be healthy. Always.")
        notifications_item = FunctionItem("Notifications", show_submenu, [notifications_menu])

        sos_menu = ConsoleMenu("SOS Broadcast", "In case of emergency, we are always by your side.")
        sos_item = FunctionItem("SOS Broadcast", show_submenu, [sos_menu])

        medbay_menu = ConsoleMenu("Medbay Online", "One-stop shop for all your meds.")
        medbay_item = FunctionItem("Medbay Online", show_submenu, [medbay_menu])

        record_data_menu = ConsoleMenu("Record Your Data", "A dynamic history to better track your health.")
        record_data_item = FunctionItem("Record Your Data", show_submenu, [record_data_menu])
        
        view_details_menu = ConsoleMenu("View My Profile", "All your data, now at your fingertips.")
        view_details_item = FunctionItem("View My Profile", show_submenu, [view_details_menu])
        
        edit_details_menu = ConsoleMenu("Edit Profile", "Edit your profile and preferences.")
        edit_details_item = FunctionItem("Edit Profile", show_submenu, [edit_details_menu])

        view_details_menu.append_item(basic_info_item)
        view_details_menu.append_item(body_data_item)
        view_details_menu.append_item(export_csv_item)
        view_details_menu.append_item(export_bin_item)

        record_data_menu.append_item(record_data_subitem)

        edit_details_menu.append_item(edit_data_subitem)

        menu.append_item(notifications_item)
        menu.append_item(sos_item)
        menu.append_item(apppointment_item)
        menu.append_item(medbay_item)
        menu.append_item(record_data_item)
        menu.append_item(view_details_item)
        menu.append_item(edit_details_item)
        #time.sleep(1.5)
        menu.show()

"""
# Import the necessary packages
from consolemenu import *
from consolemenu.items import *

# Create the menu
menu = ConsoleMenu("Title", "Subtitle")

# Create some items

# MenuItem is the base class for all items, it doesn't do anything when selected
menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# A CommandItem runs a console command
command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])

# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# Once we're done creating them, we just add the items to the menu
menu.append_item(menu_item)
menu.append_item(function_item)
menu.append_item(command_item)
menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()

"""
