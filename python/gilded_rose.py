# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            # Handle the Conjured items first, to avoid double degradation issues
            if "Conjured" in item.name:
                degrade_value = 2

                if item.sell_in <= 0:
                    degrade_value *= 2  # After sell date, degrade twice as fast

                item.quality = max(0, item.quality - degrade_value)
                item.sell_in -= 1  # Reduce the sell-in days
                continue  # Skip rest of logic for conjured items

            # Logic for other items.
            if (
                item.name != "Aged Brie"
                and item.name != "Backstage passes to a TAFKAL80ETC concert"
            ):
                if item.quality > 0:
                    if item.name != "Sulfuras, Hand of Ragnaros":
                        item.quality -= 1
            else:
                if item.quality < 50:
                    item.quality += 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality += 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality += 1

            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in -= 1

            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality -= 1
                    else:
                        item.quality = 0  # Backstage passes drop to 0 after concert
                else:
                    if item.quality < 50:
                        item.quality += 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
