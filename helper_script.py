

import pandas as pd
import random
from scipy.stats import poisson,bernoulli
from datetime import datetime, timedelta
 
class DataGenerator:

    def __init__(self, *args,**kwargs):

        self.unique_ids, self.locations = args # unpack indexes and locations

        self.map_dict = dict(zip(self.unique_ids,self.locations)) # generate a dict to map id to location.

        self.variable_names = [
                "temperature",
                "humidity",
                "hours_of_sleep",
                "Heart Rate(bpm)",
                "speed(steps/hour)",
                "time_spent_eating",
                "breathing Rate(breaths/min)",
            ]
        
        self.kwargs = kwargs # make the kwargs avalable to all the methods

        random.seed(random.randint(0,1000)) # set seed

        variables = kwargs.get("variables") # selected variables
        if variables:
            self.variable_names = [var for var in self.variable_names if var in variables ] # filter the selected ones

        self.variable_names.insert(0,"datetime")            # insert critical var
        self.variable_names.insert(1,"location")  # insert critical var
        self.variable_names.insert(2,"health_condition")    # insert critical var
        
    def generate_data_for_id(self, unique_id, n,**kwargs):
        """Function to generate the data based on one ID."""

        self.previous_values=  {var: None for var in self.variable_names}

        p = kwargs.get("p") or self.kwargs.get("p")
        if not p:
            p=0.1 

        data_points = []
        for _ in range(n):
            data_point = {"id": unique_id}
            for var in self.variable_names:
            
                if var == "datetime":
                    if self.previous_values[var] is None:
                        data_point[var] = datetime.now() - timedelta(days=n)
                    else:
                        data_point[var] = self.previous_values[var] + timedelta(days=1)
                elif var == "health_condition":
                    if self.previous_values[var] is None:
                        data_point[var] = bernoulli.rvs(p=0.8) # let this stay fixed
                    else: data_point[var] = self.previous_values[var]
                elif var == "location":
                    if self.previous_values[var] is None:
                        data_point[var] = self.map_dict[unique_id] # let this stay fixed
                    else: 
                        data_point[var] = self.previous_values[var]
                        data_point[var]["lat"] = self.previous_values[var]["lat"] + random.uniform(-p,p)
                        data_point[var]["lng"] = self.previous_values[var]["lng"] + random.uniform(-p,p)
                else:
                    if self.previous_values[var] is None:
                        data_point[var] = random.uniform(35.0, 40.0) if "temperature" in var else random.gauss(50,15)
                    else:
                        delta = random.choice([-1,1])*poisson.rvs(5*p)
                        data_point[var] = max(0, self.previous_values[var] + delta)  # Ensure non-negative values
                self.previous_values[var] = data_point[var]
            data_points.append(data_point)
        
        return pd.DataFrame(data_points)

    def generate_df(self, n_per_id):
        dfs = []
        for unique_id in self.unique_ids:
            df = self.generate_data_for_id(unique_id, n_per_id)
            dfs.append(df)
        return pd.concat(dfs, ignore_index=True)