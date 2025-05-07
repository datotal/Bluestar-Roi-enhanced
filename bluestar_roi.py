import pandas as pd
import numpy as np
import streamlit as st
import os
import folium
import plotly.express as px
from geopy.distance import geodesic
import warnings
warnings.filterwarnings("ignore", message=".*SettingWithCopyWarning.*")
from streamlit_folium import folium_static
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import zipfile
import re

#setting page icon
st.set_page_config(
    page_title="Prospect Analysis",
    page_icon="🌙",
   
    initial_sidebar_state="auto",
)


st.title("PROSPECT RECOMMENDATIONS")
st.header("Time Frame 12 Months ")
st.subheader("Shipment Count 456,720")
st.subheader("Total Shipments Excluding Outliers 456,720")
st.subheader("Outliers 0 (0.0%)")
st.subheader("Total Spend $14,812,415")
st.subheader("Total Savings $1,251,921 (8%)")

#savings chart
name= ["Zone Savings","LTL To Parcel Mode Optimization","Parcel To LTL Mode Optimization",'LTL to TL Mode Optimization',"Parcel To LTL Consolidation",'LTL To TL Consolidation','TL vs TL DAT Rates - Savings','LTL To TL Consolidation Weekwise','Potential Warehouse Savings']
savings_total= [20212,44101,9257,10070,48126,7698,541459,329573,241425]

# savings chart
fig = px.pie(names=name,values=savings_total,hole=0.5,color_discrete_sequence=px.colors.sequential.Sunset )
fig.update_layout(title='Savings Chart',title_x=0.5)
st.plotly_chart(fig)

#Top carrier
st.subheader("Number Of Carriers Utilized: 20")
carriercharge = pd.read_excel(r"Bluestar_ROI_Carriername_charge.xlsx")
carriers_list=carriercharge.groupby("CarrierName").aggregate({"Charge":'sum'}).reset_index().sort_values(by="Charge",ascending=False).head(10)
fig=px.bar(carriers_list,x="Charge",y="CarrierName", title='Top Carriers')
fig.update_yaxes(categoryorder='total ascending')
fig.update_xaxes(title_text="Spend")
fig.update_yaxes(title_text="Carrier")
st.plotly_chart(fig)

#predicted warehouses
warehousedf = pd.read_excel(r"Bluestar_ROI_warehouse.xlsx")
shipper_zips_of_interest = ["41048", "53142", "N8W0A7", "90630", "54942"]  # warehouse location
warehouse = warehousedf[warehousedf["sZip"].isin(shipper_zips_of_interest)]
# print("warecount",warehouse.shape[0])
warehouse_list = warehouse.groupby("sState").agg(
    total_spend=("Charge", 'sum'),
    shipment_count=("Charge", 'count')
).reset_index().sort_values(by='total_spend', ascending=False)
fig = px.bar(
    warehouse_list,
    x='total_spend',
    y="sState",
    hover_data={'total_spend': ':.2f', 'shipment_count': True},
    title='Warehouse'
)
fig.update_yaxes(categoryorder='total ascending')
fig.update_xaxes(title_text="Spend ($)")
fig.update_yaxes(title_text='Warehouse Location')
st.plotly_chart(fig)



# #Mode chart
modedf = pd.read_excel(r"Bluestar_ROI_Mode.xlsx")
mode=modedf.groupby('Mode').aggregate({"Charge":'sum'}).reset_index().sort_values(by="Charge",ascending=False)
# print(mode)
fig=px.bar(mode,x="Charge",y='Mode', title='Spend By Mode')
fig.update_yaxes(categoryorder='total ascending')
fig.update_xaxes(title_text="Spend")
fig.update_yaxes(title_text='Mode')
st.plotly_chart(fig)



# Zones
st.subheader('Air Shipping in Zone 2 & 3 is Costing You — Ground is the Smarter Move')
zonedf = pd.read_csv(r"Zonesdf.csv")
st.dataframe(zonedf, use_container_width=True)
st.subheader("Total Spend $164,087")
st.subheader("Total Savings $20,212")


# LTL To Parcel Mode Optimization

