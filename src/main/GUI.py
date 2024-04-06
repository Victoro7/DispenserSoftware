import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import json
import csv
import Value as val
import Program as program
import Calculations as calc

# Create the main window
root = tk.Tk()
root.title("FluidCAM")

# Create a frame to fit everything
main_frame = tk.Frame(root)  # Main frame to contain everything
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

controls_frame = tk.Frame(main_frame)  # Frame for controls (buttons, dropdowns, entry fields)
controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

grid_frame = tk.Frame(main_frame)  # Frame for the 8x12 grid
grid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

bottom_frame = tk.Frame(main_frame)  # This is a new frame for the bottom elements
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Storing all the user preferences
preference = {
    'name': None,
    'plate': None,
    'insert': None,
    'reservoir': None,
    'tip': None,
    'equip': None,
    'eject': None,
    'grid': None
}

# Add in-program grid that simulates 96-well plate, saves as np matrix
# GRID
entries = {}


# Function to toggle the entire matrix
def toggle_matrix(var):
    fill_number = fill.get() if var.get() and fill.get() else ""
    for r in range(12):  # Now loops through columns first
        for c in range(8):  # Then rows
            entries[(r, c)].delete(0, tk.END)
            entries[(r, c)].insert(0, fill_number)


# Function to toggle a row
def toggle_row_zero(r, var):
    fill_number = fill.get() if var.get() and fill.get() else ""
    for c in range(8):
        entries[(r, c)].delete(0, tk.END)
        entries[(r, c)].insert(0, fill_number)


# Function to toggle a column
def toggle_col_zero(c, var):
    fill_number = fill.get() if var.get() and fill.get() else ""
    for r in range(12):  # Adjusted for new dimensions
        entries[(r, c)].delete(0, tk.END)
        entries[(r, c)].insert(0, fill_number)


# Variable to store the fill number from the entry box
fill = tk.StringVar()
# Label for the entry box
label = tk.Label(bottom_frame, text="Enter volume (in uL)\nto fill the grid:")
label.pack(side='top', padx=5)  # 'e' for east/right
# Specify number to be filled inside the grids
fill_number_entry = tk.Entry(bottom_frame, textvariable=fill, width=10)
fill_number_entry.pack(side='top', padx=0, pady=(0, 150))

# Create the "All" (fill grid with specified number) checkbox
all_var = tk.IntVar()
all_check = tk.Checkbutton(grid_frame, text="All", variable=all_var,
                           onvalue=1, offvalue=0, command=lambda: toggle_matrix(all_var))
all_check.grid(row=0, column=0)

# Create column checkboxes to fill with the specified number
for c in range(8):  # Adjusted loop for rows
    col_var = tk.IntVar()
    chk = tk.Checkbutton(grid_frame, variable=col_var,
                         onvalue=1, offvalue=0,
                         command=lambda col=c, var=col_var: toggle_col_zero(col, var))
    chk.grid(row=0, column=c + 2)

    # Add a label below each row checkbox
    letter = chr(72 - c % 8)
    label = tk.Label(grid_frame, text=f"{letter}")
    label.grid(row=1, column=c + 2)

# Create row checkboxes to fill with the specified number
for r in range(12):  # Adjusted loop for columns
    row_var = tk.IntVar()
    chk = tk.Checkbutton(grid_frame, variable=row_var,
                         onvalue=1, offvalue=0,
                         command=lambda row=r, var=row_var: toggle_row_zero(row, var))  # Adjusted command
    chk.grid(row=r + 2, column=0)  # Adjusted position

    # Add a label to the right of each column checkbox
    label = tk.Label(grid_frame, text=f"{r + 1}")
    label.grid(row=r + 2, column=10)

# Create a 12x8 grid of entry widgets
for r in range(12):  # Adjusted loop for rows
    for c in range(8):  # Adjusted loop for columns
        entry = tk.Entry(grid_frame, width=5, justify='center')
        entry.grid(row=r + 2, column=c + 2)  # Adjusted position
        entries[(r, c)] = entry


# GRID end

# assigns a variable using user's choice
def update_selection(name, value):
    preference[name] = value


# Add procedure name, should press enter key to save name
pname_label = tk.Label(controls_frame, text="Enter procedure name:")
pname_label.pack()

pname = tk.Entry(controls_frame, width=30)
pname.pack()

# Declare StringVar objects for dropdowns
plate_var = tk.StringVar(value="Choose a plate size")
insert_var = tk.StringVar(value="Choose an insert type")
reservoir_var = tk.StringVar(value="Choose a reservoir type")
tip_var = tk.StringVar(value="Choose a tip type")


