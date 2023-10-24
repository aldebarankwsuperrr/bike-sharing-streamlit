import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

st.header('Bike Sharing :bike:')
hour = pd.read_csv("./hour_cleaned.csv")
with st.sidebar:
    st.image("bicycle.png")
    
    year = st.selectbox(
        label="Tahun",
        options=(2011, 2012)
    )
st.subheader('Bike Sharing Trend In {year}'.format(year = year))

def create_by_month(hour_updated):
    month = hour_updated.groupby(by=["month"],sort=False).agg({
    "count":"sum"
    }).reset_index()
    
    return month

def create_by_season(hour_updated):
    season = hour_updated.groupby(by=["season"], sort=False).agg({
    "count":"sum"
    }).reset_index()
    
    return season

def create_by_weather(hour_updated):
    weather = hour_updated.groupby(by=["weathersit"]).agg({
    "count":"sum"
    }).reset_index()
    
    return weather

def create_by_holiday(hour_updated):
    holiday = hour_updated.groupby(by=["holiday"]).agg({
    "count":"sum"
    }).reset_index()
    
    return holiday

def create_busiest_hour(hour_updated):
    busiest = hour_updated.groupby(by=["hour"]).agg({
    "count":"mean"
    }).reset_index()
    
    busiest.columns = ["hour", "average frequency"]
    busiest["sibuk"] = busiest["average frequency"].apply(lambda x: "sibuk" if x > busiest["average frequency"].mean() else "tidak sibuk")
    busiest["warna"] = busiest["sibuk"].apply(lambda x: "#72BCD4" if x == "sibuk" else "#D3D3D3")
    
    return busiest
    
def create_by_day(hour_updated):
    day_bike = hour_updated.groupby(by=["weekday"]).agg({
        "count":"sum"
    }).reset_index().sort_values(by=["count"], ascending=False)
    
    return day_bike
    
hour_updated = hour[hour['year'] == year]
col1, col2 = st.columns(2)

base_sum = hour[hour['year'] == 2011]['count'].sum()
selisih = hour_updated['count'].sum() - base_sum
    
avg_2012 = hour[hour['year'] == 2012]['count'].mean().round(2)
avg_2011 = hour[hour['year'] == 2011]['count'].mean().round(2)
average = ((avg_2012 - avg_2011) / avg_2011).round(2) * 100

with col1:
    total_bike_sharing = hour_updated['count'].sum()
    if year == 2012:
        st.metric("Total", value=total_bike_sharing, delta=str(selisih))
    else:
        st.metric("Total", value=total_bike_sharing)
 
with col2:
    if year == 2012:
        st.metric("Rata-Rata", value=avg_2012, delta=str("+{average}%".format(average=average)))
    else:
        st.metric("Rata-Rata", value=avg_2011)
    
month = create_by_month(hour_updated)
fig, ax = plt.subplots(figsize=(18, 6))
ax.plot(
    month["month"],
    month["count"],
    linewidth=6,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=16)
st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    season = create_by_season(hour_updated)
    colors = ["#D3D3D3", "#D3D3D3", "#72BCD4","#D3D3D3"]
    fig, ax = plt.subplots(figsize=(7, 6))
    
    sns.barplot(data=season, x="season", y="count", palette=colors)
    ax.set_title("Trend by Season", loc="center", fontsize=17)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=16)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

with col4:
    weather = create_by_weather(hour_updated)
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3","#D3D3D3"]
    fig, ax = plt.subplots(figsize=(7, 6))
    
    sns.barplot(data=weather, x="weathersit", y="count", palette=colors)
    ax.set_title("Trend by Weather", loc="center", fontsize=17)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=16)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)


day = create_by_day(hour_updated)
fig, ax = plt.subplots(figsize=(18, 6))
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(data=day, x="weekday", y="count", palette=colors)
ax.set_title("Trend by Day", loc="center", fontsize=17)
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=16)
ax.set_ylabel(None)
ax.set_xlabel(None)
st.pyplot(fig)

st.subheader('Busiest Hour In {year}'.format(year = year))

busiest = create_busiest_hour(hour_updated)
fig, ax = plt.subplots(figsize=(18, 6))
st.dataframe(data=busiest[["hour", "average frequency"]], width=500, height=300)
colors = list(busiest["warna"])
sns.barplot(data=busiest, x="hour", y="average frequency", palette=colors)
# plt.xticks(busiest["hour"])
ax.tick_params(axis='y', labelsize=15)
ax.tick_params(axis='x', labelsize=16)
ax.set_ylabel(None)
ax.set_xlabel(None)
st.pyplot(fig)
