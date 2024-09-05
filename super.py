import helpers






# Instaniate what type of program this should be
ISMASTER = False
MASTERIMG = False
AUTOUPDATE = False

last_variable_name = None
foundUSB = False
config = ""

while True:
    print("-> STARTING PROGRAM")
    # Find and connect to USB drive
    if not foundUSB:
        print("-> LOOKING FOR USB")
        usb_path = helpers.find_usb_drive()
    if usb_path and config == "":
        foundUSB = True
        print(f"USB FOUND", usb_path)
        print("-> READING USB")
        config = helpers.get_text_file_on_usb(usb_path, 'config.txt')
        print("READ DONE")
    if not foundUSB and usb_path == None:
        print("USB NOT FOUND")
        foundUSB = False

    # Do pre program stuff, like update, and setups
    if(AUTOUPDATE):
        print("-> CHECKING FOR UPDATES")
        helpers.git_pull()
        print("UPDATES DONE")
    
    # Construct the API URL
    if(ISMASTER):
        print("MASTER SCRIPT START")
        if(MASTERIMG):
            print("MASTERIMG")
    else:
        print("SLAVE SCRIPT START")



if __name__ == '__main__':
    # Start the Flask API server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # Allows Flask thread to exit when the main program exits
    flask_thread.start()

    # Start listening to MIDI signals in the main thread
    midi_listener()