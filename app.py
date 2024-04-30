import streamlit as st 
import numpy as np
import pandas as pd
import time 
import folium
import random
from typing import Iterable
from streamlit_folium import st_folium
from folium.plugins import Draw

from helper_script import DataGenerator

# -------------------------------------------------

def clear_fg():
    """Function to clear map"""
    st.session_state.locations=[]
    st.session_state.markers =[]

    fg = folium.FeatureGroup()

def add_marker():
    """Function to add marker to the map"""

    icon = folium.CustomIcon("cow.png", icon_size=(30, 30))
    location = st.session_state.get("locations")
    
    if location:
       location = location[-1] # Slice lcoation if location list not empty
       if not st.session_state.added_locs or (len(st.session_state.added_locs[-1]) > 1 and location != st.session_state.added_locs[-1]):
            animal_id = random.choice(["A","X","C"]) + str(random.randint(0, 1000)) + random.choice(["L","F","X"])
            st.session_state.added_locs.append(location)
            st.session_state.animal_id.append(animal_id)
            marker = folium.Marker(location=[location["lat"], location["lng"]],
                               tooltip=f"Animal_ID: {animal_id}",
                               icon=icon)
            st.session_state.markers.append(marker)
       else: pass
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

def recenter_map():
    """Recenter map based on a series of locations.
    locations (List(Dict:{"lat":float,"lng":float}))
     """
    locations = st.session_state.get("added_locs")

    if locations:
        center = pd.DataFrame(locations).mean().to_dict()
        st.session_state["center"] = center

    else: pass

@st.cache_data
def create_df(*args,**kwargs):
    """ Function to call the generator and create the df.
    *args

    list_of_animals [Array] : Index of Animals to generate data from.
    locations [Array((Tuple), ...)] : Locations associoated with index animals
    n_samples = number of data points to generate per animal.
    """

    list_of_animals, locations, *_ = args 

    variables = kwargs.get("variables",None)                        # extract variables 
    n_samples = kwargs.get("n") or kwargs.get("n_rows") or 1        # extract n_rows
    p = kwargs.get("p") or kwargs.get("prob") or 0.1                # extract probability

    if list_of_animals and locations :

        generator = DataGenerator(list_of_animals,locations,
                                  n=n_samples,
                                  variables=variables,
                                  p=p)

        return generator.generate_df(n_samples)
    
    else: return st.warning("No list of ids has been passed!")

def generate_new_df():
    st.session_state.generate_new_df = True
# -------------------------------------------------

if "df" not in st.session_state:
    st.session_state.df = None              # var to store the df
if "animal_id" not in st.session_state:
    st.session_state.animal_id = []         # list of animal to be indexed
if "markers" not in st.session_state:
    st.session_state.markers = []           # object to store folium marker objects
if "locations" not in st.session_state:
    st.session_state.locations = []         # object to store last clicked locations on the mapp
if "added_locs" not in st.session_state:
    st.session_state.added_locs = []        # object to store locations that succesfully have been added to map
if "center" not in st.session_state:
    st.session_state["center"] = {"lat":25.5503534,"lng":-99.9710282}  # object to pass to center arg in folium map
if "zoom" not in st.session_state:
    st.session_state["zoom"] = 13                                      # object to pass to zoom arg in folium map         
if "generate_new_df" not in st.session_state:
    st.session_state["generate_new_df"] = False                        # object to use the button of the form correctly

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
            st.button("Add to Map ⭕",on_click=add_marker,key="add_to_map_button")
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

    if st.session_state.add_to_map_button:
        st.info("Added a new marker to the map",icon="ℹ️")


with columns[1]:

    var = [
           "temperature",
           "humidity",
           "hours_of_sleep"
           "Heart Rate(bpm)",
           "speed(steps/hour)",
           "time_spent_eating",
           "breathing Rate(breaths/min)",]
    
    with st.form("key_form"):

        st.multiselect("Select the variables to get into the package ",
                   options=var,default=var,
                   help="Select the variables to randomly generate for the animal.",
                   key="Variables")

        st.slider("Randomness 💫",
              help="The more this value increases, the more random are the data between the animals.",
              min_value = 0.1, max_value=1.0,value = 0.1,step=0.1,
              key="probs")
        
        st.slider("Number of Samples", help="Number of samples per ID to generate",
            min_value=1,max_value=200,value=10,step=10,key="N_samples")
        
        st.write('Press submit to generate.')

        submit = st.form_submit_button(label='Generate New Data ✅',on_click=generate_new_df)
        
    #st.write(st.session_state.get("Variables"))    
if st.session_state.get("generate_new_df") and st.session_state.get("animal_id") and st.session_state.get("added_locs"):
    with st.spinner("Creating dataset"):

        time.sleep(2)
        
        st.session_state.df = create_df(st.session_state.animal_id, st.session_state.added_locs,
                                        variables =st.session_state.get("Variables"),
                                        n_rows=st.session_state.get("N_samples"),
                                        p=st.session_state.get("probs"))

        st.data_editor(st.session_state.df,
                       column_config={"datetime":st.column_config.DatetimeColumn(
                           format="D MMM YYYY, h:mm a"
                       )}) # print the new df

        st.session_state.generate_new_df = False # set to false again 

elif st.session_state.get("df") is not None:

        st.data_editor(st.session_state.df,
                       column_config={"datetime":st.column_config.DatetimeColumn(
                           format="D MMM YYYY, h:mm a"
                       )}) # print the new df

