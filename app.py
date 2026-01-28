
import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="Dashboard E-commerce", layout="wide")
st.title("📊 Dashboard E-commerce")

# -----------------------
# LOAD DATA
# -----------------------
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

    # -----------------------
    # ACTIVITÉ UTILISATEURS DANS LE TEMPS
    # -----------------------
    st.subheader("📈 Activité des utilisateurs dans le temps")

    df_time = df.copy()
    df_time["date"] = df_time["timestamp"].dt.date
    df_time["month"] = df_time["timestamp"].dt.to_period("M").astype(str)
    df_time["year"] = df_time["timestamp"].dt.year

    # 📅 Par jour (DAU)
    daily_activity = (
        df_time.groupby("date")["visitorid"]
        .nunique()
        .reset_index(name="utilisateurs_actifs")
    )

    fig_day = px.line(
        daily_activity,
        x="date",
        y="utilisateurs_actifs",
        title="📅 Activité quotidienne des utilisateurs (DAU)"
    )
    st.plotly_chart(fig_day, use_container_width=True)

    # 📆 Par mois (MAU)
    monthly_activity = (
        df_time.groupby("month")["visitorid"]
        .nunique()
        .reset_index(name="utilisateurs_actifs")
    )

    fig_month = px.line(
        monthly_activity,
        x="month",
        y="utilisateurs_actifs",
        title="📆 Activité mensuelle des utilisateurs (MAU)"
    )
    st.plotly_chart(fig_month, use_container_width=True)

    # 📈 Par année (YAU)
    yearly_activity = (
        df_time.groupby("year")["visitorid"]
        .nunique()
        .reset_index(name="utilisateurs_actifs")
    )

    fig_year = px.bar(
        yearly_activity,
        x="year",
        y="utilisateurs_actifs",
        title="📈 Activité annuelle des utilisateurs (YAU)"
    )
    st.plotly_chart(fig_year, use_container_width=True)




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

    # Drop-off
    st.subheader("📉 Drop-off entre les étapes")

    funnel_df["Drop-off (%)"] = (
        funnel_df["Utilisateurs"]
        .pct_change()
        .fillna(0) * -100
    )

    st.dataframe(funnel_df)
