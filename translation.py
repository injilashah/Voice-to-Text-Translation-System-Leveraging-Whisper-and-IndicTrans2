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
      model1_name ="prajdabre/rotary-indictrans2-indic-en-1B"
      model2_name = "prajdabre/rotary-indictrans2-en-indic-1B"
      translations = indic_indic(model1_name,model2_name, src_lang, target_lang,transcription)
      return translations 
    
    
    
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    # Load model in 8-bit quantization
    model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        #load_in_8bit=True, 
        attn_implementation="flash_attention_2"
    ).to(DEVICE)

    ip = IndicProcessor(inference=True)

    input_sentences = [transcription]

    batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=tgt_lang)

    
    # Tokenize the sentences and generate input encodings
    inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        max_length=2048,
        
    )

    # Move inputs to the correct device (only inputs, NOT model)
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Generate translations using the model
    with torch.inference_mode():
        generated_tokens = model.generate(
            **inputs,
            num_beams=5,
        length_penalty=1.5,
        repetition_penalty=2.0,
        num_return_sequences=1,
        max_new_tokens=2048,
        early_stopping=True
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
def indic_indic(model1_name,model2_name,src_lang,tgt_lang,transcription,intermediate_lng ="eng_Latn",):
  tokenizer = AutoTokenizer.from_pretrained(model1_name, trust_remote_code=True)

    # Load model in 8-bit quantization
  model = AutoModelForSeq2SeqLM.from_pretrained(
        model1_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        #load_in_8bit=True, 
        attn_implementation="flash_attention_2"
    ).to(DEVICE)

  ip = IndicProcessor(inference=True)

  input_sentences = [transcription]

  batch = ip.preprocess_batch(input_sentences, src_lang=src_lang, tgt_lang=intermediate_lng)

    # Tokenize the sentences and generate input encodings
  inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        max_length=2048,
    )

    # Move inputs to the correct device (only inputs, NOT model)
  inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Generate translations using the model
  with torch.inference_mode():
        generated_tokens = model.generate(
            **inputs,
            num_beams=10,
        length_penalty=1.5,
        repetition_penalty=2.0,
        num_return_sequences=1,
        max_new_tokens=2048,
        early_stopping=True
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
  translations1 = ip.postprocess_batch(generated_tokens, lang=tgt_lang)
  
  translations1 =str(translations).strip("'")
  tokenizer = AutoTokenizer.from_pretrained(model2_name, trust_remote_code=True)

    # Load model in 8-bit quantization
  model = AutoModelForSeq2SeqLM.from_pretrained(
        model2_name,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        #load_in_8bit=True, 
        attn_implementation="flash_attention_2"
    ).to(DEVICE)

  ip = IndicProcessor(inference=True)

  input_sentences = [translations1]

  batch = ip.preprocess_batch(input_sentences, src_lang=intermediate_lng, tgt_lang=tgt_lang)

    # Tokenize the sentences and generate input encodings
  inputs = tokenizer(
        batch,
        truncation=True,
        padding="longest",
        return_tensors="pt",
        max_length=2048,
    )

    # Move inputs to the correct device (only inputs, NOT model)
  inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Generate translations using the model
  with torch.inference_mode():
        generated_tokens = model.generate(
            **inputs,
            num_beams=10,
        length_penalty=1.5,
        repetition_penalty=2.0,
        num_return_sequences=1,
        max_new_tokens=2048,
        early_stopping=True
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
  

  return translations

