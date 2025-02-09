import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import sys
import os

# Get the absolute path of IndicTransToolkit
indictrans_path = "/content/Voice-to-Text-Translation-System-Leveraging-Whisper-and-IndicTrans2/IndicTrans2/huggingface_interface/IndicTransToolkit/IndicTransToolkit"
sys.path.append(indictrans_path)

from processor import IndicProcessor

# Check if GPU is available
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def translate_text(transcription, target_lang, src_lang):
    mapping = {
        "Assamese": "asm_Beng", "Bengali": "ben_Beng", "Bodo": "brx_Deva", "Dogri": "doi_Deva",
        "Gujarati": "guj_Gujr", "Hindi": "hin_Deva", "Kannada": "kan_Knda",
        "Kashmiri(Perso-Arabic script)": "kas_Arab", "Kashmiri(Devanagari script)": "kas_Deva",
        "Konkani": "kok_Deva", "Maithili": "mai_Deva", "Malayalam": "mal_Mlym",
        "Manipuri(Bengali script)": "mni_Beng", "Manipuri(Meitei script)": "mni_Mtei",
        "Marathi": "mar_Deva", "Nepali": "nep_Deva", "Odia": "ory_Orya",
        "Punjabi": "pan_Guru", "Sanskrit": "san_Deva", "Santali(Ol Chiki script)": "sat_Olck",
        "Sindhi(Perso-Arabic script)": "snd_Arab", "Sindhi(Devanagari script)": "snd_Deva",
        "Tamil": "tam_Taml", "Telugu": "tel_Telu", "Urdu": "urd_Arab","English":"eng_Latn",
    }
    if target_lang in mapping:
      tgt_lang = mapping[target_lang]
      
    if src_lang == tgt_lang:
      return "Detected Language and Target Language cannot be same"

    if src_lang == "eng_Latn":
      model_name = "prajdabre/rotary-indictrans2-en-indic-1B"
    else:
      model_name ="prajdabre/rotary-indictrans2-indic-en-1B"
        
    
    
    
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    # Load model in 8-bit quantization
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        load_in_8bit=True, 
        attn_implementation="flash_attention_2"
    )  # No `.to(DEVICE)` needed

    ip = IndicProcessor(inference=True)

    input_sentences = [transcription]

    batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=tgt_lang)

    # Tokenize the sentences and generate input encodings
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        return_attention_mask=True
    )

    # Move inputs to the correct device (only inputs, NOT model)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Generate translations using the model
    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            use_cache=True,
            min_length=0,
            max_length=256,
            num_beams=5,
            num_return_sequences=1
        )

    # Move generated tokens to CPU before decoding
    generated_tokens = generated_tokens.cpu().tolist()

    # Decode the generated tokens into text
    with tokenizer.as_target_tokenizer():
        generated_tokens = tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )

    # Postprocess the translations
    translations = ip.postprocess_batch(generated_tokens, lang=tgt_lang)
    print(type(translations))
    translations =str(translations).strip("'")
    return translations
