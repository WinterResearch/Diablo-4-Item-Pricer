import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
import pandas as pd
import os

main_stat_types = {
    'None': ['Cooldown Reduction', 'Maximum Mana', 'Lucky Hit Chance while Barrier', 'Percent Total Armor', 'Maximum Life'],
    'Focus': ['Cooldown Reduction', 'Resource Generation', 'Mana Cost Reduction', 'Critical Strike Chance', 'Lucky Hit Resource', 'Crackling Damage', 'Lucky Hit Barrier', 'Crit Chance Injured'],
    'Gloves': ['Ranks Ice Shards', 'Critical Strike Chance', 'Attack Speed', 'Lucky Hit Chance Resource', 'Lucky Hit Chance', 'Ranks Chain Lightning', 'Intelligence', 'Crit Strike Injured', 'Lucky Hit Heal', 'All Stats', 'Ranks Frozen Orb'],
    'Pants': ['Damage Reduction Burning', 'Damage Reduction Close', 'Damage Reduction', 'Damage Reduction Distant', 'Percent Total Armor', 'Intelligence', 'Ranks Blizzard'],
    'Boots': ['Mana Cost Reduction', 'Ranks Frost Nova', 'Movement Speed', 'Ranks Teleport', 'Slow Duration', 'Movement Speed After Elite', 'All Stats', 'Dodge Chance', 'Shadow Resist', 'Ranks Ice Armor'],
    'Wand': ['Critical Strike Damage', 'Vulnerable Damage', 'Intelligence', 'Core Skill Damage', 'Damage Close', 'Lucky Execute Elites', 'Ultimate Skill Damage', 'Basic Skill Damage', 'Damage Crowd', 'Damage Slowed', 'Damage Over Time', 'Damage Burning', 'Damage Injured', 'Overpower Damage'],
    'Amulet': ['Cooldown Reduction', 'Mana Cost Reduction', 'Ranks Devouring Blaze', 'Ranks Defensive Skills', 'Damage Reduction Burning', 'Healing Received', 'Movement Speed', 'Strength', 'Damage Reduction', 'Thorns', 'Shock Skill Damage', 'Speed After Elite', 'Damage', 'Ultimate Skill Dmg', 'Lucky Hit Barrier', 'Ranks Conjuration', 'Ranks Icy Touch'],
    'Ring': ['Critical Strike Damage', 'Vulnerable Damage', 'Resource Generation', 'Critical Strike Chance', 'Maximum Mana', 'Damage Crowd', 'Lightning Damage', 'Damage Chilled', 'Cold Damage', 'Maximum Life', 'Barrier Generation', 'Overpower Damage', 'Life Regen', 'Lucky Hit Chance','Crackling Damage'],
    'Helm': ['Cooldown Reduction', 'Maximum Mana', 'Lucky Hit Chance while Barrier', 'Percent Total Armor', 'Maximum Life', 'Intelligence', 'Resist Type', 'CC Duration'],
    'Chest': ['Damage Reduction Distance', 'Damage Reduction Close', 'Strength', 'Total Armor']
    # Add the main stat types for the other slots
}

#todo add a personal flip section, post buys, follow up with true sold price, reflect in historical db, maintain "pnl" / error reducing
root = tk.Tk()
root.grid_columnconfigure(1, weight=1)

root.title('Diablo MMO Item Pricer')

slot_var = tk.StringVar()
stat1_type_var = tk.StringVar()
stat2_type_var = tk.StringVar()
stat3_type_var = tk.StringVar()
stat4_type_var = tk.StringVar()

# Function to update stat type options
def update_stat_type_options(*args):
    slot = slot_var.get()
    stat1_type_menu['menu'].delete(0, 'end')
    stat2_type_menu['menu'].delete(0, 'end')
    stat3_type_menu['menu'].delete(0, 'end')
    stat4_type_menu['menu'].delete(0, 'end')
    if slot in main_stat_types:
        for stat in main_stat_types[slot]:
            try:
                stat1_type_menu['menu'].add_command(label=stat, command=lambda stat=stat: stat1_type_var.set(stat))
                stat2_type_menu['menu'].add_command(label=stat, command=lambda stat=stat: stat2_type_var.set(stat))
                stat3_type_menu['menu'].add_command(label=stat, command=lambda stat=stat: stat3_type_var.set(stat))
                stat4_type_menu['menu'].add_command(label=stat, command=lambda stat=stat: stat4_type_var.set(stat))
            except Exception as e:
                print(f'Error encountered for stat {stat}: {str(e)}')

