import pyttsx3
import speech_recognition as sr
import webbrowser  
import datetime  
import wikipedia
import PyDictionary
import setuptools
 
 
dictionary = PyDictionary.PyDictionary()

 

# Comandos:

# Pesquisar artigo na Wikipédia = "Pesquisar na Wikipedia (sua_palavra)"

# Pesquisar no Youtube = "Youtube (suas_termos_de_pesquisa)"

# Qual é o dia de hoje? = Contanto que você tenha as palavras-chave 
# "qual" e "dia" ou "que" e "dia", isso acionará a função tellDay()

# Que horas são? = Contanto que você tenha as palavras-chave "que" e "horas", ou 
# "qual" e "horas", isso acionará a função tellTime()

# Qual é o seu nome? = Contanto que você tenha as palavras-chave "qual", "seu" e "nome",
# isso acionará a função greet()

# Saia do programa = "Tchau"
# A programa vai continuar rodando até que você diga "Tchau".

# Significa ainda não está funcionando.

# Para instalar as dependências do projeto, execute os seguintes comandos no terminal:
    # pip install -r requirements.txt 
    # pip install --upgrade pyaudio
    # pip install setuptools 
    # pip install numpy 
    # pip install soundfile 
    # pip install torch 
    # pip install openai-whisper =
    # Para instalar as dependências do projeto

# Para atualizar o projeto, execute os seguintes comandos no terminal:
    # git fetch --all
    # git reset --hard origin/master


class Assistant:

    def __init__(self):
        
        # voices[2] appears to be the Brazilian Portuguese voice from my localization files
        # muito bem

        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[2].id)


    def speak(self, audio):
        
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
        self.engine.say(audio)  
        self.engine.runAndWait()
    
    def take_command(self):
        r = sr.Recognizer()
        
        with sr.Microphone() as source:
            print('Escutando...')
            r.pause_threshold = 0.7
            audio = r.listen(source)
            
            try:
                print("Analisando...")
                Query = r.recognize_whisper(audio, language='portuguese')
                print("Utilizador disse: ", Query.lower())
                
            except Exception as error:
                print(error)
                print("Como?")
                return "None"
            
        return Query
    
     
    def greet(self):
        self.speak("Pois nao?")
    


    def tellDay(self):
        
        day = datetime.datetime.today().weekday() + 1
        day_dict = {1: 'segunda-feira', 2: 'terca-feira', 
                    3: 'quarta-feira', 4: 'quinta-feira', 
                    5: 'sexta-feira', 6: 'sabado',
                    7: 'domingo'}
        
        day_of_the_week = day_dict.get(day)
        
        if day_of_the_week:
            print(f"Hoje e {day_of_the_week}.")
            self.speak(f"Hoje e {day_of_the_week}.")
    
    
    def tellTime(self):
        
        current_time = datetime.datetime.now()
        print(str(current_time))
        hour = current_time.hour
        min = current_time.minute
        self.speak(f"A hora é {hour} e {min} minutos.")   
    
    
    def take_query(self):
        self.greet()
        
        
        start = input("Voce quer falar comigo? (sim/nao): ")
        if start.lower() == "sim":
            while True:
                query = self.take_command().lower()
                if "pesquisar" and "wikipedia" in query:
                    self.search_fav_sites(query)
                    continue
                
                elif "qual" and "dia" in query or "que" and "dia" in query:
                    self.tellDay()
                    continue
                
                elif "que" and "horas" in query or "qual" and "horas" in query:
                    self.tellTime()
                    continue
                
                elif "qual" and "seu" and "nome" in query:
                    self.speak("Eu sou Jose Rizal. O seu assistente.")
                    continue

                elif "youtube" in query:
                    self.search_fav_sites(query)
                    continue

                elif "significa" in query or "Significa" in query:
                    
                    # For some reason the indexes of the query are not cooperating
                    # I can't do the [trigger_word + 1] to get the target word
                    # It keeps giving me a list out of range error

                    query_list = query.lower().split()
                    print(f"Query list: {query_list}")
                    trigger_word = query_list[0]
                    print(f"Trigger word: {trigger_word}")
                    word = query_list[1]
                    self.translate_to_portuguese(word)
                
                elif "tchau" in query:
                    
                    self.speak("Tchau, tchau!")
                    break

                else:
                    self.speak("Desculpe, não entendi o que você quis dizer")
                    continue
        
        elif start.lower() == "nao": 
            print("Que tristeza :(")
            return
        
        else:
            print("Por favor, responda com sim ou nao.")
            return
        
       
                
                
    def search_fav_sites(self, sitename):
            
        if "youtube" in sitename:
                
            # Index of youtube is found in the string.
            # This grabs the list item that comes after "youtube"
            # Hopefully this is a good way to keep it working once we start
            # taking more user input.
            
            search = sitename.lower().split().index("youtube")
            search_term = sitename.split()[search + 1:]
            self.speak(f"Pesquisando o Youtube para {"".join(search_term)}.")
            webbrowser.open(f"http://www.youtube.com/results?search_query={'+'.join(search_term)}")
            return

        if "pesquisar" and "wikipedia" in sitename:
            
            # Trigger words "pesquisar" and "wikipedia" are removed from the string
            # Leaving search term only, then the string is passed to the portuguese wikipedia 
            # search URL
            sitename = sitename.replace(",", "")
            wikipedia.set_lang("pt")
            sitename_list = sitename.lower().split()
            index_of_wikipedia = sitename_list.index("wikipedia")
            search_terms = sitename_list[index_of_wikipedia + 1:]
            
            self.speak(f"Pesquisando por wikipedia {"".join(search_terms)} ")
            print(f"Pesquisando por wikipedia {"".join(search_terms)}.")
            webbrowser.open(f"https://pt.wikipedia.org/wiki/Special:Search?search={"_".join(search_terms)}")
            return
            
    def translate_to_portuguese(self, word):
        
        # The code is working as it should I think but it keeps giving invalid word error
        # I think the problem is with the PyDictionary library and its translation.

        dictionary = PyDictionary.PyDictionary()
        translation = dictionary.translate(word, 'pt-BR')
        print(translation.replace(".", ""))
        self.speak(f"{word} significa {translation}")
        



if __name__ == '__main__':
    
    assistant = Assistant()
    assistant.take_query()