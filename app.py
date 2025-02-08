import gradio as gr
from transcription import transcribe_audio
from translation import translate_text

from process_yt_video import download_audio,get_embed_url
from create_srt import create_srt



# Function to handle transcription
def process_transcription(audio_file,youtube_url):
  if youtube_url:
        audio_file= download_audio(youtube_url)
        print(f"Downloaded audio file from YouTube: {audio_file}")  # Download YouTube video
        
  if not audio_file:
    return None, "No audio provided!", None, None
  print(f"Processing audio file: {audio_file}")

  detected_lang, transcription = transcribe_audio(audio_file)
  if not transcription:
        return "Error in transcription", None  # Ensure non-empty response

  return detected_lang, transcription


  

# Function to handle translation
def process_translation(transcription, target_lang, detected_lang):
    if not transcription:
        return "Please transcribe first!", gr.update(interactive=False)
    
    translated_text=translate_text(transcription, target_lang, detected_lang)
    # Generate subtitle file# Generate subtitle file
    subtitle_file = create_srt(transcription, translated_text)
    return translated_text, subtitle_file

# Function to handle transliteration
def process_transliteration(translated_text):
    if not translated_text:
        return "Please translate first!"
    #return transliterate_text(translated_text)
    return "hello"
# Function to update embedded YouTube video player
def update_video(youtube_url):
    embed_url = get_embed_url(youtube_url)
    return f"<iframe width='560' height='315' src='{embed_url}' frameborder='0' allowfullscreen></iframe>" if embed_url else ""

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🎙️ Voice-to-Text-Translation")

     

    with gr.Row():    
      with gr.Column(): 
            gr.Label("🎵 Transcription section") # First column for transcription
            audio_input = gr.Audio(sources =["microphone","upload"],type="filepath", label="Record or Upload Audio 🎤")
            youtube_url = gr.Textbox(label="Enter YouTube Link")
            video_player = gr.HTML("")
            youtube_url.change(update_video, inputs=[youtube_url], outputs=[video_player])
    with gr.Column():
      
      transcribe_button = gr.Button("Generate Transcription", interactive=True)
            
      detected_language = gr.Textbox(label="Detected Language", interactive=False)
      transcription_output = gr.Textbox(label="Transcription", interactive=False)
    

       
    with gr.Column():
            gr.Label("Translation")  # Second column for translation
            language_selector = gr.Dropdown([
                'Assamese', 'Bengali', 'Bodo', 'Dogri', 'English','Gujarati', 'Hindi', 'Kannada', 'Kashmiri(Perso-Arabic script)', 
                'Kashmiri(Devanagari script)', 'Konkani', 'Maithili', 'Malayalam', 'Manipuri(Bengali script)', 
                'Manipuri(Meitei script)', 'Marathi', 'Nepali', 'Odia', 'Punjabi', 'Sanskrit', 'Santali(Ol Chiki script)', 
                'Sindhi(Perso-Arabic script)', 'Sindhi(Devanagari script)', 'Tamil', 'Telugu', 'Urdu'
            ], label="Select Target Language")
            translate_button = gr.Button("Generate Translation", interactive=True)
            translation_output = gr.Textbox(label="Translation", interactive=False)
            subtitle_download = gr.File(label="Download Subtitles", visible=False)
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
        outputs=[translation_output,subtitle_download]
    )
    
    transliterate_button.click(
        process_transliteration, 
        inputs=translation_output, 
        outputs=transliteration_output
    )

# Launch the Gradio App
if __name__ == "__main__":
    demo.launch(share=True, debug=True)