# Add Dropdowns
def dropdown(name, prompt, options, message, var, callback=None, selection_callback=None):
    f = tk.Frame(controls_frame)  # Creates frame
    f.pack(fill='x', expand=True)

    mes = tk.Label(f, text=message)  # displays the message
    mes.grid(row=0, column=0, sticky='w', padx=5)

    var.set(prompt)  # default value

    def call(value):  # can't be called outside
        if callback:
            callback(value)
        update_selection(name, value)
        if selection_callback:  # new callback after selection
            selection_callback(value)

    w = tk.OptionMenu(f, var, *options, command=call)
    w.grid(row=0, column=1)  # creates and packs dropdown menu

    f.grid_columnconfigure(1, weight=1)
    w.config(anchor='w')

    return w


# Implement the callback for updating insert options
def insert_opts(selected_plate_size):
    opt_insert = {
        "6 well plate": ["none", val.three_in_one],
        "96 well plate": ["none", val.ez_seed],
    }
    new_options = opt_insert.get(selected_plate_size, ["none"])  # Default to ["none"] if not found

    menu = dropdown_insert['menu']  # Access the menu of the OptionMenu widget
    menu.delete(0, 'end')  # Clear current options

    # update insert in preference
    def update_in(value):
        insert_var.set(value)
        update_selection('insert', value)

    # Add new options to the insert type dropdown
    for option in new_options:
        dropdown_insert['menu'].add_command(label=option, command=lambda value=option: update_in(value))
    # Update the displayed value to the first option of the new list
    insert_var.set(new_options[0])


# Plate Size
opt_plate = ["6 well plate", "96 well plate"]
p_plate = ["Choose a plate size"]
dropdown('plate', p_plate, opt_plate, "Plate Size:", plate_var, insert_opts)

# Insert type
p_insert = ["Choose an insert type"]
dropdown_insert = dropdown('insert', p_insert, ["none"], "Insert Type:", insert_var)


# Reservoir size
def greying(value):
    if value == "25":
        equip.config(state=tk.DISABLED)  # Disables the checkbox
        CheckVar1.set(0)  # also unchecks it
    else:
        equip.config(state=tk.NORMAL)


opt_res = ["1.5", "5", "25"]
p_res = ["Choose a reservoir type"]
dropdown('reservoir', p_res, opt_res, "Reservoir Type (in mL):", reservoir_var, selection_callback=greying)

# Tip Type
opt_tip = [250]
p_tip = ["Choose a tip type"]
dropdown('tip', p_tip, opt_tip, "Tip Type (in uL):", tip_var)


# Add Checkboxes:

# Tip equipped
def tip_set(protocol):
    # # Fill empty cells with '0's
    # for r in range(12):
    #     for c in range(8):
    #         if entries[(r, c)].get() == '':
    #             entries[(r, c)].delete(0, tk.END)
    #             entries[(r, c)].insert(0, '0')
    #
    # # Initialize all letters to light grey (assuming no columns are filled)
    # for label in letter_labels.values():
    #     label.config(fg="grey")
    #
    # # Mapping each letter to its corresponding columns
    # column_pairs = {
    #     'A': (0, 1),
    #     'B': (2, 3),
    #     'C': (4, 5),
    #     'D': (6, 7)
    # }
    #
    # # Check each pair of columns in the grid to determine if they are filled
    # for letter, (col_start, col_end) in column_pairs.items():
    #     is_filled = False
    #     for r in range(12):
    #         if entries[(r, col_start)].get() != '0' and entries[(r, col_end)].get() != '0':
    #             is_filled = True
    #             break
    #     # Update the color of the letter based on whether its columns are filled
    #     if is_filled:
    #         letter_labels[letter].config(fg="blue")
    #     else:
    #         letter_labels[letter].config(fg="grey")
    if protocol == val.tip4_96:
        for letter_ in letters:
            letter_labels[letter_].config(fg="#blue")
    elif protocol == val.tip2_96:
        for letter_ in letters:
            letter_labels[letter_].config(fg="grey")
        letter_labels['B'].config(fg="#blue")
        letter_labels['D'].config(fg="#blue")


# Tip Placement Label
equip_label = tk.Label(bottom_frame, text="Tip Placement", font=('Helvetica', 18, 'bold'))
equip_label.pack(pady=(10, 0))

# Frame for the Tip Positions
letters_frame = tk.Frame(bottom_frame)
letters_frame.pack()

# Reservoir Volumes Label
equip_label = tk.Label(bottom_frame, text="Reservoir Volumes", font=('Helvetica', 18, 'bold'))
equip_label.pack(pady=(10, 0))

