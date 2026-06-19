import streamlit as st 
import requests

st.title("Sales Revenue Estimator")

sales_quantity = st.number_input(
           "Sales Quantity",
           min_value = 0)
           
customers = st.number_input(
            "Customers",
            min_value = 0)
            
margin = st.number_input(
          "Margin",
          min_value = 0.0,
          step = 0.01)
          
margin_goal = st.number_input(
               "Margin_Goal",
               min_value = 0.0,
               step = 0.01)
               
revenue_goal = st.number_input(
               "Revenue Goal",
               min_value = 0)
               
date = st.date_input(
        "Date")
        
department = st.text_input(
             "Department")
             
             
seller = st.text_input("Seller")

if st.button("Predict Revenue"):

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json={
            "Sales_Quantity": sales_quantity,
            "Customers": customers,
            "Margin": margin,
            "Margin_Goal": margin_goal,
            "Revenue_Goal": revenue_goal,
            "Date": str(date),
            "Department": department,
            "Seller": seller
        }
    )

    result = response.json()
    print(f"Result is:{result}")

    st.success(
        f"Predicted Revenue: {result}"
    )
    
    
    
