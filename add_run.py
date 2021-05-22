import streamlit as st
# with st.form("my_form"):
#     st.write("Inside the form")
#     slider_val = st.slider("Form slider")
#     checkbox_val = st.checkbox("Form checkbox")
#    # Every form must have a submit button.
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         st.write("slider", slider_val, "checkbox", checkbox_val)
# # st.write("Outside the form")
# st.write('''
# div.stButton > button:first-child {
# background-color: #00cc00;color:white;font-size:20px;height:3em;width:30em;border-radius:10px 10px 10px 10px;
# }
# .css-2trqyj:focus:not(:active) {
# border-color: #ffffff;
# box-shadow: none;
# color: #ffffff;
# background-color: #0066cc;
# }
# .css-2trqyj:focus:(:active) {
# border-color: #ffffff;
# box-shadow: none;
# color: #ffffff;
# background-color: #0066cc;
# }
# .css-2trqyj:focus:active){
# background-color: #0066cc;
# border-color: #ffffff;
# box-shadow: none;
# color: #ffffff;
# background-color: #0066cc;
# }
# ''', unsafe_allow_html=True)
st.markdown("""<style>
                div[role="button"] ul {
                    direction: RTL;
                    text-align: right;
                    } </style>""", unsafe_allow_html=True)


st.markdown("""<style>
                div[data-baseweb="select"] {
                    direction: RTL;
                } </style>""", unsafe_allow_html=True)
if st.button("the notice you want to show"):
    st.write("content you want to tell")