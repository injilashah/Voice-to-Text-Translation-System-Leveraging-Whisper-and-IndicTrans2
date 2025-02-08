import gradio as gr
from transcription import transcribe_audio
from translation import translate_text
#from transliteration import transliterate_text
import yt_dlp
def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        audio_path = f"temp_audio.mp3"  
    return audio_path
# Function to handle transcription
def process_transcription(audio_file,youtube_url):
  if youtube_url:
    audio_file = download_audio(youtube_url)  # Download YouTube audio
    print(f"Downloaded audio file from YouTube: {audio_file}")
  if not audio_file:
        return None, "No audio provided!"
  print(f"Processing audio file: {audio_file}")  # Debugging output
  detected_lang, transcription = transcribe_audio(audio_file)
  if not transcription:
        return "Error in transcription", None  # Ensure non-empty response

 
  return detected_lang, transcription
  
    
    
    
  

# Function to handle translation
def process_translation(transcription, target_lang, detected_lang):
    if not transcription:
        return "Please transcribe first!", gr.update(interactive=False)
    
    return translate_text(transcription, target_lang, detected_lang)

# Function to handle transliteration
def process_transliteration(translated_text):
    if not translated_text:
        return "Please translate first!"
    #return transliterate_text(translated_text)
    return "hello"
# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🎙️ Voice-to-Text-Translation-System-Leveraging-Whisper-and-IndicTrans2.</h1>")

     

        
    with gr.Column(): 
            gr.Label("🎵 Transcription section") # First column for transcription
            audio_input = gr.Audio(sources =["microphone","upload"],type="filepath", label="Record or Upload Audio 🎤")
            youtube_url = gr.Textbox(label="Enter YouTube Link")
            transcribe_button = gr.Button("Generate Transcription", interactive=True)
            
            detected_language = gr.Textbox(label="Detected Language", interactive=False)
            transcription_output = gr.Textbox(label="Transcription", interactive=False)
       
    with gr.Column():
            gr.Label("## Translation Section")  # Second column for translation
            language_selector = gr.Dropdown([
                'Assamese', 'Bengali', 'Bodo', 'Dogri', 'English','Gujarati', 'Hindi', 'Kannada', 'Kashmiri(Perso-Arabic script)', 
                'Kashmiri(Devanagari script)', 'Konkani', 'Maithili', 'Malayalam', 'Manipuri(Bengali script)', 
                'Manipuri(Meitei script)', 'Marathi', 'Nepali', 'Odia', 'Punjabi', 'Sanskrit', 'Santali(Ol Chiki script)', 
                'Sindhi(Perso-Arabic script)', 'Sindhi(Devanagari script)', 'Tamil', 'Telugu', 'Urdu'
            ], label="Select Target Language")
            translate_button = gr.Button("Generate Translation", interactive=True)
            translation_output = gr.Textbox(label="Translation", interactive=False)
        
    with gr.Column():  # Third column for transliteration
            transliterate_button = gr.Button("Generate Transliteration", interactive=True)
            transliteration_output = gr.Textbox(label="Transliteration", interactive=False)
    
    transcribe_button.click(
        process_transcription, 
        inputs=[audio_input,youtube_url],
        outputs=[detected_language, transcription_output]
        )
    
    translate_button.click(
        process_translation, 
        inputs=[transcription_output, language_selector, detected_language], 
        outputs=[translation_output]
    )
    
    transliterate_button.click(
        process_transliteration, 
        inputs=translation_output, 
        outputs=transliteration_output
    )

# Launch the Gradio App
if __name__ == "__main__":
    demo.launch(share=True, debug=True)
