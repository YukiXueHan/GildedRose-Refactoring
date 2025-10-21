# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemUpdateStrategy:
    
    def update(self, item):
        self._update_quality(item)
        self._update_sell_in(item)
        self._update_quality_after_sell_date(item)
    
    def _update_quality(self, item):
        pass
    
    def _update_sell_in(self, item):
        item.sell_in -= 1
    
    def _update_quality_after_sell_date(self, item):
        pass
    
    def _increase_quality(self, item, amount=1):
        item.quality = min(50, item.quality + amount)
    
    def _decrease_quality(self, item, amount=1):
        item.quality = max(0, item.quality - amount)


class NormalItemStrategy(ItemUpdateStrategy):
    
    def _update_quality(self, item):
        self._decrease_quality(item)
    
    def _update_quality_after_sell_date(self, item):
        if item.sell_in < 0:
            self._decrease_quality(item)


class AgedBrieStrategy(ItemUpdateStrategy):
    
    def _update_quality(self, item):
        self._increase_quality(item)
    
    def _update_quality_after_sell_date(self, item):
        if item.sell_in < 0:
            self._increase_quality(item)


class BackstagePassStrategy(ItemUpdateStrategy):
    
    def _update_quality(self, item):
        self._increase_quality(item)
        
        if item.sell_in < 11:
            self._increase_quality(item)
        
        if item.sell_in < 6:
            self._increase_quality(item)
    
    def _update_quality_after_sell_date(self, item):
        if item.sell_in < 0:
            item.quality = 0


class SulfurasStrategy(ItemUpdateStrategy):
    
    def _update_quality(self, item):
        pass  # Quality never changes
    
    def _update_sell_in(self, item):
        pass  # sell_in never changes
    
    def _update_quality_after_sell_date(self, item):
        pass  # No change after expiration


class GildedRose(object):

    def __init__(self, items):
        self.items = items
    
    def _get_strategy(self, item):
        strategies = {
            "Aged Brie": AgedBrieStrategy(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy(),
            "Sulfuras, Hand of Ragnaros": SulfurasStrategy(),
        }
        return strategies.get(item.name, NormalItemStrategy())

    def update_quality(self):
        for item in self.items:
            strategy = self._get_strategy(item)
            strategy.update(item)