import os
import datetime
import uuid
import re
import nltk
from collections import Counter
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
import string

# Pobranie wymaganych zasobów NLTK
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('stopwords')

download_nltk_resources()

# Katalogi
RAW_PROMPTS_DIR = "raw_prompts/"
PROCESSED_PROMPTS_DIR = "prompts/"

# Stała wartość dla autora promptu
AUTHOR = "Paweł Wolski"

def extract_keywords(prompt_text):
    """Analizuje treść promptu i wybiera 3 najczęstsze rzeczowniki występujące co najmniej 2 razy."""
    words = word_tokenize(prompt_text.lower())
    words = [word for word in words if word.isalnum() and word not in stopwords.words('english')]
    tagged_words = pos_tag(words)
    
    # Wybór tylko rzeczowników (NN, NNS, NNP, NNPS)
    nouns = [word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS"]]
    
    # Liczenie wystąpień rzeczowników
    word_counts = Counter(nouns)
    
    # Wybór 3 najczęstszych rzeczowników występujących co najmniej 2 razy
    common_nouns = [word.capitalize() for word, count in word_counts.items() if count >= 2][:3]
    
    return ", ".join(common_nouns)

def generate_filename():
    """Tworzy unikalną nazwę pliku na podstawie daty i losowego identyfikatora UUID."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    unique_id = uuid.uuid4().hex[:8]
    return f"{date_str}-prompt-{unique_id}.md"

def process_prompts():
    """Przetwarza pliki w katalogu raw_prompts/"""
    if not os.path.exists(RAW_PROMPTS_DIR):
        print("Katalog raw_prompts nie istnieje.")
        return

    if not os.listdir(RAW_PROMPTS_DIR):
        print("Brak plików do przetworzenia.")
        return

    for filename in os.listdir(RAW_PROMPTS_DIR):
        filepath = os.path.join(RAW_PROMPTS_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if not lines:
            print(f"Pominięto pusty plik: {filename}")
            continue

        # Sprawdzenie, czy plik ma pierwszą linię z modelem AI
        if len(lines) >= 2:
            model_ai = lines[0].strip()
            prompt_text = "".join(lines[1:]).strip()
        else:
            model_ai = "Nieznany model AI"
            prompt_text = lines[0].strip()
        
        if not prompt_text:
            print(f"Pominięto pusty plik: {filename}")
            continue
        
        title = " ".join(prompt_text.split()[:5]) + "..."
        date_created = datetime.datetime.now().strftime("%d.%m.%Y")
        tags = extract_keywords(prompt_text)
        file_name = generate_filename()
        repo_link = f"https://github.com/tuPeWu/prompt-repo/blob/main/prompts/{file_name}"
        
        os.makedirs(PROCESSED_PROMPTS_DIR, exist_ok=True)
        
        new_filepath = os.path.join(PROCESSED_PROMPTS_DIR, file_name)
        with open(new_filepath, "w", encoding="utf-8") as new_file:
            new_file.write(f"Autor promptu: {AUTHOR}\n")
            new_file.write(f"Wykorzystany model AI: {model_ai}\n")
            new_file.write(f"Krótki tytuł: {title}\n")
            new_file.write(f"Pełna treść promptu: {prompt_text}\n")
            new_file.write(f"Data wygenerowania: {date_created}\n")
            new_file.write(f"Słowa-klucze: {tags}\n")
            new_file.write(f"Link do repozytorium GitHub: {repo_link}\n")

        if os.path.exists(new_filepath):
            print(f"Plik poprawnie zapisany: {new_filepath}")
            os.remove(filepath)
        else:
            print(f"Błąd: Nie udało się zapisać pliku {new_filepath}")

        print("### DEBUG: Sprawdzanie wygenerowanych plików ###")
        print("Zawartość katalogu prompts/:")
        for file in os.listdir(PROCESSED_PROMPTS_DIR):
            print(file)
