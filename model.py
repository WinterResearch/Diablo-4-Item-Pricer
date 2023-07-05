# Importing pandas
import pandas as pd

# Define the main stat types for each slot
main_stat_types = {
    'None': ['Cooldown Reduction', 'Maximum Mana', 'Lucky Hit Chance while Barrier', 'Percent Total Armor', 'Maximum Life'],
    'Focus': ['Cooldown Reduction', 'Resource Generation', 'Mana Cost Reduction', 'Critical Strike Chance', 'Lucky Hit Resource'],
    'Gloves': ['Ranks Ice Shards', 'Critical Strike Chance', 'Attack Speed', 'Lucky Hit Chance Resource', 'Lucky Hit Chance'],
    'Pants': ['Damage Reduction Burning', 'Damage Reduction Close', 'Damage Reduction', 'Damage Reduction Distant', 'Percent Total Armor'],
    'Boots': ['Mana Cost Reduction', 'Ranks Frost Nova', 'Movement Speed', 'Ranks Teleport'],
    'Wand': ['Critical Strike Damage', 'Vulnerable Damage', 'Intelligence', 'Core Skill Damage', 'Damage Close'],
    'Amulet': ['Cooldown Reduction', 'Mana Cost Reduction', 'Ranks Devouring Blaze', 'Ranks Defensive Skills', 'Damage Reduction Burning', 'Healing Received', 'Movement Speed'],
    'Ring': ['Critical Strike Damage', 'Vulnerable Damage', 'Resource Generation', 'Critical Strike Chance', 'Maximum Mana', 'Damage Crowd', 'Lightning Damage', 'Damage Chilled', 'Cold Damage', 'Maximum Life'],
    'Helm': ['Cooldown Reduction', 'Maximum Mana', 'Lucky Hit Chance while Barrier', 'Percent Total Armor', 'Maximum Life'],
    # Add the main stat types for the other slots
}
# Load the items data
items = pd.read_csv('items.csv')

# Query whether the user wants to add a new item
add_item = input("Do you want to add a new item? Press 1 for Yes, 2 for No: ")

while add_item == "1":
    # Prompt the user to select a slot
    print("Select a slot:")
    for i, slot in enumerate(main_stat_types.keys(), 1):
        print(f"{i}. {slot}")
    slot_index = int(input("Enter the number for the slot: ")) - 1
    slot = list(main_stat_types.keys())[slot_index]

    # Prompt the user to enter the item power, level and DPS
    item_power = float(input("Enter the item power: "))
    level = int(input("Enter the item level: "))
    DPS = float(input("Enter the DPS: "))
    sold_value = float(input("Enter the sold value: "))  
    # Initialize stat types and values
    stat_types = []
    stat_values = []

    # Prompt the user to select stat types and enter corresponding values
    for i in range(4):
        print(f"Select stat{i+1} type:")
        for j, stat_type in enumerate(main_stat_types[slot], 1):
            print(f"{j}. {stat_type}")
        stat_index = int(input(f"Enter the number for stat{i+1} type: ")) - 1
        stat_type = main_stat_types[slot][stat_index]
        stat_types.append(stat_type)

        stat_value = float(input(f"Enter the value for {stat_type}: "))
        stat_values.append(stat_value)

    # Construct a new item
    new_item = pd.DataFrame({
        'Slot': [slot],
        'Item Power': [item_power],
        'Level': [level],
        'Stat1 Type': [stat_types[0]],
        'Stat1 Value': [stat_values[0]],
        'Stat2 Type': [stat_types[1]],
        'Stat2 Value': [stat_values[1]],
        'Stat3 Type': [stat_types[2]],
        'Stat3 Value': [stat_values[2]],
        'Stat4 Type': [stat_types[3]],
        'Stat4 Value': [stat_values[3]],
        'DPS': [DPS],
        'Sold Value': [sold_value]
    })

    # Append the new item to the items DataFrame
    items = items.append(new_item, ignore_index=True)

    # Query whether the user wants to add another new item
    add_item = input("Do you want to add another new item? Press 1 for Yes, 2 for No: ")

