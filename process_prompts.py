import os
import datetime
import hashlib
import re
import random
import nltk
from nltk.corpus import stopwords

# Pobranie wymaganych zasobów NLTK
def download_nltk_resources():
    nltk.download('stopwords')
    nltk.download('punkt')

# Kluczowe słowa dla tagowania
KEYWORDS = ["AI", "machine learning", "UX", "NLP", "hermeneutics", "philosophy", "automation", "cognition"]

# Katalogi
RAW_PROMPTS_DIR = "raw_prompts/"
PROCESSED_PROMPTS_DIR = "prompts/"

def extract_keywords(prompt_text):
    """Analizuje treść promptu i wybiera tagi na podstawie słów kluczowych."""
    words = re.findall(r'\b\w+\b', prompt_text.lower())  # Tokenizacja
    keywords_found = {word.capitalize() for word in words if word in KEYWORDS}
    
    # Jeśli znaleziono mniej niż 3 tagi, dodaj losowe
    while len(keywords_found) < 3:
        keywords_found.add(random.choice(KEYWORDS))

    return ", ".join(list(keywords_found)[:3])

def generate_filename():
    """Tworzy unikalną nazwę pliku na podstawie daty i hash."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    unique_hash = hashlib.md5(date_str.encode()).hexdigest()[:6]  # Skrócony hash
    return f"{date_str}-prompt-{unique_hash}.md"

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
            prompt_text = file.read().strip()

        if not prompt_text:
            print(f"Pominięto pusty plik: {filename}")
            continue

        title = " ".join(prompt_text.split()[:5]) + "..."  # Pierwsze 5 słów jako tytuł
        date_created = datetime.datetime.now().strftime("%d.%m.%Y")
        tags = extract_keywords(prompt_text)
        file_name = generate_filename()
        repo_link = f"https://github.com/tuPeWu/prompt-repo/blob/main/prompts/{file_name}"

        # Tworzenie katalogu prompts/, jeśli nie istnieje
        os.makedirs(PROCESSED_PROMPTS_DIR, exist_ok=True)

        # Tworzenie nowego pliku w katalogu prompts/
        new_filepath = os.path.join(PROCESSED_PROMPTS_DIR, file_name)
        with open(new_filepath, "w", encoding="utf-8") as new_file:
            new_file.write(f"Tytuł: {title}\n")
            new_file.write(f"Pełna treść: {prompt_text}\n")
            new_file.write(f"Data utworzenia: {date_created}\n")
            new_file.write(f"Tagi: {tags}\n")
            new_file.write(f"Link do repozytorium: {repo_link}\n")

        # Usunięcie przetworzonego pliku
        os.remove(filepath)
        print(f"Przetworzono: {filename} → {new_filepath}")

if __name__ == "__main__":
    download_nltk_resources()
    process_prompts()
