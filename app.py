import streamlit as st
import pandas as pd
import plotly.express as px
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
import streamlit.components.v1 as components
from mitosheet.streamlit.v1 import spreadsheet
from streamlit_option_menu import option_menu
import google.generativeai as genai
from PIL import Image
from streamlit_extras.app_logo import add_logo


st.set_page_config(
    page_title="DropTable",
    page_icon="💧",
    layout="wide"
)
init_streamlit_comm()

def load_data(file):
    data = pd.read_csv(file, encoding='latin-1')
    return data
   
def main():
    add_logo("http://placekitten.com/120/120")

    #selected = option_menu(
       # menu_title = None,
        #options = ["Home","DropAI", "About"],
        #default_index = 0,
        #orientation = "horizontal",
        #icons = ["house","book","phone"]
    #)
    st.write(
        """![Static Badge](https://img.shields.io/badge/%20version-1.0.2-white)
        
        """
    )
    st.title(":blue[Drop]Table")
    st.subheader(":blue[Interactive] and :blue[dynamic] data analytics visualization dashboard")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv","XLSX"])
    tab1, tab2, tab3 = st.tabs(["Basic visualization", "DropAI","Advanced Interactive visualization",])
    with tab1:
        if uploaded_file is None:
            st.info("Upload a .csv or .xlsx spreadsheet file to continue", icon="ℹ️")
        # Upload CSV file through Streamlit

        if uploaded_file is not None:

            # Load data into a DataFrame
            df = load_data(uploaded_file)
            with st.expander("Click to expand uploaded datasheet 📜"):
                st.dataframe(df)

            # Plot based on user selection
            chart_types = st.multiselect("Select Chart Types", ["Bar Chart", "Stacked Bar Chart","Line Chart", "Scatter Plot", "Pie Chart", "Dot Plot", "Histogram", "Area Chart"])
            
            for chart_type in chart_types:
                st.subheader(f"{chart_type} Visualization")
                if chart_type == "Area Chart":
                    st.sidebar.write("Select attributes for Filled Area Chart")
                    x_axis = st.sidebar.selectbox("Select for Area Chart - X", df.columns, key=f"area_x_{chart_type}", index=None)
                    y_axis = st.sidebar.selectbox("Select for Area Chart - Y", df.columns, key=f"area_y_{chart_type}", index=None)
                    color = st.sidebar.selectbox("Select Colour Column", df.columns, key=f"area_c_{chart_type}", index=None)
                    line = st.sidebar.selectbox("Select Line Column", df.columns, key=f"area_l_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis is None or y_axis is None or color is None or line is None:
                        st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis)
                            fig = px.area(df_sort, x=x_axis, y=y_axis, color=color, line_group=line,title="Stacked filled area chart comparing sales with product line against order dates.", width=1240)
                            st.plotly_chart(fig)
                        st.toast('Graph visualized!', icon='🎉')
                    
                elif chart_type == "Histogram":
                    st.sidebar.write("Select X-axis and Y-axis for Histogram Chart")
                    x_axis = st.sidebar.selectbox("Select for Bar Chart - X", df.columns, key=f"hist_x_{chart_type}", index=None)
                    color = st.sidebar.selectbox("Select Colour Column", df.columns, key=f"hist_y_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis is None or color is None:
                        st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis)
                            fig = px.histogram(df_sort, x=x_axis, color=color, title='Order Status Distribution Over Time', width=1240)
                            st.plotly_chart(fig)
                        st.toast('Hooray!', icon='🎉')
                elif chart_type == "Bar Chart":
                    st.sidebar.write("Select X-axis and Y-axis for Bar Chart")
                    x_axis = st.sidebar.selectbox("Select for Bar Chart - X", df.columns, key=f"bar_x_{chart_type}", index=None)
                    y_axis = st.sidebar.selectbox("Select for Bar Chart - Y", df.columns, key=f"bar_y_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis is None or y_axis is None:
                        st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis)
                            fig = px.bar(df_sort, x=x_axis, y=y_axis, width=1240)
                            st.plotly_chart(fig)
                        st.toast('We did it!', icon='🎉')
                elif chart_type == "Line Chart":
                    st.sidebar.write("Select X-axis and Y-axis for Line Chart")
                    x_axis1 = st.sidebar.selectbox("Select for Line Chart - X", df.columns, key=f"line_x_{chart_type}", index=None)
                    y_axis1 = st.sidebar.selectbox("Select for Line Chart - Y", df.columns, key=f"line_y_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis1 is None or y_axis1 is None:
                        st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis1)
                            fig = px.line(df_sort, x=x_axis1, y=y_axis1, width=1240)
                            st.plotly_chart(fig)
                        st.toast('Hooray!', icon='🎉')
                elif chart_type == "Scatter Plot":
                    st.sidebar.write("Select X-axis and Y-axis for Scatter Plot Chart")
                    x_axis3 = st.sidebar.selectbox("Select for Scatter Plot - X", df.columns, key=f"scatter_x_{chart_type}", index=None)
                    y_axis3 = st.sidebar.selectbox("Select for Scatter Plot - Y", df.columns, key=f"scatter_y_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis3 is None or y_axis3 is None:
                        st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis3)
                            fig = px.scatter(df_sort, x=x_axis3, y=y_axis3, width=1240)
                            st.plotly_chart(fig)
                        st.toast('Another victory', icon='🥇')
                elif chart_type == "Pie Chart":
                    selected_column = st.sidebar.selectbox("Select Column for Pie Chart", df.columns, key=f"pie_column_{chart_type}", index=None)
                    st.sidebar.divider()
                    with st.spinner("Generating chart..."):
                        fig = px.pie(df, names=selected_column, title=f'Pie Chart for {selected_column}', width=1240)
                        st.plotly_chart(fig)
                    st.toast('Winning streak!', icon='🏆')
                elif chart_type == "Stacked Bar Chart":
                    st.sidebar.write("Select X-axis and Y-axis for Bubble Chart")
                    x_axis4 = st.sidebar.selectbox("Select for Stacked Bar Chart - X", df.columns, key=f"stacked_x_{chart_type}", index=None)
                    y_axis4 = st.sidebar.selectbox("Select for Stacked Bar Chart - Y", df.columns, key=f"stacked_y_{chart_type}", index=None)
                    color = st.sidebar.selectbox("Select Color Column", df.columns, key=f"stacked_size_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis4 is None or y_axis4 is None or color is None:
                        st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis4)
                            fig = px.bar(df_sort, x=x_axis4, y=y_axis4, color=color, title=f'Stacked Bar Chart for {x_axis4}, {y_axis4}, {color}', width=1240)
                            st.plotly_chart(fig)
                        st.toast('Bubbles and soap!', icon='🧼')
                elif chart_type == "Dot Plot":
                    st.sidebar.write("Select X-axis and Y-axis for Dot Plot Chart")
                    x_axis5 = st.sidebar.selectbox("Select for Dot Plot Chart - X", df.columns, key=f"dot_x_{chart_type}", index=None)
                    y_axis5 = st.sidebar.selectbox("Select for Dot Plot Chart - Y", df.columns, key=f"dot_y_{chart_type}", index=None)
                    st.sidebar.divider()
                    if x_axis5 is None or y_axis5 is None:
                         st.error("Either cant build relationship with given columns or Column(s) are empty")
                    else:
                        with st.spinner("Generating chart..."):
                            df_sort = df.sort_values(by=x_axis5)
                            fig = px.scatter(df_sort, x=x_axis5, y=y_axis5, title=f'Dot Plot for {x_axis5} and {y_axis5}', width=1240)
                            st.plotly_chart(fig)
                        st.toast('Hooray!', icon='🎉')
    with tab3:
        if uploaded_file is None:
            st.info("Upload a .csv or .xlsx spreadsheet file to continue", icon="ℹ️")
        if uploaded_file is not None:
            @st.cache_resource
            def get_pyg_html(df: pd.DataFrame) -> str:
                # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
                html = get_streamlit_html(df, dark="light", use_kernel_calc=True, debug=False)
                return html

            components.html(get_pyg_html(df), width=1240, height=915)
    with tab2:
        st.info("DropAI is a specially integrated AI using GoogleGenAI's Gemini-vision-pro model to analyse charts accurately", icon="💡")
        input = st.file_uploader("Choose a .png or .jpg file", type=['png'])
        if input is not None:
            img = Image.open(input)
            Google = 'AIzaSyDtl-9-hd5-JIXTnrYhf57_lQKsXm3Ksp0'
            genai.configure(api_key=Google)
            model = genai.GenerativeModel('gemini-pro-vision')
            with st.spinner("Sending and fetching data through DropAI"):
                response = model.generate_content(["Read and analyse this graphs and state all the valuable business intelligence insights one can derive from it in english", img])
                if response is None:
                    st.write(response.prompt_feedback)
                else:
                    st.write(response.prompt_feedback)
                    st.success("Analysis done 👌")
                    st.toast('Hooray!', icon='🎉')
                    st.balloons()
                    st.write(response.prompt_feedback)
                    st.image(input)
                    st.markdown(response.text)
            

if __name__ == "__main__":
    main()
