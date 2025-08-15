import streamlit as st
import pandas as pd
import altair as alt
import constants
#Verallgemeinerung des GWP-Rechners
def calculate_gwp(params):
    """Calculates GWP based on material and parameters."""
    material = params["material"]
    
    if material == "Stahlbetonflachdecke":
        return calculate_stahlbetonflachdecke_gwp(params)
    elif material == "Spannbetonhohldiele":
        return calculate_spannbetonhohldiele_gwp(params)
    elif material == "Holz-Beton-Verbunddecke":
        return calculate_holz_beton_verbunddecke_gwp(params)
    elif material == "Holzbalkendecke":
        return calculate_holzbalkendecke_gwp(params)
    return None, None

def calculate_stahlbetonflachdecke_gwp(params):
    volumen = params["dicke_stbflachdecke"] * 1 * 1
    gwp_beton1 = constants.GWP_BETON_SZENARIO1.get(params["festigkeitsklasse"])
    gwp_beton2 = constants.GWP_BETON_SZENARIO2.get(params["festigkeitsklasse"])
    gwp_beton3 = constants.GWP_BETON_SZENARIO3.get(params["festigkeitsklasse"])

    beton_A1A3 = volumen * gwp_beton1
    stahl_A1A3 = params["bewehrungsgrad"] * constants.GWP_STAHL1
    beton_A1A3C = volumen * gwp_beton2
    stahl_A1A3C = params["bewehrungsgrad"] * constants.GWP_STAHL2
    beton_A1A3CD = volumen * gwp_beton3
    stahl_A1A3CD = params["bewehrungsgrad"] * constants.GWP_STAHL3

    df = pd.DataFrame([
        {"Szenario": "A1-A3", "Komponente": "Beton", "GWP": beton_A1A3},
        {"Szenario": "A1-A3", "Komponente": "Stahl", "GWP": stahl_A1A3},
        {"Szenario": "A1-A3+C", "Komponente": "Beton", "GWP": beton_A1A3C},
        {"Szenario": "A1-A3+C", "Komponente": "Stahl", "GWP": stahl_A1A3C},
        {"Szenario": "A1-A3+C/D", "Komponente": "Beton", "GWP": beton_A1A3CD},
        {"Szenario": "A1-A3+C/D", "Komponente": "Stahl", "GWP": stahl_A1A3CD},
    ])
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Szenario:N', title="Szenario"),
        y=alt.Y('GWP:Q', title="GWP [kg CO₂-Äq.]"),
        color=alt.Color('Komponente:N', scale=alt.Scale(domain=["Beton", "Stahl"], range=["#BEBEBE", "#4682B4"])),
        tooltip=['Komponente', 'GWP']
    ).properties(title="Geteiltes Balkendiagramm: Beton vs. Stahl")
    
    return df, chart

def calculate_spannbetonhohldiele_gwp(params):
    volumen_ohnehohlräume = params["dicke_stbhohldiele"] * 1 * 1
    volumen = volumen_ohnehohlräume * (params["anteil_hohlräume"] / 100)
    gwp_beton1 = constants.GWP_BETON_SZENARIO1.get(params["festigkeitsklasse"])
    gwp_beton2 = constants.GWP_BETON_SZENARIO2.get(params["festigkeitsklasse"])
    gwp_beton3 = constants.GWP_BETON_SZENARIO3.get(params["festigkeitsklasse"])

    beton_A1A3 = volumen * gwp_beton1
    spannstahl_A1A3 = params["bewehrungsgrad"] * constants.GWP_SPANNSTAHL1
    beton_A1A3C = volumen * gwp_beton2
    spannstahl_A1A3C = params["bewehrungsgrad"] * constants.GWP_SPANNSTAHL2
    beton_A1A3CD = volumen * gwp_beton3
    spannstahl_A1A3CD = params["bewehrungsgrad"] * constants.GWP_SPANNSTAHL3

    df = pd.DataFrame([
        {"Szenario": "A1-A3", "Komponente": "Beton", "GWP": beton_A1A3},
        {"Szenario": "A1-A3", "Komponente": "Spannstahl", "GWP": spannstahl_A1A3},
        {"Szenario": "A1-A3+C", "Komponente": "Beton", "GWP": beton_A1A3C},
        {"Szenario": "A1-A3+C", "Komponente": "Spannstahl", "GWP": spannstahl_A1A3C},
        {"Szenario": "A1-A3+C/D", "Komponente": "Beton", "GWP": beton_A1A3CD},
        {"Szenario": "A1-A3+C/D", "Komponente": "Spannstahl", "GWP": spannstahl_A1A3CD}
    ])

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Szenario:N', title="Szenario"),
        y=alt.Y('GWP:Q', title="GWP [kg CO₂-Äq.]"),
        color=alt.Color('Komponente:N', scale=alt.Scale(domain=["Beton", "Spannstahl"], range=["#BEBEBE", "#D01313"])),
        tooltip=['Komponente', 'GWP']
    ).properties(title="Geteiltes Balkendiagramm: Beton vs. Spannstahl (SBH)")

    return df, chart

