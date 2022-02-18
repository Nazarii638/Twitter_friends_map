"""Program creates the HTML map of friends' location by using the JSON file"""
import json
from functools import lru_cache
import folium
from geopy.geocoders import Nominatim, ArcGIS


arcgis = ArcGIS(timeout=10)
nominatim = Nominatim(timeout=10, user_agent="justme")
geocoders = [arcgis, nominatim]


def main():
    """
    The main function that gathers the information from JSON file,
    after that launches another function that creates the map.
    """
    data = reading_the_file() # dictionary
    creating_map(data)


def reading_the_file(path="info.json"):
    """
    The function opens, reads and returns the dictionary from JSON file.
    >>> type(reading_the_file())
    <class 'dict'>
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def creating_map(data: dict):
    """
    The function takes the data(dictionary), works with it. During that
    launches the function that finds the coordinates for the location.
    After that function creates the HTML map. Every marker has the following
    information: nickname of user in twitter and his location.
    """
    user_map = folium.Map(location=[0, 0], zoom_start=1)

    html = """<h4>Friend information:</h4>
    Username: {},<br>
    Place: {}
    """

    friends_markers = folium.FeatureGroup(name="Friends")

    for num in range(len(data["users"])):
        try:
            friend_info = list(getting_the_loc(data["users"][num]["location"]))
            friend_info.append(data["users"][num]["screen_name"])
        except TypeError:
            continue
        iframe = folium.IFrame(html=html.format(friend_info[-1],
        friend_info[-2]), width=300, height=100)

        friends_markers.add_child(folium.Marker(location=[friend_info[0],friend_info[1]],
        popup=folium.Popup(iframe), icon=folium.Icon(color="red")))
        user_map.add_child(friends_markers)

    user_map.add_child(folium.LayerControl())
    user_map.save("templates/friends_map.html")


@lru_cache(maxsize=None)
def getting_the_loc(address: str):
    """
    The function with geocode module finds and returns
    the coordinates and the city.
    >>> getting_the_loc('Chicago, Illinois')
    (41.884250000000065, -87.63244999999995, 'Chicago, Illinois')
    """
    i = 0
    try:
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude, location.address
        i += 1
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude, location.address
    except AttributeError:
        return None
