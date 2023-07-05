# D4 Item Pricer

Pricing Diablo 4 Items for Buying / Selling 

Run `gui.py` to launch GUI for adding items / pricing items.

Click `Submit` to add item to `items.csv` (Historical Sold Items).

Clicking `Add to pricing options` will send item to `price_option.csv` (For quoting item price / value).

Note, when pricing an item, you will not fill out `Sold Value`. If it's a historically sold item you're adding for training, fill out `Sold Value`.

DPS will correspond to DPS / Armor / Item level, whichever is present on the item in that order.

`Sold Value` is expressed in millions (sold value: 5 = 5,000,000).

To include stat types for items, modify `main_stat_types` (present in both `gui.py` and `model.py`, make them mirror each other).

The more items you add to the `items.csv` database, the better the tool will be at pricing items.

The current CSV is loaded with Sorceress items. To clear these options, empty the `items.csv`, leave the header. Modify `main_stat_types` for your class stat priorities.
