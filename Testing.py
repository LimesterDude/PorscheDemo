from pyscript import display, document
def chatbot_input2(Fråga):
    Fråga = document.querySelector("#chatbot_input2").value
    
    if not Fråga or not Fråga.strip():
        display("skriv något först", target = "out")
        return
    
    display(f"Du skrev: {Fråga}", target = "out")
    document.querySelector("#chatbot_input2").value =""