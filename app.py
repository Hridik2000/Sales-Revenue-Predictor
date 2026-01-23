import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="Revenue Prediction App",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Revenue Prediction App")
st.write("Enter the details below to predict revenue")

@st.cache_resource
def load_model():
    return joblib.load("model/final_model.pkl")

@st.cache_resource
def load_ranges():
    return joblib.load("model/feature_ranges.pkl")



final_model = load_model()
ranges = load_ranges()

st.subheader("Input Features")

sales_qty = st.number_input(
    "Sales Quantity",
    min_value=int(ranges["Sales Quantity"]["min"]),
    max_value=int(ranges["Sales Quantity"]["max"]),
    value=int((ranges["Sales Quantity"]["min"] + ranges["Sales Quantity"]["max"]) / 2),
    help=f"Range used during training: {ranges['Sales Quantity']['min']} – {ranges['Sales Quantity']['max']}"
)


customers = st.number_input(
    "Number of Customers",
    min_value=int(ranges["Customers"]["min"]),
    max_value=int(ranges["Customers"]["max"]),
    value=int((ranges["Customers"]["min"] + ranges["Customers"]["max"]) / 2),
    help=(
        f"Range used during training: "
        f"{ranges['Customers']['min']} – {ranges['Customers']['max']}"
    )
)


margin = st.number_input(
    "Margin",
    min_value=float(ranges["Margin"]["min"]),
    max_value=float(ranges["Margin"]["max"]),
    value=round((ranges["Margin"]["min"] + ranges["Margin"]["max"]) / 2, 2),
    step=0.01,
    help=f"Training range: {ranges['Margin']['min']:.2f} – {ranges['Margin']['max']:.2f}"
)


margin_goal = st.number_input(
    "Margin Goal",
    min_value=0.0,
    max_value=1.0,
    value=0.30,
    step=0.01,
    help="Target margin (0–1). Keep within historical limits."
)


revenue_goal = st.number_input(
    "Revenue Goal",
    min_value=int(ranges["Revenue Goal"]["min"]),
    max_value=int(ranges["Revenue Goal"]["max"]),
    value=int(ranges["Revenue Goal"]["max"] * 0.5),
    help=f"{ranges['Revenue Goal']['min']} – {ranges['Revenue Goal']['max']}"
)


department = st.selectbox(
    "Department",
    [
        "Brinquedo",
        "Vestuário",
        "Eletrônicos",
        "Casa",
        "Papelaria",
        "Acessórios",
        "Esportes"
    ]
)

seller = st.selectbox(
    "Seller",
    [
        "Ana Sousa",
        "Beatriz Santos",
        "Camila Carvalho",
        "Camila Lima",
        "Thiago Barbosa",
        "Thiago Carvalho",
        "Vitória Ribeiro",
        "Letícia Nascimento"
    ]
)

def warn_if_outside(name, value):
    min_v = ranges[name]["min"]
    max_v = ranges[name]["max"]
    if value < min_v or value > max_v:
        st.warning(
            f"⚠ {name} is outside training range "
            f"({min_v:.2f} – {max_v:.2f}). Prediction reliability may drop."
        )

month = st.selectbox("Month", list(range(1, 13)))
dayofweek = st.selectbox("Day of Week (0=Mon)", list(range(0, 7)))

quarter = (month - 1) // 3 + 1

# -----------------------------
# Prediction
# -----------------------------
st.divider()

if st.button("🔮 Predict Revenue", key="predict_btn"):

    # Create input dataframe EXACTLY like training
    input_df = pd.DataFrame([{
        "Sales Quantity": sales_qty,
        "Customers": customers,
        "Margin": margin,
        "Margin Goal": margin_goal,
        "Revenue Goal": revenue_goal,
        "Department": department,
        "Seller": seller,
        "Month": month,
        "DayOfWeek": dayofweek,
        "Quarter": quarter
    }])

    # Predict (log scale)
    log_prediction = final_model.predict(input_df)

    # Convert back to original scale
    revenue_prediction = np.expm1(log_prediction)[0]

    st.success(f"💰 Predicted Revenue: ₹ {revenue_prediction:,.2f}")

    # Optional debug view
    with st.expander("🔍 See model input"):
        st.dataframe(input_df)

warn_if_outside("Sales Quantity", sales_qty)
warn_if_outside("Margin", margin)
warn_if_outside("Revenue Goal", revenue_goal)
warn_if_outside("Customers", customers)