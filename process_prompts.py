import os
import datetime
import uuid  # Dodajemy do generowania unikalnych nazw
import re
import random
import nltk
from nltk.corpus import stopwords

# Pobranie wymaganych zasobów NLTK
def download_nltk_resources():
    nltk.download('stopwords')
    nltk.download('punkt')

# Rozszerzona lista słów kluczowych dla tagowania
KEYWORDS = set([
    "AI", "machine learning", "UX", "NLP", "hermeneutics", "philosophy", "automation", "cognition",
    "badania UX", "użyteczność", "doświadczenie użytkownika", "projektowanie skoncentrowane na człowieku",
    "projektowanie skoncentrowane na użytkowniku", "heurystyki", "tworzenie szkieletów stron (wireframing)",
    "prototypowanie", "architektura informacji", "obciążenie poznawcze", "przystępność (affordance)",
    "modele mentalne", "persony", "dostępność", "projektowanie inkluzywne", "projektowanie emocjonalne",
    "śledzenie ruchu gałek ocznych", "testowanie użyteczności", "ewaluacja heurystyczna", "ciągłe badania",
    "sortowanie kart", "testy A/B", "badania jakościowe", "badania ilościowe", "etnografia", "grupy fokusowe",
    "ścieżka klienta", "punkty styku", "projektowanie usług", "projektowanie iteracyjne", "projektowanie partycypacyjne",
    "wzorce zachowań", "projektowanie interakcji", "prawo Fittsa", "prawo Hicka", "błędy poznawcze",
    "zmęczenie decyzyjne", "grywalizacja", "projektowanie bez tarcia", "wzorce nawigacyjne", "przystępności",
    "skeumorfizm", "minimalizm", "płaskie projektowanie", "projektowanie ruchu", "projektowanie responsywne",
    "mobilne podejście (mobile-first)", "progresywne ulepszanie", "ciemne wzorce", "nakłanianie (nudging)",
    "mikrointerakcje", "wskaźniki ładowania", "puste stany", "wdrażanie użytkownika (onboarding)",
    "heurystyki użyteczności", "wezwanie do działania (CTA)", "przepływy użytkownika", "utrzymanie klienta",
    "mapowanie usług", "projektowanie perswazyjne", "benchmarki użyteczności", "interakcja człowiek-komputer",
    "rozszerzona rzeczywistość", "wirtualna rzeczywistość", "sztuczna inteligencja", "automatyzacja",
    "UX chatbotów", "interfejsy konwersacyjne", "interfejsy multimodalne", "neurodesign",
    "projektowanie oparte na zachowaniach", "projektowanie etyczne", "prywatność danych", "zgodność z RODO",
    "UX trybu ciemnego", "interfejsy głosowe", "analiza sentymentu", "analiza predykcyjna", "UX writing",
    "czytelność", "rozpoznawalność", "typografia", "współczynniki kontrastu", "komponenty UI",
    "okna modalne", "opinie użytkowników", "mapy cieplne", "tokeny projektowe", "biblioteki komponentów",
    "atomic design", "siatki CSS", "animacje UI", "projektowanie kontekstowe", "mobilna dostępność",
    "analiza zadań", "metryki użyteczności", "empatia klienta", "analiza konkurencji", "wzorce ruchu oczu",
    "współczynniki konwersji", "cyfrowa psychologia", "dowód społeczny", "kluczowe wskaźniki UX (UX KPIs)",
    "mapowanie percepcji", "UX oparty na analizie danych", "badanie kontekstowe", "mapowanie empatii",
    "hierarchia wizualna", "responsywna typografia", "projektowanie modułowe", "projektowanie uniwersalne",
    "strategia treści", "przejście poznawcze", "lepka nawigacja", "zachowania podczas przewijania",
    "interakcje dotykowe", "przejścia UI", "wskaźniki skupienia", "choroba lokomocyjna w VR",
    "agnostycyzm urządzeniowy", "elementy grywalizacji", "testowanie dostępności", "semantyczny HTML",
    "psychologia kolorów", "wielozmysłowy UX", "doświadczenie wielokanałowe", "mapy cieplne śledzenia wzroku"
])

# Katalogi
RAW_PROMPTS_DIR = "raw_prompts/"
PROCESSED_PROMPTS_DIR = "prompts/"

# Stała wartość dla autora promptu
AUTHOR = "Paweł Wolski"

def extract_keywords(prompt_text):
    """Analizuje treść promptu i wybiera słowa-klucze."""
    words = re.findall(r'\b\w+\b', prompt_text.lower())  # Tokenizacja
    keywords_found = {word.capitalize() for word in words if word in KEYWORDS}
    
    # Jeśli znaleziono mniej niż 3 słowa-klucze, dodaj losowe
    while len(keywords_found) < 3:
        keywords_found.add(random.choice(list(KEYWORDS)))
    
    return ", ".join(list(keywords_found)[:3])

def generate_filename():
    """Tworzy unikalną nazwę pliku na podstawie daty i losowego identyfikatora UUID."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    unique_id = uuid.uuid4().hex[:8]  # Krótki unikalny identyfikator
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

        if len(lines) < 2:
            print(f"Pominięto plik {filename}, ponieważ nie zawiera wymaganych danych.")
            continue

        model_ai = lines[0].strip()
        prompt_text = "".join(lines[1:]).strip()
        
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

        os.remove(filepath)
        print(f"Przetworzono: {filename} → {new_filepath}")
