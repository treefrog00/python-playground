from math import radians, sin, cos, sqrt, atan2


def lat_lon_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate distance between two points
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


# def calculate_distance_from_lat_lons(records):
#     # Get all data records that contain position data
#     lat_lons = []
#     for record in records:
#         if record.has_field('position_lat') and record.has_field('position_long'):
#             lat = record.get_value('position_lat') / ((2**32) / 360)
#             lon = record.get_value('position_long') / ((2**32) / 360)
#             lat_lons.append((lat, lon))

#     # Calculate total distance
#     total_distance = 0
#     for i in range(len(lat_lons)-1):
#         lat1, lon1 = lat_lons[i]
#         lat2, lon2 = lat_lons[i+1]
#         total_distance += lat_lon_distance(lat1, lon1, lat2, lon2)

#     return total_distance
