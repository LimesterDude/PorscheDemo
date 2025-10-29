from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from Backend_tools.tools import wiki_tool
from Webscraper.scrape import scrape_website, extract_body_content, clean_body_content
from Backend_tools.websearch import web_searcher
import json
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import re
from uuid import uuid4
from typing import Dict, List
from langchain.schema import AIMessage, HumanMessage
# chat_history = sessions.get(session_id, [])

sessions: Dict[str, List[Dict[str, str]]] = {}

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
        allow_origins=[
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://localhost:8000",
            "http://127.0.0.1:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )





@app.get("/")
def root():
    return {"message": "Backend fungerar!"}
@app.post("/api/User_input")
async def User_input(input: str = Body(..., embed = True), session_id: str =Body(...)):
    Fråga = (input or "").strip()

    if not Fråga:
        raise HTTPException(status_code=400, detail="Empty question")
    
    chat_history = sessions.setdefault(session_id, [])
    chat_history.append({"role": "user", "content": Fråga})
    
    Url = web_searcher(Fråga, chat_history)

    if Url["status"] == "clarification":
        svar = Url["prompt"]
        chat_history.append({"role": "assistant", "content": svar})
        sessions[session_id] = chat_history
        
        return {"svar":svar, "session_id": session_id}
    
    if Url["status"] == "ok":
        Url = Url["Url"]


    Resultat = scrape_website(Url)
    Body_content = extract_body_content(Resultat)
    Cleaned_content = clean_body_content (Body_content)



    

    llm = ChatOpenAI(model="gpt-5-nano-2025-08-07")




    # ----------------------------------------Prompts-------------------------------------------------------------------------------------#
    formatted_history = []
    for msg in chat_history[:-1]:
        if msg["role"] == "user":
            formatted_history.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            formatted_history.append(AIMessage(content=msg["content"]))

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
            Du är en hjälpsam assistent som svarar på användarens fråga baserat på 'Cleaned_content'.
            Om du har tillräcklig information, ge ett tydligt svar.
            Om något är oklart, be om EN förtydligande fråga – men inte mer än en gång.
            

        
                """,
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}\n\n{Cleaned_content}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # ----------------------------------------Prompts-------------------------------------------------------------------------------------#


    Payload = {
        "input": Fråga,
        "Cleaned_content": Cleaned_content,
        "chat_history": formatted_history,

    }

  
        
    #-------------------------------------------------AGENT--------------------------------------------------------------------------#

    tools = []
    search_agent = create_tool_calling_agent( 
        llm=llm,
        prompt=answer_prompt,
        tools=tools
    )
    agent_executor = AgentExecutor(agent=search_agent, tools=tools, verbose=False)

    raw_response = await agent_executor.ainvoke(Payload)

    # sessions: Dict[str, List[Dict[str, str]]] = {}
    # chat_history.append({"role": "user", "content": Fråga})
    # chat_history.append({"role": "assistant", "content": chat_history})

    #-------------------------------------------------AGENT--------------------------------------------------------------------------#
    svar = str(raw_response.get("output", ""))
    chat_history.append({"role": "assistant", "content": svar})
    
    # print(raw_response["output"])
    
    
    
    # return {"svar": raw_response["output"]}
    return {"svar": svar, "session_id": session_id}





