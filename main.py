import streamlit as st
from streamlit_option_menu import option_menu
import Brain_analyser, home, meditron,account

st.set_page_config(
page_title = "Analyser.Br"
)

class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })


    def run():
        with st.sidebar:
            app = option_menu(
                menu_title = "Features",
                options = ['Meditron','Home','Account','Analyser'],
                icons = ['house-fill', 'chat-fill'],
                menu_icon = 'chat-text-fill',
                default_index = 1,
                styles={
                    "container": {"padding": "5!important", "background-color":'black'},
                    "icon": {"color": "white", "font-size": "18px"},
                    "nav-link": {"color":"white", "font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                    "menu-title": {"color": "white"},}
                )
        
        if app == 'Home':
            home.app()
        if app == 'Meditron':
            meditron.app()
        if app == 'Analyser':
            Brain_analyser.app()
        if app == 'Account':
            account.app()
    
    run()

        
    