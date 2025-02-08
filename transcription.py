import whisper
import numpy as np

from whisper import load_model, transcribe
from whisper.audio import load_audio

def transcribe_audio(audio):
  model = load_model("medium")
  #audio_path = "/content/bharat.mp3"
  #audio = load_audio(audio_path)
  result = transcribe(model, audio)


  detected_language = result.get("language")
  whisper_to_indictrans2 = {
    "as": "asm_Beng",   # Assamese
    "bn": "ben_Beng",   # Bengali
    "brx": "brx_Deva",  # Bodo
    "doi": "doi_Deva",  # Dogri
    "gu": "guj_Gujr",   # Gujarati
    "hi": "hin_Deva",   # Hindi
    "kn": "kan_Knda",   # Kannada
    "ks": "kas_Arab",   # Kashmiri (Perso-Arabic script)
    "ks_Deva": "kas_Deva",  # Kashmiri (Devanagari script)
    "kok": "kok_Deva",  # Konkani
    "mai": "mai_Deva",  # Maithili
    "ml": "mal_Mlym",   # Malayalam
    "mni": "mni_Beng",  # Manipuri (Bengali script)
    "mni_Mtei": "mni_Mtei",  # Manipuri (Meitei script)
    "mr": "mar_Deva",   # Marathi
    "ne": "nep_Deva",   # Nepali
    "or": "ory_Orya",   # Odia
    "pa": "pan_Guru",   # Punjabi
    "sa": "san_Deva",   # Sanskrit
    "sat": "sat_Olck",  # Santali (Ol Chiki script)
    "sd": "snd_Arab",   # Sindhi (Perso-Arabic script)
    "sd_Deva": "snd_Deva",  # Sindhi (Devanagari script)
    "ta": "tam_Taml",   # Tamil
    "te": "tel_Telu",   # Telugu
    "ur": "urd_Arab"    # Urdu
}
  if detected_language in whisper_to_indictrans2.keys():
    detected_language = whisper_to_indictrans2[detected_language]
  else: 
    return None
  transcription = result.get("text")  # Adjust key if necessary

  return detected_language, transcription