# Save the updated items data to the CSV file
items.to_csv('items.csv', index=False)

# Print the first few rows of the data
print(items.head())


# Descriptive statistics for the numeric columns
print(items.describe())

# Check for missing data
print(items.isnull().sum())









# Define a function that checks if an item has at least 3 of the 4 main stat types
def has_main_stats(row):
    slot = row['Slot']
    stat_types = row[['Stat1 Type', 'Stat2 Type', 'Stat3 Type', 'Stat4 Type']].values
    return sum(stat in main_stat_types[slot] for stat in stat_types) >= 3

# Apply the function to each item and create a new binary column 'HasMainStats'
items['HasMainStats'] = items.apply(has_main_stats, axis=1)







# Importing required libraries
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Define numerical columns
num_cols = ['Item Power', 'Level', 'Stat1 Value', 'Stat2 Value', 'Stat3 Value', 'Stat4 Value', 'DPS', 'HasMainStats']
# Other preprocessing steps remain the same


# Define categorical columns
cat_cols = ['Slot', 'Stat1 Type', 'Stat2 Type', 'Stat3 Type', 'Stat4 Type']

# Numerical data missing value handler
num_imputer = SimpleImputer(strategy='median')

# Categorical data missing value handler
cat_imputer = SimpleImputer(strategy='most_frequent')

# One-hot encoder for categorical columns
ohe_encoder = OneHotEncoder(drop='first', sparse=False)

# Preprocessing for numerical data
num_transformer = Pipeline(steps=[
    ('imputer', num_imputer)
])

# Preprocessing for categorical data
cat_transformer = Pipeline(steps=[
    ('imputer', cat_imputer),
    ('onehot', ohe_encoder)
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_cols),
        ('cat', cat_transformer, cat_cols)
    ])

# Apply preprocessing to the items data
items_preprocessed = preprocessor.fit_transform(items.drop("Sold Value", axis=1))

# Print the shape of the preprocessed data
print(items_preprocessed.shape)

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Split data into features and target
X = items_preprocessed
y = items['Sold Value']

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model 
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model
model.fit(X_train, y_train)

# Get predictions
predictions = model.predict(X_val)

# Calculate MAE
mae = mean_absolute_error(y_val, predictions)

print("Validation MAE: ", mae)


# Load new items data
new_items = pd.read_csv('price_option.csv')

# Create 'HasMainStats' feature for new items
new_items['HasMainStats'] = new_items.apply(has_main_stats, axis=1)

# Convert 'Stat1 Value', 'Stat2 Value', and 'Stat4 Value' to float64 in new_items
new_items['Stat1 Value'] = new_items['Stat1 Value'].astype('float64')
new_items['Stat2 Value'] = new_items['Stat2 Value'].astype('float64')
new_items['Stat4 Value'] = new_items['Stat4 Value'].astype('float64')

# Preprocess new items data
new_items_preprocessed = preprocessor.transform(new_items)

# Print columns in the original data but not in new_items
missing_cols = set(items.columns) - set(new_items.columns)
print(f"Columns in original data but missing in new_items: {missing_cols}")

# Print columns in new_items but not in the original data
extra_cols = set(new_items.columns) - set(items.columns)
print(f"Columns in new_items but not in original data: {extra_cols}")

# Check for mismatched data types
for col in set(new_items.columns).intersection(set(items.columns)):
    if items[col].dtype != new_items[col].dtype:
        print(f"Type mismatch: {col} is {items[col].dtype} in original data and {new_items[col].dtype} in new_items")

# Predict prices
predicted_prices = model.predict(new_items_preprocessed)

# Add the predicted prices to the new_items DataFrame
new_items['Predicted Price'] = predicted_prices

# Print the predicted prices
print(new_items)


# Save the new_items DataFrame to a new CSV file
new_items.to_csv('priced_items.csv', index=False)

print('done')

