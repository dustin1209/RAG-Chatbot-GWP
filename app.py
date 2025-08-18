import streamlit as st
from lib import ui
from lib import gwp_calculator
from lib import chatbot

#Ausführen der App anhand der Main-Funktion
def main():
    """Main function to run the Streamlit application."""
    #Zeigt die Ausgabe an 
    ui.display_main_page()
    #Asuwahlmöglichketen der GUI
    if "auswahl_bestaetigt" not in st.session_state:
        st.session_state.auswahl_bestaetigt = False
    if "details_bestaetigt" not in st.session_state:
        st.session_state.details_bestaetigt = False
    'Einholen der Benutzerauswhl'
    option = ui.get_user_choice()
    #Wenn Berechnungstool geöffnet wird, wird dieses auch ausgeführt ansonsten start des Chatbots
    if st.session_state.auswahl_bestaetigt:
        if option == "Berechnung des Global Warming Potentials":
            params = ui.get_calculation_parameters()
            if params and st.session_state.details_bestaetigt:
                ui.display_calculation_info()
                df, chart = gwp_calculator.calculate_gwp(params)
                if df is not None and chart is not None:
                    gwp_calculator.display_gwp_results(df, chart)
        else:
            chatbot.handle_chat()
#Sorgt dafür das App läuft
if __name__ == "__main__":
    main()




