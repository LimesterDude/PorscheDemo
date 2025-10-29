import json, asyncio
from pyscript import document, display
from pyodide.http import pyfetch

async def on_submit(event=None):
    if event: 
        event.preventDefault()
        
    element = (document.querySelector("#chatbot_input"))
    out = document.querySelector("#out") #här kommer out att vara något värde som finns i autoreply funktionen
    
    query = (element.value or "").strip()
    if not query:
        out.textContent = "skriv något först!"
        return
    
    out.textContent = "Bearbetar..."
    resp = await pyfetch(
        url="/api/ask"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        body = json.dumps({"Fråga": query})
    )

    if not resp.ok:
        out.textContent = f"Serverfel {resp.status}"
        return
    
    data = await resp.json
    out.textContent = data.get("Fråga", "(inget svar)")

    element.value= ""
    element.focus()

document.querySelector("#chat-form").addEventLister("submit", on_submit) #Tror något annat värde än "submit ska stå där"
