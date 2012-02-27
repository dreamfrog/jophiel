from scrapy.statscol import DummyStatsCollector

from scrapy.utils.misc import load_object
from scrapy import settings
# if stats are disabled use a DummyStatsCollector to improve performance
if settings['STATS_ENABLED']:
    stats = load_object(settings['STATS_CLASS'])()
else:
    stats = DummyStatsCollector()