def calculate_holz_beton_verbunddecke_gwp(params):
    volumen_beton = params["dicke_stbhbv"] * 1 * 1
    volumen_holz = params["dicke_holzhbv"] * 1 * 1
    gwp_beton1 = constants.GWP_BETON_SZENARIO1.get(params["festigkeitsklasse"])
    gwp_beton2 = constants.GWP_BETON_SZENARIO2.get(params["festigkeitsklasse"])
    gwp_beton3 = constants.GWP_BETON_SZENARIO3.get(params["festigkeitsklasse"])
    gwp_holz1 = constants.GWP_HOLZ_SZENARIO1.get(params["festigkeitsklasse_holz"])
    gwp_holz2 = constants.GWP_HOLZ_SZENARIO2.get(params["festigkeitsklasse_holz"])
    gwp_holz3 = constants.GWP_HOLZ_SZENARIO3.get(params["festigkeitsklasse_holz"])

    GWP_beton_A1A3 = volumen_beton * gwp_beton1
    GWP_stahl_A1A3 = params["bewehrungsgrad"] * constants.GWP_STAHL1
    GWP_holz_A1A3 = volumen_holz * gwp_holz1
    GWP_beton_A1A3C = volumen_beton * gwp_beton2
    GWP_stahl_A1A3C = params["bewehrungsgrad"] * constants.GWP_STAHL2
    GWP_holz_A1A3C = volumen_holz * gwp_holz2
    GWP_beton_A1A3CD = volumen_beton * gwp_beton3
    GWP_stahl_A1A3CD = params["bewehrungsgrad"] * constants.GWP_STAHL3
    GWP_holz_A1A3CD = volumen_holz * gwp_holz3

    df = pd.DataFrame([
        {"Szenario": "A1-A3", "Komponente": "Beton", "GWP": GWP_beton_A1A3},
        {"Szenario": "A1-A3", "Komponente": "Stahl", "GWP": GWP_stahl_A1A3},
        {"Szenario": "A1-A3", "Komponente": "Holz", "GWP": GWP_holz_A1A3},
        {"Szenario": "A1-A3+C", "Komponente": "Beton", "GWP": GWP_beton_A1A3C},
        {"Szenario": "A1-A3+C", "Komponente": "Stahl", "GWP": GWP_stahl_A1A3C},
        {"Szenario": "A1-A3+C", "Komponente": "Holz", "GWP": GWP_holz_A1A3C},
        {"Szenario": "A1-A3+C/D", "Komponente": "Beton", "GWP": GWP_beton_A1A3CD},
        {"Szenario": "A1-A3+C/D", "Komponente": "Stahl", "GWP": GWP_stahl_A1A3CD},
        {"Szenario": "A1-A3+C/D", "Komponente": "Holz", "GWP": GWP_holz_A1A3CD},
    ])

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Szenario:N', title="Szenario"),
        y=alt.Y('GWP:Q', title="GWP [kg CO₂-Äq.]"),
        color=alt.Color('Komponente:N', scale=alt.Scale(domain=["Beton", "Stahl", "Holz"], range=["#BEBEBE", "#4682B4", "#FD8B01"])),
        tooltip=['Komponente', 'GWP']
    ).properties(title="Geteiltes Balkendiagramm: Beton vs. Stahl vs. Holz")

    return df, chart

def calculate_holzbalkendecke_gwp(params):
    volumen_holz = params["breite_holzbalken"] * params["höhe_holzbalken"] / params["abstand_holzbalken"]
    gwp_holz1 = constants.GWP_HOLZ_SZENARIO1.get(params["festigkeitsklasse_holz"])
    gwp_holz2 = constants.GWP_HOLZ_SZENARIO2.get(params["festigkeitsklasse_holz"])
    gwp_holz3 = constants.GWP_HOLZ_SZENARIO3.get(params["festigkeitsklasse_holz"])

    GWP_holz_A1A3 = volumen_holz * gwp_holz1
    GWP_holz_A1A3C = volumen_holz * gwp_holz2
    GWP_holz_A1A3CD = volumen_holz * gwp_holz3

    df = pd.DataFrame([
        {"Szenario": "A1-A3", "Komponente": "Holz", "GWP": GWP_holz_A1A3},
        {"Szenario": "A1-A3+C", "Komponente": "Holz", "GWP": GWP_holz_A1A3C},
        {"Szenario": "A1-A3+C/D", "Komponente": "Holz", "GWP": GWP_holz_A1A3CD},
    ])

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Szenario:N', title="Szenario"),
        y=alt.Y('GWP:Q', title="GWP [kg CO₂-Äq.]"),
        color=alt.Color('Komponente:N', scale=alt.Scale(domain=["Holz"], range=["#FD8B01"])),
        tooltip=['Komponente', 'GWP']
    ).properties(title="GWP Holzbalkendecke")

    return df, chart

def display_gwp_results(df, chart):
    """Displays the GWP calculation results."""
    st.altair_chart(chart, use_container_width=True) 