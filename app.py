import gradio as gr
from transcription import transcribe_audio
from translation import translate_text
#from transliteration import transliterate_text

# Function to handle transcription
def process_transcription(audio_file):
    detected_lang,transcription = transcribe_audio(audio_file)
    if detected_language:
        return detected_lang,transcription
    else:
        return None
# Function to handle translation
def process_translation(transcription, target_lang,detected_lang):
    if not transcription:
        return "Please transcribe first!"
    return translate_text(transcription, target_lang,detected_lang)

# Function to handle transliteration
#def process_transliteration(translated_text):
    if not translated_text:
        return "Please translate first!"
    return transliterate_text(translated_text)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️Speech to Text")
    
    with gr.Row():
        audio_input = gr.Audio(type="filepath", label="Upload Audio File 🎵")
        transcription_output = gr.Textbox(label="Transcription", interactive=False)
        detected_language= gr.Textbox(label ="Detected Language",interactive=False)
    transcribe_button = gr.Button("Generate Transcription")
    
    with gr.Row():
        language_selector = gr.Dropdown(['Assamese', 'Bengali', 'Bodo', 'Dogri', 'Gujarati', 'Hindi', 'Kannada', 'Kashmiri(Perso-Arabic script)', 'Kashmiri(Devanagari script)', 'Konkani', 'Maithili', 'Malayalam', 'Manipuri(Bengali script)', 'Manipuri(Meitei script)', 'Marathi', 'Nepali', 'Odia', 'Punjabi', 'Sanskrit', 'Santali(Ol Chiki script)', 'Sindhi(Perso-Arabic script)', 'Sindhi(Devanagari script)', 'Tamil', 'Telugu', 'Urdu'], label="Select Target Language")
        translation_output = gr.Textbox(label="Translation", interactive=False)

    translate_button = gr.Button("Generate Translation")

    #with gr.Row():
        #transliteration_output = gr.Textbox(label="Transliteration", interactive=False)

    #transliterate_button = gr.Button("Generate Transliteration")

    # Button Click Events
    transcribe_button.click(process_transcription, inputs=audio_input, outputs=[detected_language,transcription_output])
    translate_button.click(process_translation, inputs=[transcription_output, language_selector,detected_language], outputs=translation_output)
    #transliterate_button.click(process_transliteration, inputs=translation_output, outputs=transliteration_output)

# Launch the Gradio App
if __name__ == "__main__":
    demo.launch(share=True , debug = True)
