from pyproj import Transformer
from bng import to_osgb36

crs_british = 'EPSG:27700'
crs_wgs84 = 'EPSG:4326'

transformer = Transformer.from_crs(crs_british, crs_wgs84)

# for checking conversions, note NG869576
# is approx 57.5585963,-5.563975
os_numeric = to_osgb36("NG869576")
transformer.transform(*os_numeric)

reverser = Transformer.from_crs(crs_wgs84, crs_british)

from_osgb36(reverser.transform(*c))