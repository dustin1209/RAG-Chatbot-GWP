#Festlegen der verwendeten Konstanten 
SYSTEM_MESSAGE = """
Du bist ein spezialisierter Chatbot zur Bewertung von **Deckensystemen** hinsichtlich ihres **Global Warming Potentials (GWP)**.

## Ziel:
- Führe Analysen und strukturierte Vergleiche von Deckensystemen durch.
- Nutze dazu Tools wie Vektorsuche und Vergleichsfunktionen.
"""

GWP_BETON_SZENARIO1 = {
    "C12/15": 129,
    "C16/20": 150,
    "C20/25": 157,
    "C25/30": 181,
    "C30/37": 196,
    "C35/45": 220,
    "C40/50": 0,
    "C45/55": 273,
    "C50/60": 275
}

GWP_HOLZ_SZENARIO1 = {
    "C14": -707.3,
    "C16": -707.3,
    "C18": -707.3,
    "C20": -707.3,
    "C22": -707.3,
    "C24": -707.3,
    "C27": -707.3,
    "C30": -707.3,
    "C35": -707.3,
    "C40": -707.3,
    "GL24h": -677.1,
    "GL28h": -677.1,
    "GL30h": -677.1,
    "GL32h": -677.1,
    "GL36h": -677.1,
    "GL24c": -677.1,
    "GL28c": -677.1,
    "GL30c": -677.1,
    "GL32c": -677.1,
    "GL36c": -677.1
}

GWP_BETON_SZENARIO2 = {
    "C12/15": 147.67,
    "C16/20": 168.67,
    "C20/25": 175.67,
    "C25/30": 199.67,
    "C30/37": 214.67,
    "C35/45": 238.67,
    "C40/50": 0,
    "C45/55": 291.67,
    "C50/60": 293.65
}

GWP_HOLZ_SZENARIO2 = {
    "C14": 77.87,
    "C16": 77.87,
    "C18": 77.87,
    "C20": 77.87,
    "C22": 77.87,
    "C24": 77.87,
    "C27": 77.87,
    "C30": 77.87,
    "C35": 77.87,
    "C40": 77.87,
    "GL24h": 88.893,
    "GL28h": 88.893,
    "GL30h": 88.893,
    "GL32h": 88.893,
    "GL36h": 88.893,
    "GL24c": 88.893,
    "GL28c": 88.893,
    "GL30c": 88.893,
    "GL32c": 88.893,
    "GL36c": 88.893
}

GWP_BETON_SZENARIO3 = {
    "C12/15": 135.57,
    "C16/20": 156.57,
    "C20/25": 163.57,
    "C25/30": 187.57,
    "C30/37": 202.57,
    "C35/45": 226.57,
    "C40/50": 0,
    "C45/55": 279.57,
    "C50/60": 281.5
}

GWP_HOLZ_SZENARIO3 = {
    "C14": -350.23,
    "C16": -350.23,
    "C18": -350.23,
    "C20": -350.23,
    "C22": -350.23,
    "C24": -350.23,
    "C27": -350.23,
    "C30": -350.23,
    "C35": -350.23,
    "C40": -350.23,
    "GL24h": -297.707,
    "GL28h": -297.707,
    "GL30h": -297.707,
    "GL32h": -297.707,
    "GL36h": -297.707,
    "GL24c": -297.707,
    "GL28c": -297.707,
    "GL30c": -297.707,
    "GL32c": -297.707,
    "GL36c": -297.707
}

GWP_STAHL1 = 474 / 1000
GWP_STAHL2 = 477.096 / 1000
GWP_STAHL3 = 825.696 / 1000

GWP_SPANNSTAHL1 = 2913 / 1000
GWP_SPANNSTAHL2 = 2918.443 / 1000
GWP_SPANNSTAHL3 = 1422.443 / 1000

DECKENSYSTEME = [
    "Stahlbetonflachdecke",
    "Spannbetonhohldiele",
    "Holz-Beton-Verbunddecke",
    "Holzbalkendecke"
]

BETONFESTIGKEITSKLASSEN = [
    "C20/25", "C25/30", "C30/37", "C35/45", "C40/50", "C45/55", "C50/60"
]

HOLZFESTIGKEITSKLASSEN = [
    "C14", "C16", "C18", "C24", "C30", "C35", "C40", "GL24h", "GL28h", "GL32h"
] 