st.header("LTL To Parcel Mode Optimization")
st.subheader("Based On Weight We Recommend 353 Shipments Can Be Shipped via PARCEL Ground")
ltlparceldf = pd.read_csv(r"LTL To Parcel Mode Optimization.csv")
st.dataframe(ltlparceldf, use_container_width=True)
st.subheader("Total Spend $131,745")
st.subheader("Total Estimated Spend $87,288")
st.subheader("Total Savings $44,101")

# Parcel To LTL Mode Optimization 

st.header("Parcel To LTL Mode Optimization")
st.subheader("Based On Weight We Recommend 10 Shipements Can Be Shipped via LTL")
parcelltldf = pd.read_csv(r"Parcel To LTL Mode Optimization.csv")
st.dataframe(parcelltldf, use_container_width=True)
st.subheader("Total Spend $14,762")
st.subheader("Total Estimated Spend $5,495")
st.subheader("Total Savings $9,257")

# LTL To TL Mode Optimization

st.header("LTL To TL Mode Optimization")
st.subheader("Based On Weight We Recommend 16 Shipements Can Be Shipped via TL")
ltltldf = pd.read_csv(r"LTL To TL Mode Optimization.csv")
st.dataframe(ltltldf, use_container_width=True)
st.subheader("Total Spend $31,998")
st.subheader("Total Estimated Spend $21,911")
st.subheader("Total Savings $10,070")

# Parcel To LTL Consolidation

st.header("Parcel To LTL Consolidation")
st.subheader("In PARCEL Out Of 439,668 Shipments, 22,763 Can Be Consolidated")
parcelltlconsdf = pd.read_csv(r"Parcel To LTL Consolidation.csv")
st.dataframe(parcelltlconsdf, use_container_width=True)
st.subheader("By Consolidating 22,763 Shipments,303 Shipments Can Go via LTL Service")
parcelltlcons2df = pd.read_csv(r"ParcelToLTLCons2.csv")
st.dataframe(parcelltlcons2df, use_container_width=True)
st.subheader("Total Spend $101,780")
st.subheader("Total Estimated Spend $53,321")
st.subheader("Total Savings $48,126")

# LTL To TL Consolidation

st.header("LTL To TL Consolidation")
st.subheader("In LTL Out Of 16,000 Shipments, 1007 Can Be Consolidated")
ltltlconsdf = pd.read_csv(r"LTL To TL Consolidation.csv")
st.dataframe(ltltlconsdf, use_container_width=True)
st.subheader("By Consolidating 1007 Shipments, 6 Shipments Can Go via TL Service")
ltltlcons2df = pd.read_csv(r"ltltlconsdf.csv")
st.dataframe(ltltlcons2df, use_container_width=True)
st.subheader("Total Spend $22,468")
st.subheader("Total Estimated Charge $14,764")
st.subheader("Total Savings $7,698")

# TL vs TL DAT Rates

st.header("TL vs TL DAT Rates")
st.write ("As of today's date rate")
tldat = pd.read_csv(r"TLvsTLDAT.csv")
st.dataframe(tldat, use_container_width=True)
st.subheader("Total Spend $1,340,451")
st.subheader("Average Market Rate - Savings 541,459 (40.39%)")
st.subheader("Ceiling Rate - Savings $444,900 (33.19%)")

# LTL To TL Consolidation Weekwise

st.subheader("------------------------------------------------------------------------------")
st.header("Additional Potential Savings")
st.header("LTL To TL Consolidation Weekwise")
st.subheader("In LTL Out Of 16,000 Shipments, 1775 Can Be Consolidated")
ltltotlweek = pd.read_csv(r"LTL To TL Consolidation Weekwise.csv")
st.dataframe(ltltotlweek, use_container_width=True)
st.subheader("By Consolidating 1775 Shipments,53 Shipments Can Go via TL Service")
ltltotlweek2 = pd.read_csv(r"LTL To TL Consolidation Weekwise2.csv")
st.dataframe(ltltotlweek2, use_container_width=True)
st.subheader("Total Spend $465,263")
st.subheader("Total Estimated Charge $135,641")
st.subheader("Total Savings $329,573")


# Warehouse Savings 