# Function to validate input and add the item to the database
def submit_item():
    try:
        # Check if all entries are filled
        for entry in [slot_var, power_entry, level_entry, stat1_type_var, stat1_value_entry, stat2_type_var, stat2_value_entry, 
                      stat3_type_var, stat3_value_entry, stat4_type_var, stat4_value_entry, dps_entry, sold_value_entry]:
            if not entry.get():
                raise ValueError("Please fill all entries")

        # Define a function to sort stats by order
        def sort_stats_by_order(slot, stat_types, stat_values):
            if slot in main_stat_types:
                order = main_stat_types[slot]
                stat_types_sorted = sorted(stat_types, key=lambda x: order.index(x) if x in order else len(order))
                stat_values_sorted = [stat_values[stat_types.index(x)] for x in stat_types_sorted]
                return stat_types_sorted, stat_values_sorted
            else:
                return stat_types, stat_values

        # Get stats and their values
        stat_types = [stat1_type_var.get(), stat2_type_var.get(), stat3_type_var.get(), stat4_type_var.get()]
        stat_values = [float(stat1_value_entry.get()), float(stat2_value_entry.get()), float(stat3_value_entry.get()), float(stat4_value_entry.get())]

        # Sort stats by order
        stat_types, stat_values = sort_stats_by_order(slot_var.get(), stat_types, stat_values)

        # Construct the item data
        item_data = {
            'Slot': slot_var.get(),
            'Item Power': int(power_entry.get()),
            'Level': int(level_entry.get()),
            'Stat1 Type': stat_types[0],
            'Stat1 Value': stat_values[0],
            'Stat2 Type': stat_types[1],
            'Stat2 Value': stat_values[1],
            'Stat3 Type': stat_types[2],
            'Stat3 Value': stat_values[2],
            'Stat4 Type': stat_types[3],
            'Stat4 Value': stat_values[3],
            'DPS': float(dps_entry.get()),
            'Sold Value': float(sold_value_entry.get())
        }

        add_item_to_database(item_data, "items.csv")
        
        messagebox.showinfo("Success", "Item added successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_item_to_pricing():
    try:
        # Check if all entries are filled
        for entry in [slot_var, power_entry, level_entry, stat1_type_var, stat1_value_entry, stat2_type_var, stat2_value_entry, 
                      stat3_type_var, stat3_value_entry, stat4_type_var, stat4_value_entry, dps_entry]:
            if not entry.get():
                raise ValueError("Please fill all entries")

        # Construct the item data
        item_data = {
            'Slot': slot_var.get(),
            'Item Power': int(power_entry.get()),
            'Level': int(level_entry.get()),
            'Stat1 Type': stat1_type_var.get(),
            'Stat1 Value': float(stat1_value_entry.get()),
            'Stat2 Type': stat2_type_var.get(),
            'Stat2 Value': float(stat2_value_entry.get()),
            'Stat3 Type': stat3_type_var.get(),
            'Stat3 Value': float(stat3_value_entry.get()),
            'Stat4 Type': stat4_type_var.get(),
            'Stat4 Value': float(stat4_value_entry.get()),
            'DPS': float(dps_entry.get()),
        }

        add_item_to_database(item_data, "price_option.csv")
        
        messagebox.showinfo("Success", "Item added successfully to pricing options!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def submit_item():
    try:
        # Check if all entries are filled
        for entry in [slot_var, power_entry, level_entry, stat1_type_var, stat1_value_entry, stat2_type_var, stat2_value_entry, 
                      stat3_type_var, stat3_value_entry, stat4_type_var, stat4_value_entry, dps_entry, sold_value_entry]:
            if not entry.get():
                raise ValueError("Please fill all entries")

        # Construct the item data
        item_data = {
            'Slot': slot_var.get(),
            'Item Power': int(power_entry.get()),
            'Level': int(level_entry.get()),
            'Stat1 Type': stat1_type_var.get(),
            'Stat1 Value': float(stat1_value_entry.get()),
            'Stat2 Type': stat2_type_var.get(),
            'Stat2 Value': float(stat2_value_entry.get()),
            'Stat3 Type': stat3_type_var.get(),
            'Stat3 Value': float(stat3_value_entry.get()),
            'Stat4 Type': stat4_type_var.get(),
            'Stat4 Value': float(stat4_value_entry.get()),
            'DPS': float(dps_entry.get()),
            'Sold Value': float(sold_value_entry.get())
        }

        add_item_to_database(item_data, "items.csv")  # Uncomment this line
        
        messagebox.showinfo("Success", "Item added successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Place this function definition above the submit button creation
submit_button = tk.Button(root, text="Submit", command=submit_item)
submit_button.grid(row=20,columnspan=2)
from itertools import permutations

def add_item_to_database(item_data, file_name):
    # Get all the permutations of the stat type and value pairs
    stat_type_values = list(permutations([(item_data['Stat1 Type'], item_data['Stat1 Value']),
                                          (item_data['Stat2 Type'], item_data['Stat2 Value']),
                                          (item_data['Stat3 Type'], item_data['Stat3 Value']),
                                          (item_data['Stat4 Type'], item_data['Stat4 Value'])]))

    # Generate a new row for each permutation
    for perm in stat_type_values:
        new_item_data = item_data.copy()
        new_item_data['Stat1 Type'], new_item_data['Stat1 Value'] = perm[0]
        new_item_data['Stat2 Type'], new_item_data['Stat2 Value'] = perm[1]
        new_item_data['Stat3 Type'], new_item_data['Stat3 Value'] = perm[2]
        new_item_data['Stat4 Type'], new_item_data['Stat4 Value'] = perm[3]

        df = pd.DataFrame([new_item_data])

        if os.path.isfile(file_name):
            df.to_csv(file_name, mode='a', header=False, index=False)
        else:
            df.to_csv(file_name, index=False)

# Slot
slot_label = tk.Label(root, text='Slot')
slot_label.grid(row=0, column=0)
slot_menu = ttk.OptionMenu(root, slot_var, *main_stat_types.keys(), command=update_stat_type_options)
slot_menu.grid(row=0, column=1)

# Item Power
power_label = tk.Label(root, text='Item Power')
power_label.grid(row=1, column=0)
power_entry = tk.Entry(root)
power_entry.grid(row=1, column=1)

# Level
level_label = tk.Label(root, text='Level')
level_label.grid(row=2, column=0)
level_entry = tk.Entry(root)
level_entry.grid(row=2, column=1)

# Stat1 Type
stat1_type_label = tk.Label(root, text='Stat1 Type')
stat1_type_label.grid(row=3, column=0)
stat1_type_menu = ttk.OptionMenu(root, stat1_type_var, '')
stat1_type_menu.grid(row=3, column=1)

# Stat1 Value
stat1_value_label = tk.Label(root, text='Stat1 Value')
stat1_value_label.grid(row=4, column=0)
stat1_value_entry = tk.Entry(root)
stat1_value_entry.grid(row=4, column=1)

# Stat2 Type
stat2_type_label = tk.Label(root, text='Stat2 Type')
stat2_type_label.grid(row=5, column=0)
stat2_type_menu = ttk.OptionMenu(root, stat2_type_var, '')
stat2_type_menu.grid(row=5, column=1)

# Stat2 Value
stat2_value_label = tk.Label(root, text='Stat2 Value')
stat2_value_label.grid(row=6, column=0)
stat2_value_entry = tk.Entry(root)
stat2_value_entry.grid(row=6, column=1)

# Stat3 Type
stat3_type_label = tk.Label(root, text='Stat3 Type')
stat3_type_label.grid(row=7, column=0)
stat3_type_menu = ttk.OptionMenu(root, stat3_type_var, '')
stat3_type_menu.grid(row=7, column=1)

# Stat3 Value
stat3_value_label = tk.Label(root, text='Stat3 Value')
stat3_value_label.grid(row=8, column=0)
stat3_value_entry = tk.Entry(root)
stat3_value_entry.grid(row=8, column=1)

# Stat4 Type
stat4_type_label = tk.Label(root, text='Stat4 Type')
stat4_type_label.grid(row=9, column=0)
stat4_type_menu = ttk.OptionMenu(root, stat4_type_var, '')
stat4_type_menu.grid(row=9, column=1)

# Stat4 Value
stat4_value_label = tk.Label(root, text='Stat4 Value')
stat4_value_label.grid(row=10, column=0)
stat4_value_entry = tk.Entry(root)
stat4_value_entry.grid(row=10, column=1)

# DPS
dps_label = tk.Label(root, text='DPS')
dps_label.grid(row=11, column=0)
dps_entry = tk.Entry(root)
dps_entry.grid(row=11, column=1)

# Sold Value
sold_value_label = tk.Label(root, text='Sold Value')
sold_value_label.grid(row=12, column=0)
sold_value_entry = tk.Entry(root)
sold_value_entry.grid(row=12, column=1)

price_option_button = tk.Button(root, text="Add to Pricing Options", command=add_item_to_pricing)
price_option_button.grid(row=21,columnspan=2)


root.mainloop()
