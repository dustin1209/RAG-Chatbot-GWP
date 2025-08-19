import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from langchain.agents import tool
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from typing import Annotated
import os
from lib import constants
from lib import ui
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()


#Tool-Vektorsuche erstellen
@tool
def vector_search(query: Annotated[str, "Anfrage an die Vektordatenbank"]) -> str:
    """Durchsuche die Vekordatenbank nach Vektoren, die der Nutzeranfrage am ähnlichsten sind."""
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})
    vectorstore = FAISS.load_local("Schritt3.-FAISS-Vectorstore", embedding_model, allow_dangerous_deserialization=True)
    # Vektorsuche anahnd der 5 ähnlichsten Ergebnisse
    results = vectorstore.similarity_search(query, k=5)

    docs_text = "\n\n".join([res.page_content for res in results])
    # Formulierung der Antwort anhand der 5 Dokumente
    prompt = f"""Du bist ein sachkundiger KI-Assistent. Beantworte Fragen ausschließlich auf Basis der folgenden Dokumentauszüge. 
    Antworte klar, präzise und verständlich. Wenn die Dokumente keine ausreichenden Informationen liefern, sage: "Keine ausreichenden Informationen in den Dokumenten vorhanden.
    
    Dokumente:
    {docs_text}

    Frage: {query}

    Antwort:"""
#Festlegung LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    response = llm.chat([
        {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
        {"role": "user", "content": prompt}
    ])
    #Ausgabe
    return response.content

#Tool-Vergleiche Deckensysteme
@tool
def vergleiche_deckensysteme(spannweite: Annotated[float, "Spannweite des Einfeldträgers in m"], nutzlast: Annotated[float, "Nutzlast in kN/m²"]) -> str:
    """Du bekommst die Spannweite und die Nutzlast eines Einfeldträger-Deckensystems übergeben und sollst einen Vergleich der Umweltwirkung, spezifischer dem GWP dieser schaffen.Um dem Nutzer einen besseren Überblick zu verscahffen sortierst du die Werte in absteigender Reihenfolge und markierst sie von rot nach grün. wenn möglich zeige dem Nutzer ein Balkendiagrammpython.Du gibst das GWP in kg CO2-äq./m2 aus."""
    #Versuch Auslesen der Werte Spannweite und Nutzlast
    try:    
        spannweite = float(str(spannweite).replace(',', '.'))
        nutzlast = float(str(nutzlast).replace(',', '.'))
    except Exception:
        return "❌ Ungültiger Wert für Spannweite oder Nutzlast."
    #Auslesen der Datei
    dateipfad = "Schritt6.2.-DataFrame-ExcelTabellen/Predictions_Lineare_Regression_Gewichtet.xlsx"
    prediction_daten = pd.read_excel(dateipfad)
    prediction_daten.columns = prediction_daten.columns.str.strip()

    bedingungen = [
        prediction_daten['Nutzlast'] == nutzlast,
        prediction_daten['Spannweite'] == spannweite
    ]
    gesamt_bedingung = bedingungen[0]
    for bed in bedingungen[1:]:
        gesamt_bedingung &= bed
    #Ausgabe der Daten des DataFrames anhand der Parameter Spannweite und Nutzlast für jedes Deckensystem
    ergebnis = prediction_daten[gesamt_bedingung]

    if ergebnis.empty:
        return f"Keine passenden Deckensysteme für Spannweite {spannweite} m und Nutzlast {nutzlast} kN/m² gefunden."
    #Sortiere die Ergebnisse anhand der Größe und gebe die Daten an das LLM
    ergebnis_sortiert = ergebnis.sort_values(by="GWP_predicted", ascending=False)

    ergebnis_sortiert["GWP_predicted"] = ergebnis_sortiert["GWP_predicted"].round(0).astype(int)

    relevante_spalten = ['Deckensystem', 'GWP_predicted', 'Spannweite', 'Nutzlast']
    ergebnis_dict = ergebnis_sortiert[relevante_spalten].to_dict(orient="records")

    return {"data": ergebnis_dict}
    
 
#Agent-Executor initieren und Tools übergeben
def get_agent_executor():
    """Initializes the LangChain agent."""
    if "agent_executor" not in st.session_state:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY"))
        
        tools = [vector_search, vergleiche_deckensysteme]
        memory = MemorySaver()
        st.session_state.agent_executor = create_react_agent(llm, tools, checkpointer=memory, system_message=constants.SYSTEM_MESSAGE)
    return st.session_state.agent_executor
#Funktion Chat-Handling- Chatverlauf und Ausgabe des Bots initieren
def handle_chat():
    """Handles the chatbot interaction."""
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "main_thread"
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    agent_executor = get_agent_executor()
    ui.display_chatbot_info()
    user_input = ui.get_chatbot_input()
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    if user_input:
        st.session_state.chat_history.append(("user", user_input))
        try:
            bot_response = ""
            for step in agent_executor.stream({"messages": [("user", user_input)]}, config=config, stream_mode="values"):
                if "messages" in step and step["messages"]:
                    bot_response = step["messages"][-1].content
            
        except Exception as e:
            bot_response = f"❌ Fehler bei der Antwort: {e}"
        st.session_state.chat_history.append(("bot", bot_response))

    st.write("---")
    for sender, message in st.session_state.chat_history:
        ui.render_chat_message(sender, message)