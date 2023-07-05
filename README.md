# D4 Item Pricer
 Pricing Diablo 4 Items for Buying / Selling \n
 Run gui.py to launch gui for adding items / pricing items
 Click submit to add item to items.csv (Historical Sold Items)
 Clicking add to pricing options will send item to price_option.csv (For quoting item price / value)
 Note, when pricing an item, you will not fill out Sold Value. If its a historically sold item you're adding for training, fill out Sold Value.
 DPS will correspond to DPS / Armor / Item level, whichever is present on the item in that order
 Sold Value is expressed in millions (sold value: 5 = 5,000,000)
 To include stat types for items, modify main_stat_types (present in both gui.py and model.py, make them mirror eachother)
 The more items you had to the items.csv database, the better the tool will be at pricing items
 The current csv is loaded with Sorcress items. To clear these options, empty the items.csv, leave the header. Modify main_stat_types for your class stat priorities
