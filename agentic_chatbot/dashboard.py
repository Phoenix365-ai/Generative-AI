import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import ollama

# Cyberpunk Theme Styling
st.markdown(
    """
    <style>
        body {
            background-color: #0d0d0d;
            color: #00ffcc;
            font-family: 'Orbitron', sans-serif;
        }
        .stButton>button {
            background-color: #00ffcc;
            color: black;
            border-radius: 10px;
            font-weight: bold;
        }
        .stFileUploader {
            border: 2px dashed #00ffcc;
            padding: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("🚀 AI-Powered Dashboard Generator with Ollama")
st.markdown("**Upload your dataset and let AI generate insights!**")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read Data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("✅ File Uploaded Successfully!")
    st.dataframe(df.head())
    
    # Dashboard Selection
    dashboard_option = st.selectbox("Select a Dashboard", [
        "Select an option", "Key Performance Indicators", "Numerical Data Analysis",
        "Categorical Data Analysis", "Correlation Heatmap", "Scatter Plots",
        "AI-Powered Data Insights"])
    
    # Key Performance Indicators (KPIs)
    if dashboard_option == "Key Performance Indicators":
        st.subheader("📌 Key Performance Indicators")
        st.metric(label="Total Rows", value=df.shape[0])
        st.metric(label="Total Columns", value=df.shape[1])
        st.metric(label="Missing Values", value=df.isnull().sum().sum())
    
    # Numerical Data Analysis
    elif dashboard_option == "Numerical Data Analysis":
        st.subheader("📊 Numerical Data Analysis")
        for col in df.select_dtypes(include=['number']).columns:
            fig = px.histogram(df, x=col, title=f"Distribution of {col}", color_discrete_sequence=["#00ffcc"])
            st.plotly_chart(fig, use_container_width=True)
    
    # Categorical Data Analysis
    elif dashboard_option == "Categorical Data Analysis":
        st.subheader("📊 Categorical Data Analysis")
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() < 20:
                fig = px.bar(df[col].value_counts(), x=df[col].value_counts().index, y=df[col].value_counts().values, 
                             title=f"Category Distribution for {col}", color_discrete_sequence=["#ff66cc"])
                st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Heatmap
    elif dashboard_option == "Correlation Heatmap":
        st.subheader("📈 Correlation Heatmap")
        if not df.select_dtypes(include=['number']).empty:
            corr = df.select_dtypes(include=['number']).corr()
            fig = px.imshow(corr, text_auto=True, color_continuous_scale="teal")
            st.plotly_chart(fig)
        else:
            st.warning("⚠ No numerical columns available for correlation analysis.")
    
    # Scatter Plots
    elif dashboard_option == "Scatter Plots":
        st.subheader("📍 Scatter Plots for Correlation Analysis")
        num_cols = df.select_dtypes(include=['number']).columns
        for i in range(len(num_cols) - 1):
            fig = px.scatter(df, x=num_cols[i], y=num_cols[i + 1], title=f"Scatter Plot of {num_cols[i]} vs {num_cols[i + 1]}")
            st.plotly_chart(fig, use_container_width=True)
    
    # AI-Powered Data Insights
    elif dashboard_option == "AI-Powered Data Insights":
        st.subheader("🤖 AI-Generated Insights")
        prompt = f"Generate key insights and observations based on the following dataset:\n{df.describe().to_string()}"
        response = ollama.chat(model='mistral', messages=[{"role": "user", "content": prompt}])
        if "message" in response and "content" in response["message"]:
            st.write(response["message"]["content"])
        else:
            st.error("⚠ Error retrieving AI insights. Please check your Ollama setup.")
