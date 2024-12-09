from bs4 import BeautifulSoup
from gensim.summarization import summarize
from rouge import Rouge
import newspaper


def ekstrakArtikel(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()
    return article.text

def inputTeksPanjang():
    chunks = []
    print("Ketik atau paste kan teksmu di bawah ini. Tekan Ctrl+D (untuk Unix/Linux) atau Ctrl+Z (untuk Windows) di ikuti dengan Enter untuk menyelesaikan:")
    print("")
    try:
        while True:
            chunk = input()
            chunks.append(chunk)
    except EOFError:
        pass

    return '\n'.join(chunks)

def ringkasanByTeks(text):
    hasilRingkasan = summarize(text)
    return hasilRingkasan

def ringkasanByURL(teks):
    soup = BeautifulSoup(teks, 'html.parser')
    text = soup.get_text()
    hasilRingkasan = ringkasanByTeks(text)
    return hasilRingkasan

def ringkasanByFile(filepath):
    with open(filepath, 'r') as file:
        text = file.read()
        hasilRingkasan = ringkasanByTeks(text)
        return hasilRingkasan

def tingkatPresisi(teksAsli, hasilRingkasan):
    rouge = Rouge()
    scores = rouge.get_scores(hasilRingkasan, teksAsli)
    return scores[0]

input_type = input("\n 1. URL\n 2. File\n 3. Teks\n\nMasukkan angka berdasarkan sumber teks: ")

if input_type == "1":
    url = input("Masukkan URL: ")
    teksAsli = ekstrakArtikel(url)
    hasilRingkasan = ringkasanByURL(teksAsli)
elif input_type == "2":
    filepath = input("Masukkan filepath: ")
    with open(filepath, 'r') as file:
        teksAsli = file.read()
    hasilRingkasan = ringkasanByFile(filepath)
elif input_type == "3":
    teksAsli = inputTeksPanjang()
    hasilRingkasan = ringkasanByTeks(teksAsli)
else:
    print("Inputan salah. Exit.")
    exit()

print("\n==================== ORIGINAL TEXT ====================")
print(teksAsli)
print("\n==================== SUMMARIZED TEXT ====================")
print(hasilRingkasan)
print("\n==================== ROUGE SCORES ====================")

# Calculate Rouge scores
rouge_scores = tingkatPresisi(teksAsli, hasilRingkasan)

print(f"Rouge-1 Precision: {rouge_scores['rouge-1']['p']}")
print(f"Rouge-1 Recall: {rouge_scores['rouge-1']['r']}")
print(f"Rouge-1 F1 Score: {rouge_scores['rouge-1']['f']}")
print(f"Rouge-2 Precision: {rouge_scores['rouge-2']['p']}")
print(f"Rouge-2 Recall: {rouge_scores['rouge-2']['r']}")
print(f"Rouge-2 F1 Score: {rouge_scores['rouge-2']['f']}")
print(f"Rouge-L Precision: {rouge_scores['rouge-l']['p']}")
print(f"Rouge-L Recall: {rouge_scores['rouge-l']['r']}")
print(f"Rouge-L F1 Score: {rouge_scores['rouge-l']['f']}")