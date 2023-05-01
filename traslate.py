import googletrans
import speech_recognition as sr
from googletrans import Translator
import os
from pydub import AudioSegment
import glob

# geçici .wav dosyalarını sil
for file in glob.glob("temp*.wav"):
    os.remove(file)
# adı verilen mp3 dosyasını tanımla
mp3_file = "Authentication.mp3"

# dosya adını kullanarak metin dosyalarının adlarını oluştur
eng_file = os.path.splitext(mp3_file)[0] + ".txt"
tr_file = os.path.splitext(mp3_file)[0] + "_tr.txt"

# Google Translate API'sine bağlan
translator = Translator(service_urls=['translate.google.com'])

# mp3 dosyasını yükle ve 15 saniyelik parçalara ayır
sound = AudioSegment.from_mp3(mp3_file)
chunk_length_ms = 15000 # 15 saniyelik parçalar için uzunluk
chunks = [sound[i:i+chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]

# parçalardaki transkripsiyonları tutmak için bir liste oluştur
texts = []

# her parçayı işle
for i, chunk in enumerate(chunks):
    # .wav formatına dönüştür ve kaydet
    chunk.export(f"temp{i}.wav", format="wav")

    # ses tanıma işlemi için bir tanıyıcı oluştur
    r = sr.Recognizer()

    # .wav dosyasını yükle
    with sr.AudioFile(f"temp{i}.wav") as source:
        audio = r.record(source)

    # transkripsiyonu yap
    try:
        text = r.recognize_google(audio, language="en-US")
        texts.append(text)
    except sr.RequestError as e:
        print(f"Could not transcribe chunk {i}; {0}".format(e))

# transkripsiyonları birleştir
full_text = " ".join(texts)

# transkripsiyonu metin dosyasına kaydet
with open(eng_file, mode="w", encoding="utf-8") as file:
    file.write(full_text)

# Google Translate ile çeviriyi yap
try:
    # tam metni 5000 karakter parçalarına ayır ve çevir
    translated_parts = []
    for i in range(0, len(full_text), 5000):
        part = full_text[i:i+5000]
        translated = translator.translate(part, dest="tr")
        translated_parts.append(translated.text)
    translated_text = "".join(translated_parts)
except Exception as e:
    print(f"Could not translate text; {0}".format(e))

# çeviriyi tr.txt dosyasına kaydet
with open(tr_file, mode="w", encoding="utf-8") as file:
    file.write(translated_text)

# geçici .wav dosyalarını sil
for file in glob.glob("temp*.wav"):
    os.remove(file)