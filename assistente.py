import pyttsx3
import speech_recognition as sr
import webbrowser  
import datetime  
import wikipedia
import PyDictionary
import setuptools
import string
from weather import Weather
 
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

# Traduzir para português = "Significa (sua_palavra)"

# Para instalar as dependências do projeto, execute os seguintes comandos no terminal:
    # pip install -r requirements.txt 
    

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
        
        # only get the hour from tuple returned by tellTime() with [0]
        hour = self.tellTime()[0]
        
        if hour > 6 and hour < 12:
            print("Bom dia! O pássaro madrugador pega a minhoca.")
            self.speak("Bom dia! O pássaro madrugador pega a minhoca.")
        elif hour >= 12 and hour < 18:
            print("Boa tarde! O dia está passando rápido.")
            self.speak("Boa tarde! O dia está passando rápido.")
        elif hour >= 18 and hour < 24:
            print("Boa noite! Talvez você durma cedo de uma vez.")
            self.speak("Boa noite! Talvez você durma cedo de uma vez.")
        else:
            print("Estou cansado, chefe.")
            self.speak("Estou cansado, chefe.")
    
    
    def getReady(self):
        print("Pois nao?")
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
        return hour, min   
    
    
    def take_query(self):
        self.greet()
        
        
        start = input("Voce quer falar comigo? (sim/nao): ")
        if start.lower() == "sim":
            self.getReady()
            while True:
                query = self.take_command().lower()
                if "pesquisar" and "wikipedia" in query:
                    self.search_fav_sites(query)
                    continue
                
                elif "qual" and "dia" in query or "que" and "dia" in query:
                    self.tellDay()
                    continue
                
                elif "que" and "horas" in query or "qual" and "horas" in query:
                    hour, min = self.tellTime()
                    print((f"A hora é {hour} e {min} minutos."))
                    self.speak(f"A hora é {hour} e {min} minutos.")   
                    continue
                
                elif "qual" and "seu" and "nome" in query:
                    self.speak("Eu sou Jose Rizal. O seu assistente.")
                    continue

                elif "youtube" in query:
                    self.search_fav_sites(query)
                    continue

                elif "significa" in query or "Significa" in query:
                    
                    query_list = query.lower().split()
                    print(f"Query list: {query_list}")
                    trigger_word = query_list[0]
                    print(f"Trigger word: {trigger_word}")
                    word = query_list[1]
                    self.translate_to_portuguese(word)
                
                
                
                elif "clima" in query or "Clima" in query:
                    
                    # clean up the string and send the keywords to the weather class
                    # translate(str.maketrans) makes translation table that translates punctuation to None
                    query_no_punctuation = query.translate(str.maketrans('', '', string.punctuation))
                    query_list = query_no_punctuation.lower().split()
                    trigger_word = query_list.index("clima")
                    city_name = query_list[trigger_word + 1:]
                    print(city_name)
                    weather_instance = Weather()
                    weather_instance.get_weather(city_name)
                    

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
            # Grab the list items that comes after "youtube"
            # search_terms are then joined to the youtube search URL
            
            # OpenAI will sometimes put in punctuation in the string which was messing up
            # the trigger_word variable. It wasn't finding "youtube" because it was "youtube," in the string.
            # translate(str.maketrans('', '', string.punctuation)) removes punctuation from the string

            sitename_no_punctuation = sitename.translate(str.maketrans('', '', string.punctuation))
            sitename_list = sitename_no_punctuation.lower().split()

            trigger_word = sitename_list.index("youtube")
            search_terms = sitename_list[trigger_word + 1:]
            self.speak(f"Pesquisando o Youtube para {"".join(search_terms)}.")
            webbrowser.open(f"http://www.youtube.com/results?search_query={'+'.join(search_terms)}")
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
        

        dictionary = PyDictionary.PyDictionary()
        translation = dictionary.translate(word, 'pt-BR')
        print(translation.replace(".", ""))
        self.speak(f"{word} significa {translation}")
        
    


if __name__ == '__main__':
    
    assistant = Assistant()
    assistant.take_query()
    
