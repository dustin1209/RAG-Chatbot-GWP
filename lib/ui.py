
import streamlit as st
import constants
import pandas as pd
import matplotlib.pyplot as plt

#Erezugung der grafischen Benutzeroberfläche

def display_main_page():
    """Displays the main page elements."""
    st.title("Analyse der Umweltwirkung von Deckensystemen im Hochbau")
    st.image("Decken.png", caption="Verschiedene Deckensysteme", use_container_width=True)
    st.write("Möchtest du eine Berechnung des Global Warming Potentials eines Deckensystems  \noder eine Abschätzung anhand vorliegender Literatur?")

def get_user_choice():
    """Gets the user's choice between calculation and estimation."""
    option = st.radio("Bitte auswählen:", (
        "Berechnung des Global Warming Potentials", 
        "Grobe Abschätzung anhand Literatur"
    ))
    if st.button("Auswahl bestätigen"):
        st.session_state.auswahl_bestaetigt = True
    return option

def get_calculation_parameters():
    """Gets the parameters for the GWP calculation."""
    st.header("Randbedingungen für Berechnung")
    material = st.selectbox("Deckensystem", constants.DECKENSYSTEME)
    params = {"material": material}

    if material == "Stahlbetonflachdecke":
        params["festigkeitsklasse"] = st.selectbox("Betonfestigkeitsklasse", constants.BETONFESTIGKEITSKLASSEN)
        params["bewehrungsgrad"] = st.number_input("Bewehrungsmenge eines m\u00B2 Deckenfläche in [t]", min_value=0.0, step=0.01)
        params["dicke_stbflachdecke"] = st.number_input("Deckendicke in [m]", min_value=0.0, step=0.01)
    elif material == "Spannbetonhohldiele":
        params["festigkeitsklasse"] = st.selectbox("Betonfestigkeitsklasse", constants.BETONFESTIGKEITSKLASSEN)
        params["bewehrungsgrad"] = st.number_input("Bewehrungsmenge eines m\u00B2 Deckenfläche in [t]", min_value=0.0, step=0.01)
        params["anteil_hohlräume"] = st.number_input("Anteil der Hohlräume in %", min_value=0.0, step=0.5)
        params["dicke_stbhohldiele"] = st.number_input("Deckendicke in [m]", min_value=0.0, step=0.01)
    elif material == "Holz-Beton-Verbunddecke":
        params["festigkeitsklasse"] = st.selectbox("Betonfestigkeitsklasse", constants.BETONFESTIGKEITSKLASSEN)
        params["bewehrungsgrad"] = st.number_input("Bewehrungsmenge eines m\u00B2 Deckenfläche in [t]", min_value=0.0, step=0.01)
        params["festigkeitsklasse_holz"] = st.selectbox("Holzart/Festigkeitsklasse", constants.HOLZFESTIGKEITSKLASSEN)
        params["dicke_stbhbv"] = st.number_input("Stahlbetonstärke HBV-System in [m]", min_value=0.0, step=0.01)
        params["dicke_holzhbv"] = st.number_input("Stärke der Massivholzplatte HBV-System in [m]", min_value=0.0, step=0.01)
    elif material == "Holzbalkendecke":
        params["festigkeitsklasse_holz"] = st.selectbox("Holzart/Festigkeitsklasse", constants.HOLZFESTIGKEITSKLASSEN)
        params["abstand_holzbalken"] = st.number_input("Abstand der Holzbalken in [m]", min_value=0.0, step=0.01)
        params["breite_holzbalken"] = st.number_input("Breite der Holzbalken in [m]", min_value=0.0, step=0.01)
        params["höhe_holzbalken"] = st.number_input("Höhe der Holzbalken in [m]", min_value=0.0, step=0.01)
    
    if st.button("Berechnen"):
        st.session_state.details_bestaetigt = True
        return params
    return None

def display_calculation_info():
    """Displays information about the GWP calculation."""
    st.markdown("Das Global Warming Potential **[GWP=kg CO2-äq.]** der Deckensysteme wird anhand der DIN-Normen berechnet.  \nDie spezifischen Werte wurden der Ökobaudat **(Average Datensets, Stand 25.06.2025)** entnommen.  \nDie Referenzeinheiten der Baustoffe Beton und Holz werden in Kubikmetern **[m3]** angegeben.  \nDie Referenzeinheiten von Stahl und Spannstahl in Tonnen **[t]**.  \nDie Berechnung erfolgt anhand der Volumina oder dem Gewicht der verwendeten Baustoffe je nach Refernzeinheit.")

def render_chat_message(sender, message):
    """Displays a chat message."""
    if sender == "user":
        st.markdown(
            f"""
            <div style="
                background-color:#DCF8C6; 
                padding:10px; 
                border-radius:15px; 
                max-width:70%; 
                margin-left:auto; 
                margin-bottom:5px;">
                <b>Du:</b> {message}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            f"""
            <div style="
                background-color:#E6E6E6; 
                padding:10px; 
                border-radius:15px; 
                max-width:70%; 
                margin-right:auto; 
                margin-bottom:5px;">
                <b>Bot:</b> {message}
            </div>
            """, unsafe_allow_html=True)

def display_chatbot_info():
    """Displays information about the chatbot."""
    st.markdown("""
    ## 💬 Chatbot-Funktionen

    Du hast die Möglichkeit, mit einem **Chatbot** zu kommunizieren.  
    Der Chatbot nutzt zwei Methoden:

    1. 🧠 **RAG-System**:  
       Auf Benutzeranfrage gibt der Chatbot die ähnlichsten Textstellen aus der vorhandenen Literaturbasis aus.

    2. ⚖️ **Vergleich des GWP (in kgCO₂-äq.)**:  
       Der Chatbot ermöglicht den Vergleich des **Global Warming Potentials** in Abhängigkeit von:
       - der **Spannweite** (zwischen 3 und 12 m)
       - der **Nutzlast** (zwischen 1 und 10 kN/m²)  
         
       Um diese Funktion zu nutzen, übergebe dem Chatbot:
       - das Wort **"Vergleich"**  
       - sowie Werte für **Spannweite** und **Nutzlast** im angegebenen Bereich in Schritten= **1m** oder **1kN/m2**.
    """)

def get_chatbot_input():
    """Gets the user's input for the chatbot."""
    return st.text_input("Was möchtest du wissen?") 

def plot_vergleich(data):
    df = pd.DataFrame(data)
    normierte_werte = df["GWP_predicted"].values / df["GWP_predicted"].max()
    farben = plt.cm.RdYlGn_r(normierte_werte)

    fig, ax = plt.subplots(figsize=(18, 9))
    bars = ax.bar(df["Deckensystem"], df["GWP_predicted"], color=farben)
    ax.set_ylabel("GWP [kg CO₂-eq/m²]", fontsize=16)
    ax.set_xlabel("Deckensystem", fontsize=16)
    ax.set_title("Vorhergesagte GWP-Werte pro Deckensystem (rot = hoch, grün = niedrig)", fontsize=20)
    ax.set_xticklabels(df["Deckensystem"], rotation=45, ha='right')

    for bar in bars:
        höhe = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, höhe, f'{höhe:.2f}', ha='center', va='bottom', fontsize=16)

    st.pyplot(fig)
    plt.close(fig)
