import folium
import pandas as pd

# Create a Map Object
map = folium.Map(location=[38,-92.09], zoom_start=4)

# Import Data
volcano_df = pd.read_csv('Volcanoes.txt')
lat = list(volcano_df['LAT'])
lon = list(volcano_df['LON'])
elev = list(volcano_df['ELEV'])

#function to color code the markers 

def color_code(elevation):
    if elevation < 1_000:
        return 'green'
    elif 1_000 <= elevation <3_000:
        return 'orange'
    else:
        return 'red'

# Create a Feature Group
feature_group_volcanoes = folium.FeatureGroup(name='Volcanes')

# Iterate through the data
for lt, ln, el in zip(lat,lon, elev):
    feature_group_volcanoes.add_child(folium.CircleMarker(
        location=(lt, ln),
        popup = str(el)+'m',
        radius=8,
        fill_color = color_code(el),
        color = 'grey',
        fill_opacity = 0.5))

#Add a Second feature_group
feature_group_population = folium.FeatureGroup(name='Population')

feature_group_population.add_child(folium.GeoJson(data = open('world.json',
    mode = 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<1_000_000 
    else 'orange' if 1_000_000  <= x['properties']['POP2005']<20_000_000 
    else 'red'}))
    

#Add Object to the Map 
map.add_child(feature_group_population)
map.add_child(feature_group_volcanoes)

#Add Some Map Controls 
map.add_child(folium.LayerControl())

# Save the Map
map.save('map_1.html')