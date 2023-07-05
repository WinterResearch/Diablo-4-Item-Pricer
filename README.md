# D4 Item Pricer

![d4_pricing](https://github.com/WinterResearch/Diablo-4-Item-Pricer/assets/95959417/1572ae84-83be-485b-98bd-6f3173995bfe)

Pricing Diablo 4 Items for Buying / Selling 

Run `gui.py` to launch GUI for adding items / pricing items.

Click `Submit` to add item to `items.csv` (Historical Sold Items).

Clicking `Add to pricing options` will send item to `price_option.csv` (For quoting item price / value).

Note, when pricing an item, you will not fill out `Sold Value`. If it's a historically sold item you're adding for training, fill out `Sold Value`.

Once you have added an item to price (present in price_option.csv), run model.py to produce output. Will generate priced_items.csv. Clear both csvs when necessary

DPS will correspond to DPS / Armor / Item level, whichever is present on the item in that order.

`Sold Value` is expressed in millions (sold value: 5 = 5,000,000).

To include stat types for items, modify `main_stat_types` (present in both `gui.py` and `model.py`, make them mirror each other).

The more items you add to the `items.csv` database, the better the tool will be at pricing items.

The current CSV is loaded with Sorceress items. To clear these options, empty the `items.csv`, leave the header. Modify `main_stat_types` for your class stat priorities.

You will need some level of data before the tool will begin working, so intitially start by adding various historically sold items.

Inteded to be used within the diablo 4 community discord marketplace 

![d4_pricing2](https://github.com/WinterResearch/Diablo-4-Item-Pricer/assets/95959417/99f5a566-b37f-4b75-bf2c-477defd41bca)
