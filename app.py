import streamlit as st
import pandas as pd
import plotly.express as px


# ----------------------------
# Page Title
# ----------------------------
st.set_page_config(
    page_title="Netflix Data Analysis Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------
# Background Color
# ----------------------------
st.markdown("""
<style>

.stApp{
    background-color:white;
}

h1{
    color:#E50914;
    text-align:center;
}

label{
    color:white !important;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("netflix_titles.csv")

# Fill Missing Values
df["country"] = df["country"].fillna("Unknown")
df["listed_in"] = df["listed_in"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Not Rated")

# ----------------------------
# Dashboard Title
# ----------------------------
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/7/75/Netflix_icon.svg",
    width=100
)

st.title("Netflix Data Analysis Dashboard")

# ----------------------------
# Country List
# ----------------------------
countries = []

for i in df["country"]:
    country_list = i.split(", ")

    for j in country_list:
        countries.append(j)

countries = sorted(list(set(countries)))

country = st.selectbox(
    "Select Country",
    countries
)

# ----------------------------
# Genre List
# ----------------------------
genres = []

for i in df["listed_in"]:
    genre_list = i.split(", ")

    for j in genre_list:
        genres.append(j)

genres = sorted(list(set(genres)))

genre = st.selectbox(
    "Select Genre",
    genres
)

# ----------------------------
# Release Year
# ----------------------------
year = st.selectbox(
    "Select Release Year",
    sorted(df["release_year"].unique(), reverse=True)
)

# ----------------------------
# Apply Filters
# ----------------------------
filtered = df[
    (df["country"].str.contains(country, na=False)) &
    (df["listed_in"].str.contains(genre, na=False)) &
    (df["release_year"] == year)
]

# ----------------------------
# Display Dataset
# ----------------------------
st.subheader("Filtered Netflix Dataset")

st.dataframe(filtered)

# ----------------------------
# Charts
# ----------------------------

if len(filtered) > 0:

    col1, col2 = st.columns(2)

    # Rating Distribution
    with col1:

        st.subheader("Rating Distribution")

        fig1 = px.histogram(
            filtered,
            x="rating",
            color="type",
            title="Rating Distribution"
        )

        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor="#141414",
            plot_bgcolor="#141414"
        )

        st.plotly_chart(fig1)

    # Movies vs TV Shows
    with col2:

        st.subheader("Movies vs TV Shows")

        type_count = filtered["type"].value_counts().reset_index()

        type_count.columns = ["Type", "Count"]

        fig2 = px.pie(
            type_count,
            names="Type",
            values="Count",
            hole=0.4,
            title="Movies vs TV Shows"
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#141414",
            plot_bgcolor="#141414"
        )

        st.plotly_chart(fig2)

else:

    st.warning("No data found for the selected filters.")