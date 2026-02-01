
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt



# CONFIG

st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("📊 Dashboard E-commerce")


# LOAD DATA

@st.cache_data
@st.cache_data
def load_data():
    df = pd.read_csv("data/df_merged.csv")

    # On utilise le timestamp des événements
    df["timestamp"] = pd.to_datetime(df["timestamp_x"])

    return df


df = load_data()


# -----------------------
tab_users, tab_products, tab_categories, tab_funnel = st.tabs(
    ["👤 Utilisateurs", "📦 Produits", "🗂️ Catégories", "🔻 Funnel Événements"]
)


with tab_users:
    st.subheader("👤 Métriques Utilisateurs")

    # KPIs globaux
    users = df["visitorid"].nunique()
    events = len(df)
    transactions = df[df["event"] == "transaction"]["transactionid"].nunique()
    conversion_rate = transactions / users if users > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Utilisateurs uniques", users)
    c2.metric("Événements", events)
    c3.metric("Transactions", transactions)
    c4.metric("Taux de conversion", f"{conversion_rate:.2%}")

    st.divider()

    
    # ACTIVITÉ UTILISATEURS DANS LE TEMPS
   
    import plotly.express as px

st.header("📈 Activité des utilisateurs dans le temps")

# Conversion timestamp si nécessaire
df["timestamp"] = pd.to_datetime(df["timestamp_x"], unit="ms")

# Agrégation temporelle (par jour)
activity = (
    df
    .set_index("timestamp")
    .resample("D")
    .size()
    .reset_index(name="events")
)

fig = px.line(
    activity,
    x="timestamp",
    y="events",
    title="Évolution de l’activité utilisateur (événements / jour)",
    markers=True
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Nombre d'événements",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

freq = st.selectbox(
    "Granularité temporelle",
    ["Jour", "Semaine", "Mois"]
)



with tab_products:
    st.subheader("📦 Performance Produits")

    product_perf = (
        df[df["event"] == "transaction"]
        .groupby("itemid")
        .agg(
            transactions=("transactionid", "nunique"),
            revenue=("value", "sum")
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    st.dataframe(product_perf.head(20))

    fig = px.bar(
        product_perf.head(10),
        x="itemid",
        y="revenue",
        title="Top 10 produits par revenu"
    )

    st.plotly_chart(fig, use_container_width=True)

with tab_categories:
    st.subheader("🗂️ Performance Catégories")

    category_perf = (
        df[df["event"] == "transaction"]
        .groupby("categoryid")
        .agg(
            transactions=("transactionid", "nunique"),
            revenue=("value", "sum")
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    st.dataframe(category_perf.head(20))

    fig = px.bar(
        category_perf.head(10),
        x="categoryid",
        y="revenue",
        title="Top 10 catégories par revenu"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    
with tab_funnel:
    st.subheader("🔻 Funnel des événements")

    funnel_steps = [
        ("View", "view"),
        ("Add to cart", "addtocart"),
        ("Transaction", "transaction")
    ]

    funnel_data = []

    for label, event_name in funnel_steps:
        users_count = df[df["event"] == event_name]["visitorid"].nunique()
        funnel_data.append({
            "Étape": label,
            "Utilisateurs": users_count
        })

    funnel_df = pd.DataFrame(funnel_data)

    fig = px.funnel(
        funnel_df,
        x="Utilisateurs",
        y="Étape",
        title="Funnel de conversion des événements"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Drop-off entre les étapes

st.header("🧭 Drop entre les étapes du funnel")

# Comptage des événements
event_counts = df["event"].value_counts()

views = event_counts.get("view", 0)
add_to_cart = event_counts.get("addtocart", 0)
transactions = event_counts.get("transaction", 0)

funnel_df = pd.DataFrame({
    "Étape": ["View", "Add to Cart", "Transaction"],
    "Volume": [views, add_to_cart, transactions]
})

fig = px.pie(
    funnel_df,
    names="Étape",
    values="Volume",
    hole=0.45,
    title="Répartition des étapes du funnel"
)

fig.update_traces(
    textinfo="percent+label",
    pull=[0, 0.05, 0.1]  
)

fig.update_layout(
    showlegend=True,
    height=400,
    margin=dict(t=60, b=20)
)

st.plotly_chart(fig, use_container_width=True)