# Frame for the Volume Positions
volume_frame = tk.Frame(bottom_frame)
volume_frame.pack()

volumes = tk.Label(volume_frame, text="Generate Procedure \nTo View Volumes", font=('Helvetica', 14, 'italic'), fg="grey")
volumes.pack()

# Letter labels
letters = ['D', 'C', 'B', 'A']
letter_labels = {}
for letter in letters:
    letter_labels[letter] = tk.Label(letters_frame, text=letter, fg="grey")
    letter_labels[letter].pack(side='left', expand=True)


# equip_label = tk.Label(bottom_frame, text="Minimum Reservoir Volumes")
# equip_label.pack(pady=(10, 0))

# # Add button to update tip selection
# tips_equip = tk.Button(bottom_frame, text="Press for tips", command=tip_set)
# tips_equip.pack()

# Updates Preference when checkbox is ticked
def update_equip():
    preference['equip'] = "TRUE" if CheckVar1.get() == 1 else None


CheckVar1 = tk.IntVar()

# Creates the checkbox
equip = tk.Checkbutton(controls_frame, text="Auto-Equip Tips",
                       fg="black", variable=CheckVar1,
                       onvalue=1, offvalue=0, command=update_equip)
equip.pack()


# Tip ejection bowl equipped
def update_eject():
    preference['eject'] = "TRUE" if CheckVar2.get() == 1 else None


CheckVar2 = tk.IntVar()

eject = tk.Checkbutton(controls_frame, text="Auto-Eject Tips",
                       fg="black", variable=CheckVar2,
                       onvalue=1, offvalue=0, command=update_eject)
eject.pack()


# Add Save
def save_preference():
    # Temporarily capture the state of the grid to check validity
    grid = [[entries[(r, c)].get() for c in range(8)] for r in range(12)]

    # Check the matrix for a string or a number above 1000 in any of the cells
    if any(True for row in grid for cell in row if not cell.isdigit() or int(cell) > 1000):
        messagebox.showwarning("Invalid Grid Input", "Please ensure all volumes are between 0 and 1000uL.")
    else:
        # updates the 'grid' in preference otherwise
        update_selection('grid', grid)

        # Capture name and save it
        update_selection('name', pname.get())

        # creates the filename name
        filename = f"{preference['name']}.json" if preference['name'] else "untitled.json"

        # Saves the updated list of preference to save.json
        with open(filename, "w") as file:
            json.dump(preference, file)
        messagebox.showinfo("Save", "Your Preferences are Saved")


save_button = tk.Button(root, text="Save Preferences", command=save_preference)
save_button.pack()


# Add Run Procedure
def run_procedure():
    save_preference()
    # Filename based on the procedure name and defaults to "untitled.json" if not provided.
    filename = f"{preference['name']}.json" if preference['name'] else "untitled.json"

    try:
        with open(filename, "r") as file:
            data = json.load(file)

        # Extract variables for build_procedure from the .json
        name = data.get('name')
        plate = data.get('plate')
        insert = data.get('insert')
        tip = int(data.get('tip'))
        vol_array = np.array(data.get('grid')).astype(np.float_)
        restype = data.get('reservoir')
        equip_ = data.get('equip')
        eject_ = data.get('eject')

        # Check if well volumes are 20 - 200 ul
        if calc.check_vol(vol_array):
            pass
        else:
            messagebox.showinfo("Volume Error", "Well Volumes must be 0 uL, or 20 uL - 200 uL")
            return

        # Check if total procedure volume is compatible with 1.5 mL tubes (if applicable)
        if restype == "1.5" and calc.get_protocol(vol_array) == val.tip2_96:
            if np.sum(vol_array[:, [0, 1, 2, 3]]) > 3000 or np.sum(vol_array[:, [4, 5, 6, 7]]) > 3000:
                messagebox.showinfo("Volume Error", "Total culture plate volume is too large for reservoir")
                return
        elif restype == "1.5" and calc.get_protocol(vol_array) == val.tip4_96:
            if (np.sum(vol_array[:, [0, 1]]) > 3000 or np.sum(vol_array[:, [2, 3]]) > 3000
                    or np.sum(vol_array[:, [4, 5]]) > 3000 or np.sum(vol_array[:, [6, 7]]) > 3000):
                messagebox.showinfo("Volume Error", "Total culture plate volume is too large for reservoir")
                return

        # Check if tip is being equipped with 25mL reservoir on stage
        if restype == "25" and equip_ == "TRUE":
            messagebox.showinfo("Setup Error", "Cannot Auto-Equip Tips with 25mL Reservoir")
            return

        # Calls program
        res_volumes = program.gui(name, plate, insert, restype, tip, vol_array, equip_, eject_)

        # Display Tip Arrangement
        protocol = calc.get_protocol(vol_array)
        tip_set(protocol)

        # Display Reservoir Volumes and Arrangement
        if restype == "25":
            volumes.config(text="%.3f mL" % (sum(res_volumes) / 1000), fg="#blue")
        elif restype == "1.5":
            converted_vol = [x / 1000 for x in res_volumes]
            volumes.config(text="(mL)\nRow A:   %.3f   %.3f   %.3f   %.3f\nRow B:   %.3f   %.3f   %.3f   %.3f"
                                % (converted_vol[0], converted_vol[1], converted_vol[2], converted_vol[3],
                                   converted_vol[4], converted_vol[5], converted_vol[6], converted_vol[7]),
                           fg="#blue")

        messagebox.showinfo("Procedure Run", "File Saved")
    except FileNotFoundError:
        messagebox.showerror("File Not Found", f"Could not find the file: {filename}")


