# Import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QListWidget, QTextEdit, QFileDialog, QLineEdit
import requests
import pyttsx3
import json

# Function to fetch a random word from an external API
def fetch_random_word():
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
        if response.status_code == 200:
            return response.json()[0]
        else:
            return "Error"
    except Exception as e:
        return "Error"

# Function to fetch the definition of a word from an online dictionary API
def fetch_word_definition(word):
    try:
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
        if response.status_code == 200:
            data = response.json()[0]
            definition = data['meanings'][0]['definitions'][0]['definition']
            part_of_speech = data['meanings'][0]['partOfSpeech']
            example = data['meanings'][0]['definitions'][0].get('example', 'No example available.')
            return f"Definition: {definition}\nPart of Speech: {part_of_speech}\nExample: {example}"
        else:
            return "Definition not found"
    except Exception as e:
        return "Error fetching definition"

# Function to initialize text-to-speech engine
def init_tts():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    return engine

# Main app objects and Settings
app = QApplication([])

main_window = QWidget()
main_window.setWindowTitle('Random Word Generator')
main_window.resize(800, 600)

# Create all app objects
title = QLabel('Random Word Generator')
text1 = QLabel("?")
definition1 = QTextEdit()
definition1.setReadOnly(True)
history_list = QListWidget()

button1 = QPushButton('Generate')
button_speak = QPushButton('Speak')
button_save = QPushButton('Save History')
button_load = QPushButton('Load History')
button_clear = QPushButton('Clear History')
search_input = QLineEdit()
search_input.setPlaceholderText('Search for a word...')
button_search = QPushButton('Search')

tts_engine = init_tts()

# All design objects
master_layout = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QVBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()
row5 = QHBoxLayout()

row1.addWidget(title, alignment=Qt.AlignCenter)
row2.addWidget(text1, alignment=Qt.AlignCenter)
row2.addWidget(definition1, alignment=Qt.AlignCenter)
row3.addWidget(button1, alignment=Qt.AlignCenter)
row3.addWidget(button_speak, alignment=Qt.AlignCenter)
row4.addWidget(button_save, alignment=Qt.AlignCenter)
row4.addWidget(button_load, alignment=Qt.AlignCenter)
row4.addWidget(button_clear, alignment=Qt.AlignCenter)
row5.addWidget(search_input, alignment=Qt.AlignCenter)
row5.addWidget(button_search, alignment=Qt.AlignCenter)
row5.addWidget(history_list, alignment=Qt.AlignCenter)

master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)
master_layout.addLayout(row4)
master_layout.addLayout(row5)

main_window.setLayout(master_layout)

# Create all app functions
def generate_word():
    word = fetch_random_word()
    text1.setText(word)
    definition = fetch_word_definition(word)
    definition1.setText(definition)
    history_list.addItem(word)

def speak_word():
    word = text1.text()
    tts_engine.say(word)
    tts_engine.runAndWait()

def save_history():
    options = QFileDialog.Options()
    file, _ = QFileDialog.getSaveFileName(main_window, "Save History", "", "Text Files (*.txt);;All Files (*)", options=options)
    if file:
        with open(file, 'w') as f:
            for i in range(history_list.count()):
                f.write(f"{history_list.item(i).text()}\n")

def load_history():
    options = QFileDialog.Options()
    file, _ = QFileDialog.getOpenFileName(main_window, "Load History", "", "Text Files (*.txt);;All Files (*)", options=options)
    if file:
        history_list.clear()
        with open(file, 'r') as f:
            for line in f:
                history_list.addItem(line.strip())

def clear_history():
    history_list.clear()

def search_word():
    word = search_input.text()
    if word:
        definition = fetch_word_definition(word)
        text1.setText(word)
        definition1.setText(definition)
        history_list.addItem(word)

# Events
button1.clicked.connect(generate_word)
button_speak.clicked.connect(speak_word)
button_save.clicked.connect(save_history)
button_load.clicked.connect(load_history)
button_clear.clicked.connect(clear_history)
button_search.clicked.connect(search_word)

# Style the app
main_window.setStyleSheet("background-color: #f0f0f0;")
title.setStyleSheet('font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;')
text1.setStyleSheet('font-size: 20px; color: #000;')
definition1.setStyleSheet('font-size: 16px; color: #333; background-color: #fff; padding: 10px; border: 1px solid #ccc; border-radius: 5px;')
history_list.setStyleSheet('font-size: 16px; color: #000; background-color: #fff; padding: 10px; border: 1px solid #ccc; border-radius: 5px;')
search_input.setStyleSheet('font-size: 16px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;')

button_style = '''
    font-size: 16px; 
    background-color: #007BFF; 
    color: #FFFFFF; 
    border-radius: 5px; 
    padding: 10px 20px; 
    margin: 5px;
    border: none;
    '''
button1.setStyleSheet(button_style)
button_speak.setStyleSheet(button_style)
button_save.setStyleSheet(button_style)
button_load.setStyleSheet(button_style)
button_clear.setStyleSheet(button_style)
button_search.setStyleSheet(button_style)

# Run APP
main_window.show()
app.exec_()
