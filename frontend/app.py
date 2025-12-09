import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Park Operations Management System", layout="wide")
st.title("Park Operations Management System")
st.markdown("Fetch and display park data from api")
st.sidebar.header("API Configuration")

api_options = {
    "PARKS": "http://localhost:8000/parks",
    "CENTERS": "http://localhost:8000/visitor_centers",
    "ACTIVITIES": "http://localhost:8000/activities",
}
selected_api = st.sidebar.selectbox("Select an API:", list(api_options.keys()))
api_url = api_options[selected_api]
    

if st.sidebar.button("Fetch Data", type="primary"):
    try:
        with st.spinner("Fetching data..."):
            response = requests.get(api_url,timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                st.error("Unsupported data format")
                st.stop()
            st.session_state['df'] = df
            st.session_state['api_url'] = api_url
            st.success(f"Successfully fetched {len(df)} records!")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
    except ValueError as e:
        st.error(f"Error parsing JSON: {str(e)}")
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
if 'df' in st.session_state:
    df = st.session_state['df']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    st.subheader("Filter Options")
    col1, col2 = st.columns(2)
    with col1:
        selected_columns = st.multiselect(
            "Select columns to display:",
            options=df.columns.tolist(),
            default=df.columns.tolist()
        )
    with col2:
        max_rows = st.slider("Number of rows to display:", 
                            min_value=5, 
                            max_value=len(df), 
                            value=min(50, len(df)))
    if selected_columns:
        filtered_df = df[selected_columns].head(max_rows)
        
        st.subheader("Table")
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="data.csv",
            mime="text/csv"
        )
    else:
        st.warning("Please select at least one column to display")
else:
    st.info("Configure the API settings in the sidebar and click 'Fetch Data' to get started!")
st.markdown("---")
st.markdown("Developed by Hamad")