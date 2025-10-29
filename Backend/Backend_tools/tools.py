from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv



def web_searcher(question):
    load_dotenv()
    client = OpenAI()

    
    response = client.responses.create (
        model="gpt-5-nano-2025-08-07",
        reasoning={"effort": "medium"},
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
        
        instructions=
        """
        "system"
        1.Ditt enda syfte är att finna url:s för Porsche-modeller
        2.Du kommer att prioritera de tillåtna domänerna i denna ordning:
        a) porsche.com 
        B) auto-data.net 
        C) caranddriver.com
        MEN om informationen hittats på någon av domänerna, fortsätt inte söka. Skriv alltså ENDAST ut 1 url
        
        3. Ge ingen extra information och ge endast en url per domän.
        4. Skriv endast ut den eller de domäner som information finns tillgänglig på
        5. Hitta inte på url:s som inte finns.

        6. Om det finns flera bilmodeller med det namnet Kan du fråga om ytterligare specifikation.

        """,    
        input=f"{question}",

    )
    print(response.output_text)
    return response.output_text





search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="search the web for information"
)

api_wrapper  = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

