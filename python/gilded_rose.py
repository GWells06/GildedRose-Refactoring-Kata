# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        """Handle updates for the quality of the various items."""
        for item in self.items:
            # Skip Sulfuras, Hand of Ragnaros since there is no change in quality or sell-in for Sulfuras.
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue

            # Handle the Conjured items first in order the to avoid double degradation issues
            if "Conjured" in item.name:
                self.update_conjured(item)
            else:
                self.update_non_conjured(item)

    def update_conjured(self, item):
        """Update the conjured item with its special degardation values."""
        degrade_value = 2
        if item.sell_in <= 0:
            degrade_value *= 2  # After the sell date, degrade twice as fast
        item.quality = max(0, item.quality - degrade_value)
        item.sell_in -= 1  # Reduce the sell-in days

    def update_non_conjured(self, item):
        """Update any non-conjured items."""
        # Handle Aged Brie and Backstage passes
        if item.name == "Aged Brie":
            self.update_aged_brie(item)
        elif item.name == "Backstage passes to a TAFKAL80ETC concert":
            self.update_backstage_passes(item)
        else:
            self.update_normal_item(item)

        # Update the sell-in value
        item.sell_in -= 1

        # Once the sell-in date has passed, degrade the quality faster.
        if item.sell_in < 0:
            if item.name == "Aged Brie":
                self.update_aged_brie(item, after_sell_by=True)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                item.quality = 0  # Backstage passes drop to 0 after concert
            else:
                item.quality = max(0, item.quality - 1)

    def update_aged_brie(self, item, after_sell_by=False):
        if after_sell_by:
            item.quality = min(50, item.quality + 1)
        elif item.quality < 50:
            item.quality += 1

    def update_quantity(self, item):
        if item.sell_in < 6:
            item.quality = min(50, item.quality + 3)
        elif item.sell_in < 11:
            item.quality = min(50, item.quality + 2)
        elif item.quality < 50:
            item.quality += 1

    def update_normal_item(self, item):
        if item.quality > 0:
            item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
