import speech_recognition as sr
from gtts import gTTS
import smtplib
import pywhatkit
import email
import datetime
import pyowm
import webbrowser
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
import pyaudio





'''funçao capaz de ouvir e transcrever comandos de voz'''
def ouvir():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language='pt-br')
        print("Você disse: " + comando)
    except sr.UnknownValueError:
        print("Não entendi o que você disse")
    except sr.RequestError as e:
        print("Erro ao processar sua solicitação; {0}".format(e))
    
    return comando


'''funçao para enviar email'''
def enviar_email(destinatario, assunto, mensagem):
    remetente = 'Seu_Email.com'
    senha = 'Sua_Senha'
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remetente, senha)
    servidor.sendmail(remetente, destinatario, f'Subject: {assunto}\n\n{mensagem}')
    servidor.quit()
    print('E-mail enviado com sucesso!')



'''função para mandar mensgem pelo zap'''
def enviar_mensagem_whatsapp(destinatario, mensagem, hora, minuto):
    pywhatkit.sendwhatmsg(destinatario, mensagem, hora, minuto)
    print('Mensagem enviada com sucesso!')



# Chama a função ouvir() para ouvir e transcrever o comando de voz do usuário
comando = ouvir()

# Verifica se o usuário pediu para enviar um e-mail
if 'enviar e-mail' in comando:
    # Solicita ao usuário o destinatário, o assunto e o corpo da mensagem
    destinatario = input("Digite o destinatário: ")
    assunto = input("Digite o assunto: ")
    mensagem = input("Digite a mensagem: ")
    
    # Chama a função enviar_email() para enviar o e-mail
    enviar_email(destinatario, assunto, mensagem)




owm = pyowm.OWM('sua_chave_de_API_aqui')  # Substitua 'sua_chave_de_API_aqui' pela sua chave de API da OpenWeatherMap

def previsao_do_tempo():
    try:
        cidade = input("Qual é a sua cidade? ")
        obs = owm.weather_at_place(cidade)
        w = obs.get_weather()
        temperatura = w.get_temperature('celsius')['temp']
        status = w.get_detailed_status()
        print(f"A temperatura em {cidade} é de {temperatura:.1f}°C. O tempo está {status}.")
    except:
        print("Desculpe, não consegui obter a previsão do tempo.")

import webbrowser
import pywhatkit
import os

def executar_comando(comando):
    if 'tocar música' in comando:
        # Insira o caminho do diretório onde suas músicas estão armazenadas
        music_dir = 'C:\\Users\\Usuário\\Música'
        # Seleciona uma música aleatória do diretório e a reproduz
        os.chdir(music_dir)
        songs = os.listdir()
        os.startfile(songs[random.randint(0, len(songs)-1)])

    elif 'abrir site' in comando:
        # Solicita ao usuário o site que deseja abrir
        site = input("Qual site você deseja abrir? ")
        # Abre o site no navegador padrão
        webbrowser.open(site)

    elif 'procurar na internet' in comando:
        # Solicita ao usuário o termo de pesquisa
        termo = input("O que você deseja pesquisar? ")
        # Abre o navegador padrão e pesquisa o termo no Google
        pywhatkit.search(termo)

    else:
        print("Desculpe, não entendi o comando")


def pesquisar_google(comando):
    # Separa o comando em termos individuais, eliminando a palavra "pesquisar"
    termos_pesquisa = comando.split()[1:]
    # Transforma os termos de pesquisa em uma string única, separada por espaços
    termos_pesquisa = " ".join(termos_pesquisa)
    # Usa a biblioteca pywhatkit para pesquisar no Google
    pywhatkit.search(termos_pesquisa)
    print("Pesquisa realizada com sucesso!")


# Exemplo de conjunto de dados de treinamento
treinamento = [
    {'input': 'Olá', 'output': 'Olá! Como posso ajudar?'},
    {'input': 'Qual é a previsão do tempo para hoje?', 'output': 'Não sei, mas posso procurar para você.'},
    {'input': 'Lembre-me de comprar pão', 'output': 'Certo, vou lembrar você de comprar pão.'},
    {'input': 'Onde fica o restaurante mais próximo?', 'output': 'Eu não sei, mas posso pesquisar para você.'},
    {'input': 'Como está o trânsito agora?', 'output': 'Não tenho essa informação, mas posso buscar.'}
]

# Função para treinar o assistente
def treinar_assistente(treinamento):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB

    # Extrai as entradas e saídas do conjunto de treinamento
    entradas = [exemplo['input'] for exemplo in treinamento]
    saidas = [exemplo['output'] for exemplo in treinamento]

    # Cria um vetorizador de palavras
    vetorizador = CountVectorizer()

    # Transforma as entradas em vetores de recursos
    entradas_vetorizadas = vetorizador.fit_transform(entradas)

    # Treina um classificador Naive Bayes com os vetores de recursos e as saídas
    classificador = MultinomialNB()
    classificador.fit(entradas_vetorizadas, saidas)

    return classificador, vetorizador

# Chama a função de treinamento para obter o classificador e o vetorizador
classificador, vetorizador = treinar_assistente(treinamento)

# Exemplo de uso do classificador treinado
nova_entrada = 'Qual é a cotação do dólar hoje?'
nova_entrada_vetorizada = vetorizador.transform([nova_entrada])
nova_saida = classificador.predict(nova_entrada_vetorizada)

print(nova_saida)
