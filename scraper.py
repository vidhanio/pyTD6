from mediawiki import MediaWiki
from wikitables import import_tables

bloons_wiki = MediaWiki(url="https://bloons.fandom.com/api.php")

bomb = bloons_wiki.page(pageid=2070)

print(bomb.images)

tables = import_tables()