df = pd.read_excel(r"locations_with_distances.xlsx")
st.header("Warehouse Analysis Based On Distance")
shipper_zip='sZip'
consignee_zip='cZip'
shipper_state='sState'
consignee_state='cState'
weight='Weight'
charge = 'Charge'

df[weight] = pd.to_numeric(df[weight], errors='coerce')  # Converts to float, invalid parsing becomes NaN

shipper_zips_of_interest1 = ["41408", "53142", "N8W0A7", "90630", "54942"]
considering_outbound = df[df[shipper_zip].isin(shipper_zips_of_interest1)]
considering_outbound = considering_outbound[considering_outbound[weight]<10000]
# print("Shape after filtering by weight:", considering_outbound.shape)

# print("Warehouse list",set(considering_outbound[shipper_zip]))
p=considering_outbound[[shipper_zip,shipper_state,'lat1','long1']]
p1=p.drop_duplicates(keep="first")
p1['shipper_lat_long'] = p1.apply(lambda row: f'({row["lat1"]}, {row["long1"]})', axis=1)
szip=[]
slat=[]
slong=[]
sstate=[]
for i in range(0,len(p1)):
    szip.append(p1[shipper_zip].iloc[i])
    slat.append(p1['lat1'].iloc[i])
    slong.append(p1['long1'].iloc[i])
    sstate.append(p1[shipper_state].iloc[i])
warehouse_lat_long=list(zip(szip,slat,slong,sstate))
# print("warehouse list with lat long",warehouse_lat_long)

# Initialize lists with None or default values
preferred_zip = [None] * len(considering_outbound)
preferred_state = [None] * len(considering_outbound)
preferred_lat_long = [None] * len(considering_outbound)
difference_distance = [None] * len(considering_outbound)

for i in range(0, len(considering_outbound)):
    miles = 99999999
    pzip = 0
    pstate = 'ab'
    plat = 0
    plong = 0
    
    if pd.notna(considering_outbound['lat'].iloc[i]) and pd.notna(considering_outbound['long'].iloc[i]):
        outbound_coords = (considering_outbound['lat'].iloc[i], considering_outbound['long'].iloc[i])
        
        for j in range(0, len(warehouse_lat_long)):
            if pd.notna(warehouse_lat_long[j][1]) and pd.notna(warehouse_lat_long[j][2]) and warehouse_lat_long[j][1] != 0 and warehouse_lat_long[j][2] != 0:
                warehouse_coords = (warehouse_lat_long[j][1], warehouse_lat_long[j][2])

                sample_miles = geodesic(outbound_coords, warehouse_coords).miles
                if sample_miles < miles:
                    miles = sample_miles
                    pzip = warehouse_lat_long[j][0]
                    pstate = warehouse_lat_long[j][3]
                    plat = warehouse_lat_long[j][1]
                    plong = warehouse_lat_long[j][2]
        
        pdistance = geodesic((considering_outbound['lat'].iloc[i], considering_outbound['long'].iloc[i]), (plat, plong)).miles
        difference_distance[i] = (considering_outbound['Distance'].iloc[i]) - pdistance
        preferred_zip[i] = pzip
        preferred_state[i] = pstate
        preferred_lat_long[i] = (plat, plong)

# Assign lists back to the dataframe
considering_outbound['preferred_loc'] = preferred_zip
considering_outbound['differnece_distance'] = difference_distance
considering_outbound['preferred_state'] = preferred_state
considering_outbound['preferredloc_lat_long'] = preferred_lat_long




#Getting preffered location which is not same as actual location and difference distance is greater than 100 miles
preferred_loc=considering_outbound[considering_outbound[shipper_zip] != considering_outbound['preferred_loc'] ]
preferred_loc=preferred_loc[preferred_loc['differnece_distance']>100]


#distance between preffered loc and czip
distance=[]
for idx in range(len(preferred_loc)):
    preferedlat_long=(preferred_loc['preferredloc_lat_long'])
    
    cziplat_long=(preferred_loc['lat'].iloc[idx],preferred_loc['long'].iloc[idx])
    
    disc=geodesic(preferred_loc['preferredloc_lat_long'].iloc[idx],cziplat_long).miles
    distance.append(disc)
