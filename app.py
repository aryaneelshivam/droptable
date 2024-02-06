import streamlit as st
import pandas as pd
import plotly.express as px
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit.components.v1 as components

st.set_page_config(
    page_title="droptable",
    page_icon="⚡",
)
init_streamlit_comm()

def load_data(file):
    data = pd.read_csv(file, encoding='latin-1')
    return data

def main():
    st.title("droptable")
    st.subheader("Interactive and dynamic data abalytics visualization dashboard")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    tab1, tab2  = st.tabs(["Basic visualization", "Advanced Interactive visualization"])
    with tab1:
        # Upload CSV file through Streamlit

        if uploaded_file is not None:

            # Load data into a DataFrame
            df = load_data(uploaded_file)

            # Plot based on user selection
            chart_types = st.multiselect("Select Chart Types", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Bubble Chart", "Sunburst Chart", "Dot Plot", "Histogram", "Area Chart"])
            
            for chart_type in chart_types:
                st.subheader(f"{chart_type} Visualization")
                if chart_type == "Area Chart":
                    st.write("Select attributes for Filled Area Chart")
                    x_axis = st.selectbox("Select for Area Chart - X", df.columns, key=f"area_x_{chart_type}")
                    y_axis = st.selectbox("Select for Area Chart - Y", df.columns, key=f"area_y_{chart_type}")
                    color = st.selectbox("Select Colour Column", df.columns, key=f"area_c_{chart_type}")
                    line = st.selectbox("Select Line Column", df.columns, key=f"area_l_{chart_type}")
                    fig = px.area(df, x=x_axis, y=y_axis, color=color, line_group=line,title="Stacked filled area chart comparing sales with product line against order dates.")
                    st.plotly_chart(fig)
                elif chart_type == "Histogram":
                    st.write("Select X-axis and Y-axis for Histogram Chart")
                    x_axis = st.selectbox("Select for Bar Chart - X", df.columns, key=f"hist_x_{chart_type}")
                    color = st.selectbox("Select Colour Column", df.columns, key=f"hist_y_{chart_type}")
                    fig = px.histogram(df, x=x_axis, color=color, title='Order Status Distribution Over Time')
                    st.plotly_chart(fig)
                elif chart_type == "Bar Chart":
                    st.write("Select X-axis and Y-axis for Bar Chart")
                    x_axis = st.selectbox("Select for Bar Chart - X", df.columns, key=f"bar_x_{chart_type}")
                    y_axis = st.selectbox("Select for Bar Chart - Y", df.columns, key=f"bar_y_{chart_type}")
                    fig = px.bar(df, x=x_axis, y=y_axis)
                    st.plotly_chart(fig)
                elif chart_type == "Line Chart":
                    st.write("Select X-axis and Y-axis for Line Chart")
                    x_axis1 = st.selectbox("Select for Line Chart - X", df.columns, key=f"line_x_{chart_type}")
                    y_axis2 = st.selectbox("Select for Line Chart - Y", df.columns, key=f"line_y_{chart_type}")
                    fig = px.line(df, x=x_axis1, y=y_axis2)
                    st.plotly_chart(fig)
                elif chart_type == "Scatter Plot":
                    st.write("Select X-axis and Y-axis for Scatter Plot Chart")
                    x_axis3 = st.selectbox("Select for Scatter Plot - X", df.columns, key=f"scatter_x_{chart_type}")
                    y_axis3 = st.selectbox("Select for Scatter Plot - Y", df.columns, key=f"scatter_y_{chart_type}")
                    fig = px.scatter(df, x=x_axis3, y=y_axis3)
                    st.plotly_chart(fig)
                elif chart_type == "Pie Chart":
                    selected_column = st.selectbox("Select Column for Pie Chart", df.columns, key=f"pie_column_{chart_type}")
                    fig = px.pie(df, names=selected_column, title=f'Pie Chart for {selected_column}')
                    st.plotly_chart(fig)
                elif chart_type == "Bubble Chart":
                    st.write("Select X-axis and Y-axis for Bubble Chart")
                    x_axis4 = st.selectbox("Select for Bubble Chart - X", df.columns, key=f"bubble_x_{chart_type}")
                    y_axis4 = st.selectbox("Select for Bubble Chart - Y", df.columns, key=f"bubble_y_{chart_type}")
                    size_column = st.selectbox("Select Size Column", df.columns, key=f"bubble_size_{chart_type}")
                    fig = px.scatter(df, x=x_axis4, y=y_axis4, size=size_column, title=f'Bubble Chart for {x_axis4}, {y_axis4}, {size_column}')
                    st.plotly_chart(fig)
                elif chart_type == "Sunburst Chart":
                    hierarchy_column = st.selectbox("Select Hierarchy Column", df.columns, key=f"sunburst_hierarchy_{chart_type}")
                    values_column = st.selectbox("Select Values Column", df.columns, key=f"sunburst_values_{chart_type}")
                    fig = px.sunburst(df, path=[hierarchy_column], values=values_column, title=f'Sunburst Chart for {hierarchy_column} and {values_column}')
                    st.plotly_chart(fig)
                elif chart_type == "Dot Plot":
                    st.write("Select X-axis and Y-axis for Dot Plot Chart")
                    x_axis5 = st.selectbox("Select for Dot Plot Chart - X", df.columns, key=f"dot_x_{chart_type}")
                    y_axis5 = st.selectbox("Select for Dot Plot Chart - Y", df.columns, key=f"dot_y_{chart_type}")
                    fig = px.scatter(df, x=x_axis5, y=y_axis5, title=f'Dot Plot for {x_axis5} and {y_axis5}')
                    st.plotly_chart(fig)
                    
            @st.cache_resource
            def get_pyg_html(df: pd.DataFrame) -> str:
                # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
                html = get_streamlit_html(df, use_kernel_calc=True, debug=False)
                return html

            components.html(get_pyg_html(df), height=900, scrolling=True)

if __name__ == "__main__":
    main()
