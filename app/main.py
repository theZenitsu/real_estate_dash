import streamlit as st
import plotly.express as px
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from models import Ville, Annonce, Equipement, annonce_equipement
from database import engine

# Database session setup
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit configuration
st.set_page_config(
    page_title="Real Estate Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("Real Estate Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
min_price, max_price = st.sidebar.slider("Price Range (€)", 0, 1000000, (100000, 500000), key="price_filter")
selected_city = st.sidebar.selectbox(
    "City", ["All"] + [city.name for city in session.query(Ville).all()], key="city_filter"
)
selected_equipments = st.sidebar.multiselect(
    "Equipments", [equipment.name for equipment in session.query(Equipement).all()], key="equipment_filter"
)

# Fetch filtered data
query = session.query(
    Annonce.title, 
    Annonce.price, 
    Annonce.nb_rooms, 
    Annonce.nb_baths, 
    Annonce.surface_area, 
    Ville.name.label("city")
).join(Ville, Annonce.city_id == Ville.id)

if selected_city != "All":
    query = query.filter(Ville.name == selected_city)

query = query.filter(Annonce.price.between(min_price, max_price))

data = pd.DataFrame(query.all(), columns=["Title", "Price (€)", "Rooms", "Bathrooms", "Surface (m²)", "City"])

# Optional: Filter by selected equipment
if selected_equipments:
    equipment_ids = [
        equip.id for equip in session.query(Equipement).filter(Equipement.name.in_(selected_equipments)).all()
    ]
    query_with_equipments = (
        session.query(Annonce.title)
        .join(annonce_equipement, Annonce.id == annonce_equipement.c.annonce_id)
        .filter(annonce_equipement.c.equipement_id.in_(equipment_ids))
    )
    equipment_filtered_titles = [result[0] for result in query_with_equipments.all()]
    data = data[data["Title"].isin(equipment_filtered_titles)]

# Display filtered data
st.subheader(f"Filtered Listings ({len(data)} results)")
st.dataframe(data)

# Add download button
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="filtered_listings.csv",
    mime="text/csv",
)

# Visualizations
# City Analysis
st.subheader("City Analysis: Number of Listings by City")
city_data = (
    session.query(Ville.name, func.count(Annonce.id).label("count"))
    .join(Annonce, Ville.id == Annonce.city_id)
    .group_by(Ville.name)
    .all()
)
city_df = pd.DataFrame(city_data, columns=["City", "Count"])
fig_city = px.bar(
    city_df,
    x="City",
    y="Count",
    color="City",
    title="Number of Listings by City",
    text="Count",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig_city.update_traces(texttemplate='%{text}', textposition='outside')
fig_city.update_layout(yaxis_title="Number of Listings")
st.plotly_chart(fig_city)

# Price Analysis
st.subheader("Price Analysis: Distribution of Prices")
price_hist = px.histogram(
    data, 
    x="Price (€)", 
    nbins=20, 
    title="Distribution of Property Prices", 
    color_discrete_sequence=px.colors.qualitative.Set3
)
price_hist.update_layout(yaxis_title="Count")
st.plotly_chart(price_hist)

# Price by City Analysis
st.subheader("Price Analysis: Price Distribution by City")
boxplot_city_price = px.box(
    data,
    x="City",
    y="Price (€)",
    color="City",
    title="Price Distribution by City",
    color_discrete_sequence=px.colors.qualitative.Pastel1,
)
st.plotly_chart(boxplot_city_price)


# Equipment Analysis
st.subheader("Equipment Analysis: Equipment Distribution")
equipment_data = (
    session.query(Equipement.name, func.count(annonce_equipement.c.equipement_id).label("count"))
    .join(annonce_equipement, Equipement.id == annonce_equipement.c.equipement_id)
    .group_by(Equipement.name)
    .all()
)
equipment_df = pd.DataFrame(equipment_data, columns=["Equipment", "Count"])
fig_equipment = px.pie(
    equipment_df,
    values="Count",
    names="Equipment",
    title="Equipment Distribution",
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_equipment)

# Temporal Analysis
st.subheader("Temporal Analysis: Number of Listings Over Time")
temporal_data = (
    session.query(func.date_trunc('month', Annonce.datetime).label("Month"), func.count(Annonce.id).label("Count"))
    .group_by(func.date_trunc('month', Annonce.datetime))
    .order_by(func.date_trunc('month', Annonce.datetime))
    .all()
)
temporal_df = pd.DataFrame(temporal_data, columns=["Month", "Count"])
fig_temporal = px.line(
    temporal_df,
    x="Month",
    y="Count",
    title="Number of Listings Over Time",
    markers=True,
    color_discrete_sequence=["#636EFA"],
)
st.plotly_chart(fig_temporal)

# Surface vs Price Analysis
st.subheader("Surface vs Price Analysis: Relationship Between Surface Area and Price")
scatter_surface_price = px.scatter(
    data,
    x="Surface (m²)",
    y="Price (€)",
    color="City",
    title="Relationship Between Surface Area and Price",
    size="Rooms",
    color_discrete_sequence=px.colors.qualitative.Vivid,
    hover_data=["Bathrooms"],
)
st.plotly_chart(scatter_surface_price)
