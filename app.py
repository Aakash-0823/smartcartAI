
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SmartRetail AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 SmartRetail AI")
st.caption("Intelligent E-Commerce & Retail Management")

# Sample inventory
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "Product": ["Headphones", "Smart Watch", "Shoes",
                    "Backpack", "T-Shirt"],
        "Category": ["Electronics", "Electronics", "Fashion",
                     "Accessories", "Fashion"],
        "Price (₹)": [1499, 2499, 1999, 799, 499],
        "Stock": [12, 4, 20, 3, 15],
        "Rating": [4.5, 4.7, 4.2, 4.0, 4.3]
    })

df = st.session_state.inventory

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Products", "Recommendations", "Inventory"]
)

if page == "Dashboard":
    st.header("Retail Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Products", len(df))
    c2.metric("Total Units in Stock", int(df["Stock"].sum()))
    c3.metric("Low-Stock Products", int((df["Stock"] < 5).sum()))

    st.subheader("Inventory Overview")
    st.bar_chart(df.set_index("Product")["Stock"])

    st.subheader("⚠️ Stock Alerts")
    low = df[df["Stock"] < 5]
    if low.empty:
        st.success("All products have sufficient stock.")
    else:
        for _, item in low.iterrows():
            st.warning(
                f'{item["Product"]}: only {item["Stock"]} units left!'
            )

elif page == "Products":
    st.header("Product Catalogue")
    category = st.selectbox(
        "Filter by category",
        ["All"] + sorted(df["Category"].unique().tolist())
    )
    view = df if category == "All" else df[df["Category"] == category]
    st.dataframe(view, use_container_width=True, hide_index=True)

elif page == "Recommendations":
    st.header("🎯 Product Recommendations")
    st.write("Choose a category to discover suitable products.")

    choice = st.selectbox(
        "Your interest",
        sorted(df["Category"].unique().tolist())
    )
    budget = st.slider("Your budget (₹)", 100, 5000, 2500, step=100)

    matches = df[
        (df["Category"] == choice) &
        (df["Price (₹)"] <= budget)
    ].sort_values("Rating", ascending=False)

    if matches.empty:
        st.info("No matching products. Try another budget or category.")
    else:
        st.success("Suggested products based on category, budget and rating")
        st.dataframe(matches, use_container_width=True, hide_index=True)

elif page == "Inventory":
    st.header("📦 Inventory Management")
    st.write("Demo data — edit a product's stock to test stock alerts.")

    product = st.selectbox("Select product", df["Product"].tolist())
    stock = st.number_input(
        "Update stock quantity",
        min_value=0,
        max_value=10000,
        value=int(df.loc[df["Product"] == product, "Stock"].iloc[0])
    )

    if st.button("Update Stock"):
        st.session_state.inventory.loc[
            st.session_state.inventory["Product"] == product, "Stock"
        ] = stock
        st.success(f"{product} stock updated to {stock} units.")
        st.rerun()

    st.dataframe(
        st.session_state.inventory,
        use_container_width=True,
        hide_index=True
    )

st.divider()
st.caption(
    "SmartRetail AI | Educational prototype using sample data. "
    "Recommendations are rule-based, not a trained AI model."
)