run_procedure_button = tk.Button(root, text="Generate Procedure", command=lambda: run_procedure())
run_procedure_button.pack()


# exit button
def on_exit():
    print(f"Name of the Procedure: {preference['name']}")
    print(f"Last selected plate size: {preference['plate']}")
    print(f"Last selected insert size: {preference['insert']}")
    print(f"Last selected reservoir size: {preference['reservoir']}")
    print(f"Last entered grid: {preference['grid']}")
    root.destroy()


exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack()

# Create a bottom frame (like controls and grid frames)
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)


# Import csv file
def import_csv_file():
    # Specify the options for opening the dialog
    filetypes = [('CSV files', '*.csv'), ('All files', '*.*')]
    filename = filedialog.askopenfilename(title="Open a file", initialdir="/", filetypes=filetypes)

    # Check if a file was selected (filename will not be empty)
    if filename:
        # Reads the CSV file
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            matrix = list(reader)

            # Checks if the matrix exceeds 12x8 dimensions
            if len(matrix) > 12 or any(len(row) > 8 for row in matrix):
                messagebox.showwarning("Invalid File",
                                       "Please submit an appropriate csv file with a 12x8 matrix or smaller.")
                return  # Stop processing this file

            # Populates the grid with the matrix values or zeros
            for r in range(12):
                for c in range(8):
                    entries[(r, c)].delete(0, tk.END)
                    if r < len(matrix) and c < len(matrix[r]):
                        entries[(r, c)].insert(0, matrix[r][c])
                    else:
                        entries[(r, c)].insert(0, "0")


# Create the "Import .csv File" button
import_button = tk.Button(bottom_frame, text="Import CSV File", command=import_csv_file)
import_button.pack(side=tk.LEFT, padx=10, pady=10)  # Pack to the left side of the bottom_frame


# Load Preferences
def load_pref():  # still needs exception handling
    filetypes = [('JSON files', '*.json'), ('All files', '*.*')]
    filename = filedialog.askopenfilename(title='Open Preferences .json File', initialdir="/", filetypes=filetypes)

    if filename:
        with open(filename, 'r') as file:
            loaded_pref = json.load(file)
        global preference
        preference.update(loaded_pref)

    # updating procedure name
    pname.delete(0, tk.END)
    pname.insert(0, preference.get('name', ''))

    # updating dropdowns
    global plate_var, insert_var, reservoir_var, tip_var
    plate_var.set(preference.get('plate', 'Choose a plate size'))
    insert_var.set(preference.get('insert', 'Choose an insert type'))
    reservoir_var.set(preference.get('reservoir', 'Choose a reservoir type'))
    tip_var.set(str(preference.get('tip', 'Choose a tip type')))

    # updating checkboxes
    CheckVar1.set(1 if preference.get('equip') == "TRUE" else 0)
    CheckVar2.set(1 if preference.get('eject') == "TRUE" else 0)

    # updating grid
    grid_values = preference.get('grid', [])  # Default to an empty list if 'grid' key is not found
    for r, row in enumerate(grid_values):
        for c, cell_value in enumerate(row):
            if r < 12 and c < 8:  # Ensure within grid bounds
                entry = entries[(r, c)]
                entry.delete(0, tk.END)
                entry.insert(0, cell_value)


# Create the "Load Preferences" button
load_button = tk.Button(bottom_frame, text="Load Preferences", command=load_pref)
load_button.pack(side=tk.LEFT, padx=0, pady=10)  # Pack to the left side of the bottom_frame

root.mainloop()
