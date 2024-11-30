"""
 PYMRIO Documentation : https://pymrio.readthedocs.io/_/downloads/en/latest/pdf/
"""

# All the import statements.
# maybe, by the end, we only end up using only a few of them
import pymrio
import zipfile
import os
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import plotly.express as px
import country_converter as coco
from urllib.request import urlopen
import json
import numpy as np
from plotly.io import to_html
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse


def make_it_exist(target_folder: str, which_year: int, exio_system: str) -> pd.DataFrame:
    """
    inputs :
        target_folder : takes in the string of the path where you want to check for EXIOBASE files
                        dowlnload if they don't exist
        which_year : takes in the integer of whichever year of EXIOBASE you want to check/download
        exio_system (optional): has to be either "ixi" or "pxp"

    output :
        exio3 : IOSystem with the parsed exiobase 3 data
    """

    if "IOT_" + str(which_year) + "_" + exio_system + ".feather" not in os.listdir(target_folder):
        print(f"Downloading EXIOBASE IO tables for the year : {which_year}")
        pymrio.download_exiobase3(storage_folder = target_folder, system = exio_system, years = which_year)
        print(f'Extracting EXIOBASE IO table for year : {which_year}')
        exio3 = pymrio.parse_exiobase3(os.path.join(target_folder, "IOT_" + str(which_year) + "_" + exio_system + ".zip"))
        region = list(exio3.get_regions())
        ghg_map = pd.DataFrame(0, index=region, columns=region)

        for i in ghg_map.columns:
            for j in ghg_map.index:
                ghg_map.loc[i, j] = int(exio3.Z.loc[i, j].sum().sum())
        print("Saving Feather File...")
        ghg_map.to_feather(os.path.join(target_folder, "IOT_" + str(which_year) + "_" + exio_system + ".feather"))
        print("Deleting zip file...")
        os.remove(os.path.join(target_folder, "IOT_" + str(which_year) + "_" + exio_system + ".zip"))
        print("Found File! Plotting...")
        return ghg_map
    print("Found File! Plotting...")
    return pd.read_feather(os.path.join(target_folder, "IOT_" + str(which_year) + "_" + exio_system + ".feather"))

def make_ghg_map(target_folder: str, which_year: int, exio_system: str = "ixi", origin_country: str | None = None, target_country: str | None = None) -> px.choropleth_map:
    """
    inputs :
        target_folder : takes in the **string** of the path where you want to check for EXIOBASE files
                        dowlnload if they don't exist
        which_year : takes in the **integer** of whichever year of EXIOBASE you want to check/download
        exio_system (optional): has to be either "ixi" or "pxp"
        origin_country : None, or has to be a **string** of country code (exiobase format)
                         If you want to track ghg emissions from a specific country to the RoW

        target_country : None, or has to be **string** of country code (exiobase format)
                         If you want to track ghg emissions from RoW to a specific country
    """
    ghg_map = make_it_exist(target_folder=exio3_folder, which_year=which_year, exio_system=exio_system)
    if origin_country == None and target_country == None:
        region_data = [int(ghg_map.iloc[i, i]) for i in range(min(len(ghg_map.index), len(ghg_map.columns)))]
        region_df = pd.DataFrame(data = {'region' : ghg_map.columns, 'emissions' : region_data})
    elif origin_country != None and target_country == None:
        row_index = ghg_map.index.get_loc(origin_country)
        region_data = [int(ghg_map.iloc[row_index, i]) for i in range(len(ghg_map.columns))]
        region_df = pd.DataFrame(data = {'region' : ghg_map.columns, 'emissions' : region_data})
    elif origin_country == None and target_country !=None:
        column_index  = ghg_map.columns.get_loc(target_country)
        region_data = [int(ghg_map.iloc[i, column_index]) for i in range(len(ghg_map.index))]
        region_df = pd.DataFrame(data = {'region' : ghg_map.index, 'emissions' : region_data})
    else:
        column_index = ghg_map.columns.get_loc(origin_country)
        row_index  = ghg_map.index.get_loc(target_country)
        region_data = [int(ghg_map.iloc[column_index, row_index])]
        region_df = pd.DataFrame(region_data, index=[origin_country], columns=[target_country])

    cc = coco.CountryConverter()
    country_dict = cc.get_correspondence_dict('EXIO3', 'ISO3')

    new_dict_country = []
    new_dict_emission = []
    for k in country_dict.keys():
        emission = region_df.loc[region_df['region'] == k].iloc[0, 1]
        for items in country_dict.get(k):
            new_dict_country.append(items)
            new_dict_emission.append(emission)

    new_emissions_df = pd.DataFrame({'country':new_dict_country, 'emission':new_dict_emission})
    new_emissions_df['emission_log'] = np.log(new_emissions_df['emission'])

    with urlopen('https://raw.githubusercontent.com/johan/world.geo.json/refs/heads/master/countries.geo.json') as response:
        countries = json.load(response)

    ######THIS SECTION FOR TESTING ONLY!!!!!
    if which_year%2==0:
        fig = px.choropleth_map(new_emissions_df,
                                   geojson=countries,
                                   locations='country',
                                   color='emission_log',
                                   color_continuous_scale="icefire",
                                   map_style="carto-positron",
                                   zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                   opacity=0.5
                                  )
    else:
        fig = px.choropleth_map(new_emissions_df,
                                   geojson=countries,
                                   locations='country',
                                   color='emission_log',
                                   color_continuous_scale="Viridis",
                                   map_style="carto-positron",
                                   zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                                   opacity=0.5
                                  )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


exio3_folder = "/Users/saatweek/Documents/App/EXIO3" # set up a folder within which you'll store all the datasets'
which_year = 2017 ## can be an integer, or a list of integers (but use int for now)
exio_system = 'ixi' ## choose between 'ixi' and 'pxp'

fig = make_ghg_map(exio3_folder, which_year, exio_system, target_country=None)
# fig.show()

app = FastAPI()  # Create a FastAPI instance
@app.get("/")
async def root():
    plot_div = to_html(fig, full_html=False)
    # Create the full HTML document
    html_content = f"""
        <html>
            <head>
                <title>Emission Plot</title>
            </head>
            <body>
                {plot_div}
            </body>
        </html>
        """
    return HTMLResponse(content=html_content)
@app.get("/{year}")
async def plot_year(year : int):
    exio3_folder = "/Users/saatweek/Documents/App/EXIO3"
    which_year = year
    exio_system = 'ixi' ## choose between 'ixi' and 'pxp'
    fig = make_ghg_map(exio3_folder, which_year, exio_system)
    plot_div = to_html(fig, full_html=False)
    html_content = f"""
        <html>
            <head>
                <title>Emission Plot</title>
            </head>
            <body>
                {plot_div}
            </body>
        </html>
        """
    return HTMLResponse(content=html_content)
