# Data Applications

This folder contains interactive data applications and dashboards.

## Structure

- **`streamlit/`** - Streamlit applications
  - Data exploration apps
  - ML model demos
  - Internal tools
  - Analytics dashboards

- **`dash/`** - Plotly Dash applications
  - Complex interactive dashboards
  - Real-time monitoring apps

- **`gradio/`** - Gradio ML applications
  - ML model interfaces
  - Prediction demos
  - Model testing tools

## Streamlit

Streamlit is the easiest way to build data apps in Python.

### Quick Start
```bash
# Install Streamlit
pip install streamlit

# Run example app
streamlit run streamlit/app.py
```

### Example App
```python
import streamlit as st
import pandas as pd

st.title("My Data App")

# Load data from your warehouse
@st.cache_data
def load_data():
    # Query your dbt models
    return pd.read_sql("SELECT * FROM analytics.customers", conn)

df = load_data()
st.dataframe(df)

# Add interactivity
metric = st.selectbox("Select metric", ["revenue", "orders", "customers"])
st.line_chart(df[metric])
```

### Best Practices
1. **Cache data** - Use `@st.cache_data` for expensive operations
2. **Query dbt models** - Connect to your transformed data
3. **Modular code** - Split into reusable components
4. **Authentication** - Add auth for production apps
5. **Deployment** - Deploy to Streamlit Cloud or self-host

## Dash

Plotly Dash is great for complex, production-grade dashboards.

### When to Use Dash
- Need more control than Streamlit provides
- Building complex multi-page apps
- Require custom callbacks and interactivity

## Gradio

Gradio is perfect for ML model interfaces.

### Example
```python
import gradio as gr

def predict(text):
    # Your ML model prediction
    return prediction

demo = gr.Interface(
    fn=predict,
    inputs="text",
    outputs="label"
)

demo.launch()
```

## Deployment

### Streamlit Cloud
```bash
# Push to GitHub, then deploy via Streamlit Cloud UI
# https://streamlit.io/cloud
```

### Self-Hosted
```bash
# Docker deployment
docker build -t my-streamlit-app .
docker run -p 8501:8501 my-streamlit-app
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Dash Documentation](https://dash.plotly.com/)
- [Gradio Documentation](https://gradio.app/docs/)