preferred_loc['Preferred_Distance']=distance

#Map 
def map_is_created(zips, loc):
    map_centers = []
    colors = ['#e7b108','#ff6969','#96B6C5','#916DB3','#B0578D','#EDB7ED','#A8DF8E','#C8AE7D','#A79277','#A4BC92',
              '#e7b108','#ff6969','#96B6C5','#916DB3','#B0578D','#EDB7ED','#A8DF8E','#C8AE7D','#A79277','#A4BC92',
              '#e7b108','#ff6969','#96B6C5','#916DB3','#B0578D','#EDB7ED','#A8DF8E','#C8AE7D','#A79277','#A4BC92']
    incrementer = 0
    for i in range(0, len(warehouse_lat_long)):
        
        outbound_locations = considering_outbound[considering_outbound[zips] == warehouse_lat_long[i][0]]
        outbound_locations[loc] = outbound_locations.apply(lambda row: [row['lat'], row['long']] if pd.notna(row['lat']) and pd.notna(row['long']) else None, axis=1)

        # Filter out None or invalid locations
        valid_locations = outbound_locations[loc].dropna()

        # Ensure the center is valid (non-NaN lat/long)
        center = (warehouse_lat_long[i][1], warehouse_lat_long[i][2])
        if pd.notna(center[0]) and pd.notna(center[1]):
            data = {'center': center, 'locations': valid_locations.tolist(), 'line_color': colors[incrementer]}
            incrementer += 1
            map_centers.append(data)

    # Create a map
    mymap = folium.Map(location=[35.192, -89.8692], zoom_start=3, weight=1)

    for center_data in map_centers:
        center = center_data['center']
        locations = center_data['locations']
        line_color = center_data['line_color']

        # Add lines connecting center to locations
        folium.Marker(center, icon=folium.Icon(color='red')).add_to(mymap)
        for loc in locations:
            if loc:  # Make sure loc is not None or NaN
                folium.PolyLine([center, loc], color=line_color).add_to(mymap)
    
    return mymap
originalmap=(map_is_created(shipper_zip,'location'))      
st.write("Current fulfillment map by warehouse")  
folium_static(originalmap)

originalmap=(map_is_created('preferred_loc','locations_prefered'))      
st.write("Map if orders filled by preferred (closest) warehouse")  
folium_static(originalmap)   

st.write("Out of total 9359 Lanes ,731 lanes can be shipped from a warehouse that is closer (with a 100 mile tolerance).")
waredf = pd.read_csv(r"Warehousedf.csv")
st.dataframe(waredf, use_container_width=True)
st.subheader("Total Spend $322,103")
st.subheader("Total Estimated Spend $80,318")
st.subheader("Total Savings $241,425")

st.subheader("Efficient Warehouse Utilization: Localized Shipping Solutions")

pivot = pd.read_csv(r"pivot.csv")
pivot1 = pd.read_csv(r"pivot1.csv")
col1, col2 = st.columns(2)

# Display the first DataFrame in the first column
with col1:
    
    st.write(pivot)

# Display the second DataFrame in the second column
with col2:
    
    st.write(pivot1)



########################################################## Dimmed Out Packages ##########################################################

st.write("### 📦 Dimmed-Out Packages Analysis")

dop = pd.read_excel(r"Bluestar_ROI_dimmed.xlsx")
# --------------------------------------

dop['Weight'] = pd.to_numeric(dop['Weight'], errors='coerce')  # Converts to float, invalid parsing becomes NaN
# Step 1: Apply ceiling logic for rated and actual weights
dop['ceil_rated'] = np.ceil(dop['Rated Weight'])
dop['ceil_actual'] = np.ceil(dop['Weight'])  # Replace with correct column name if needed

# Step 2: Flag dimmed packages
dop['dimmed_out'] = dop['ceil_rated'] > dop['ceil_actual']

# Step 3: Grouping by ServiceLevel for counts
dimmed_by_carrier = dop.groupby("ServiceLevel").agg(
    total_packages=('dimmed_out', 'count'),
    dimmed_packages=('dimmed_out', 'sum')
).reset_index()

