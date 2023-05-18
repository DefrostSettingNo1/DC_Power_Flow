import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="DC Power Flow App",
    page_icon="💡",
    layout="wide"
)

with st.container():
    col1, col2 = st.columns([5,1], gap="large")

    with col2:
        image1 = Image.open('National_Grid_Logo_White.png')
        st.image(image1, use_column_width="always")

    with col1:
        with st.container():
            col21, col22, col23 = st.columns([1,5,1])
            with col22:
                st.text('\n')
                st.text('\n')
                st.title("Welcome to the DC Power Flow App!")
        st.text('\n')
st.text('\n')
st.text('\n')
st.subheader(":blue[This App has been designed to enable you to run DC power flow analysis and review the results to establish the viability of any network background you have defined.]")
st.subheader(":blue[The App has been created by the System Access team and pulls data from the latest **TEC Register**, latest **Interconnector Register**, **FES 2022** and **ETYS 2022 (Appendix B)**, and has been set up for 2027, however further developments are expected in future which will enable users to choose a year.]")
st.subheader(":blue[A diagram has been included below illustrating the mess of tools and services that make the DC Power Flow App run:]")
st.text('\n')
st.text('\n')
st.text('\n')
with st.container():
    col3, col4 = st.columns([3,2])
    with col3:
        image2 = Image.open('Process inputs for power flow app.png')
        st.image(image2, use_column_width="always")

st.sidebar.success("Select _Configure_ to Run Power Flow.")
