from openai import OpenAI
from dotenv import load_dotenv
import re

def web_searcher(question, chat_history):
    load_dotenv()
    client = OpenAI()
    context = chat_history
    
  
    
    
    user_context = {
    "role": "user",
    "content": ", ".join(
        i["content"] for i in context[0::2]
    )
    }
        

    Chatbot_context = {
    "role": "assistant",
    "content": ", ".join(
        i["content"] for i in context[1::2]
    )
    }
        

    
    response = client.responses.create (
        
       
        instructions=
        f"""
        Du är en URL-hittare för Porsche-modeller.

        Mål:

        Hitta exakt en (1) giltig URL till en Porsche-modell eller specifik variant som användaren refererar till.

        Kontext:

        - {user_context} innehåller allt användaren tidigare har skrivit.
        - {Chatbot_context} innehåller alla tidigare svar som chatbotten själv har skrivit.
        - {question} är användarens nya fråga.

        Regler:

        1. Använd {user_context} och {Chatbot_context} endast för att förstå användarens tidigare frågor och sammanhang. 
        Gör aldrig antaganden som inte finns där.
        2. Hitta exakt en (1) URL som leder direkt till den modell eller variant som nämns i {question}.
        3. Prioritera domäner i följande ordning:
        a) porsche.com  
        b) auto-data.net  
        c) caranddriver.com/porsche (endast om URL börjar med caranddriver.com/porsche)
        4. Om flera modeller eller varianter kan avses:
        – Ställ EN kort följdfråga för att förtydliga (t.ex. “Menar du 911 Turbo eller 911 Turbo S?”).  
        – Gör ingen sökning innan användaren förtydligar.
        5. Om ingen relevant modell kan identifieras eller om frågan är otydlig:
        – Svara: “Jag förstod inte riktigt vad du menar.”
        6. Om ingen giltig URL hittas på tillåtna domäner:
        – Svara: “Ingen giltig källa hittades.”
        7. Skriv aldrig någon extra text när du väl returnerar en URL.
        8. Be aldrig användaren om att ange exakta årsmodeller eller länkar – endast förtydligande om modellnamn.
        9. Skriv aldrig ut hur du söker eller hur du resonerar.
        10. Stava alltid korrekt, särskilt modellnamn (t.ex. “911 Carrera 4 GTS”, “Panamera Turbo S E-Hybrid”).
        11. Gör inga svar längre än ett stycke(cirka 5 meningar).

        Output-format:

        - Om du hittar en URL: skriv endast länken, utan extra text.
        - Om otydligt: kort följdfråga.
        - Om ogiltig fråga: “Jag förstod inte riktigt vad du menar.”
        - Om ingen giltig domän hittas: “Ingen giltig källa hittades.”
       

        """,    
       
        model="gpt-5-nano-2025-08-07",
        reasoning={"effort": "low"},
        
        tools =[
            {   "type": "web_search",
                "filters": {
                    "allowed_domains": [
                        "porsche.com",
                        "auto-data.net",
                        "caranddriver.com",
                    ]
            },
        }
        ],
        
        
        input=question,
        )
    
    

    Url = response.output_text

    if re.search(r"https?://", Url):
        return {"status": "ok", "Url": Url}
    else:
        return {"status": "clarification", "prompt": Url}
        


    