# Calculate undimmed packages
dimmed_by_carrier['undimmed_packages'] = dimmed_by_carrier['total_packages'] - dimmed_by_carrier['dimmed_packages']

# Display package summary
total_dimmed = int(dimmed_by_carrier['dimmed_packages'].sum())
total_undimmed = int(dimmed_by_carrier['undimmed_packages'].sum())
total_packages = total_dimmed + total_undimmed

st.subheader(f"Out of **{total_packages}** total packages, **{total_dimmed}** were dimmed-out and **{total_undimmed}** were not.")


# Step 4: Calculate undimmed and melt
dimmed_by_carrier['undimmed_packages'] = dimmed_by_carrier['total_packages'] - dimmed_by_carrier['dimmed_packages']

melted_df = dimmed_by_carrier.melt(
    id_vars=['ServiceLevel', 'total_packages'],
    value_vars=['dimmed_packages', 'undimmed_packages'],
    var_name='Package Type',
    value_name='Count'
)

# Step 5: Add percentage column
melted_df['Percentage'] = ((melted_df['Count'] / melted_df['total_packages']) * 100).round(1)

# Step 6: Rename for clarity
melted_df['Package Type'] = melted_df['Package Type'].replace({
    'dimmed_packages': 'Dimmed-Out',
    'undimmed_packages': 'Not Dimmed-Out'
})

# Step 7: Plot
fig2 = px.bar(
    melted_df,
    x='Percentage',
    y='ServiceLevel',
    color='Package Type',
    title='Percentage of Dimmed-Out vs Not Dimmed-Out Packages by Service Level',
    text=melted_df['Count'].round(1).astype(str),
    color_discrete_map={
        'Dimmed-Out': 'indianred',
        'Not Dimmed-Out': 'mediumseagreen'
    }
)

fig2.update_layout(
    barmode='stack',
    xaxis_title='Percentage of Packages',
    yaxis_title='Service Level',
    yaxis=dict(categoryorder='total ascending'),
    xaxis=dict(ticksuffix='%')
)

st.plotly_chart(fig2)

# --------------------------------------
# 💰 Cost Impact of Dimmed Packages
# --------------------------------------

st.write("### 💸 Cost Impact Analysis")


# Step 6: Estimate the cost if billed by actual weight
dop['cost_per_lb'] = dop[charge] / dop['Rated Weight']
dop['estimated_actual_cost'] = dop[weight] * dop['cost_per_lb']

# Step 7: Cost impact only for dimmed rows
dop['dimmed_cost_impact'] = np.where(
    dop['dimmed_out'],
    dop[charge] - dop['estimated_actual_cost'],
    0
)

# Step 8 (updated): Group by ServiceLevel
cost_impact_by_service = dop.groupby('ServiceLevel').agg(
    dimmed_cost_impact=('dimmed_cost_impact', 'sum'),
    dimmed_packages=('dimmed_out', 'sum')
).reset_index()

cost_impact_by_service['dimmed_cost_impact'] = cost_impact_by_service['dimmed_cost_impact'].round(2)
cost_impact_by_service = cost_impact_by_service[cost_impact_by_service['dimmed_cost_impact'] > 0]

# Display summary stats
total_impact = cost_impact_by_service['dimmed_cost_impact'].sum().round(2)
st.subheader(f"**Total Extra Spend Due to Dimmed-Out Packages:** 💰 ${total_impact:,.2f}")

# Step 9: Plot cost impact bar chart
fig3 = px.bar(
    cost_impact_by_service.sort_values(by='dimmed_cost_impact', ascending=False),
    x='dimmed_cost_impact',
    y='ServiceLevel',
    title='Cost Impact of Dimmed-Out Packages by Service Level',
    labels={'dimmed_cost_impact': 'Extra Cost ($)', 'ServiceLevel': 'Service Level'},
    text='dimmed_cost_impact'
)

fig3.update_layout(
    xaxis_title='Extra Cost Due to Dim Weight ($)',
    yaxis_title='Service Level',
    xaxis_tickprefix='$',
    yaxis=dict(categoryorder='total ascending')
)

st.plotly_chart(fig3)

print("successfully executed")