import streamlit as st 
import numpy as np
import pandas as pd
import time 
import folium
import random
from typing import Iterable
from streamlit_folium import st_folium
from folium.plugins import Draw

# -------------------------------------------------

def clear_fg():
    """Function to clear map"""
    st.session_state.locations=[]
    st.session_state.markers =[]

    fg = folium.FeatureGroup()
def add_marker():
    """Function to add marker to the map"""
    
    location = st.session_state.get("locations")[-1]

    if len(st.session_state.added_locs[-1])>1 and location != st.session_state.added_locs[-1]:
        icon = folium.CustomIcon("cow.png", icon_size=(30, 30))
        animal_id = random.choice(["A","X","C"])+str(random.randint(0,1000))+random.choice(["L","F","X"])
        st.session_state.added_locs.append(location) 
        st.session_state.animal_id.append(animal_id)
        if location:
            marker = folium.Marker(location=[location["lat"],location["lng"]],
                                tooltip = f"Animal_ID : {animal_id}", 
                                icon=icon)
            st.session_state.markers.append(marker)
    else: pass

def change_zoom():

    st.session_state.zoom = map.get("zoom")

    zoom_list = [5,10,12,14,16,17]

    current_zoom = st.session_state.zoom

    if current_zoom in zoom_list:
        index = zoom_list.index(current_zoom)
        if index < len(zoom_list) - 1:
            new_zoom = zoom_list[index + 1]
            st.session_state.zoom = new_zoom
        else: st.session_state.zoom = zoom_list[0]
    else: 
        closest_zoom = min(zoom_list, key=lambda x: abs(x - current_zoom))
        st.session_state.zoom = closest_zoom
    st.info("Added a new marker to the map")

def recenter_map():
    """Recenter map based on a series of locations.
    locations (List(Dict:{"lat":float,"lng":float}))
     """
    locations = st.session_state.get("added_locs")

    if locations:
        center = pd.DataFrame(locations).mean().to_dict()
        st.session_state["center"] = center

    else: pass

# def add_last_clicked_to_map(map_dict:Dict,feature_group):

#     last_loc_clicked =  map_dict.get("last_clicked")

#     if last_loc_clicked:
#         marker = folium.Marker(location=[values for values in last_loc_clicked.values()],
#                            popup = time.time(),icon=folium.Icon(color="blue"))
    
#         feature_group.add_child(marker)
#     else: pass
# -------------------------------------------------

if "df" not in st.session_state:
    st.session_state.df = None
if "animal_id" not in st.session_state:
    st.session_state.animal_id = []
if "markers" not in st.session_state:
    st.session_state.markers = []
if "locations" not in st.session_state:
    st.session_state.locations = []
if "added_locs" not in st.session_state:
    st.session_state.added_locs = []
if "center" not in st.session_state:
    st.session_state["center"] = {"lat":25.5503534,"lng":-99.9710282}
if "zoom" not in st.session_state:
    st.session_state["zoom"] = 13

#Draw(export=True).add_to(m)
# -------------------------------------------------

st.set_page_config(layout="wide")
st.title("Sensor Simulation App")

columns = st.columns([2,1])

with columns[0]:

    with st.expander("Map 🗺",expanded=True):

        b_cols = st.columns([1,1,1,1,1],gap="small")
        with b_cols[0]:
            st.button("Recenter map 📍",on_click=recenter_map)
        with b_cols[1]:
            st.button("Change Zoom 🔬", on_click= change_zoom)
        with b_cols[2]:
            st.button("Add to Map ⭕",on_click=add_marker)
        with b_cols[3]:
            st.button("Clear Map ❌", on_click=clear_fg)                

        m = folium.Map(location=[19.42631,-99.136161], zoom_start=8)
        fg = folium.FeatureGroup(name="markers")

        for marker in st.session_state.markers:
            fg.add_child(marker)

        map = st_folium(
        m,
        center=st.session_state["center"],
        zoom=st.session_state["zoom"],
        key="new",
        feature_group_to_add=fg,
        height=400,
        width=900,
    )

    last_value_loc = map.get("last_clicked")

    if len(st.session_state.locations)>1 and st.session_state.locations[-1] == last_value_loc:
        pass
    elif last_value_loc: 
        st.session_state.locations.append(last_value_loc)
        #st.write(st.session_state.locations)

    # if st.session_state.map_dict:
    #     locs= [points["geometry"]["coordinates"] for points in st.session_state.map_dict]
    #     st.session_state.locations = [{"lng":i[0],"lat":i[1]} for i in locs]
    #st.write(st.session_state.locations)

    #st.write(st.session_state.center)
    #st.session_state.last_pos_clicked = map.get("last_clicked")

    #text_a.value = st.session_state.last_pos_clicked

    #st.write(st.session_state.last_pos_clicked)
        
    #add_marker_to_map(map,feature_group=fg)

with columns[1]:

    #st.write(st.session_state.locations)

    var = [
           "temperature",
           "datetime",
           "humidity",
           "hours_of_sleep"
           "Heart Rate(bpm)",
           "speed(steps\hour)",
           "time_spent_eating",
           "Breathing Rate(breaths/min)"]

    st.multiselect("Select the variables to get into the package ",
                   options=var,
                   help="Select the variables to randomly generate for the animal.",
                   key="Variables")

    st.slider("Randomness 💫",
              help="The more this value increases, the more random are the data between the animals.",
              key="probs")
    
    st.button("Generate✅")

    #st.write(map)

