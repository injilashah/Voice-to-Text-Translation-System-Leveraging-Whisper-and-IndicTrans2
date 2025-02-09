import gradio as gr
from transcription import transcribe_audio
from translation import translate_text

from process_yt_video import download_audio,get_embed_url
from create_srt import create_srt
from custom_theme import Seafoam

theme = Seafoam()

# Function to handle transcription
def process_transcription(audio_file, youtube_url):
    if youtube_url:
        audio_file = download_audio(youtube_url)
        print(f"Downloaded audio file from YouTube: {audio_file}")
    
    if not audio_file:
        return None, "No audio provided!", None, None
    
    print(f"Processing audio file: {audio_file}")
    detected_lang, transcription = transcribe_audio(audio_file)
    
    if not transcription:
        return "Error in transcription", None
    
    return detected_lang, transcription

# Function to handle translation
def process_translation(transcription, target_lang, detected_lang):
    if not transcription:
        return "Please transcribe first!", gr.update(interactive=False)
    
    translated_text = translate_text(transcription, target_lang, detected_lang)
    return translated_text

# Function to handle subtitle generation
def process_subtitle(transcription, translation):
    if not transcription or not translation:
        return "Please transcribe and translate first!", None
    
    subtitle_file = create_srt(transcription, translation)
    return "Subtitle generated successfully!", subtitle_file

# Function to handle transliteration
def process_transliteration(translated_text):
    if not translated_text:
        return "Please translate first!"
    return "hello"

# Function to update embedded YouTube video player
def update_video(youtube_url):
    embed_url = get_embed_url(youtube_url)
    return f"<iframe width='560' height='315' src='{embed_url}' frameborder='0' allowfullscreen></iframe>" if embed_url else ""

# Gradio Interface
with gr.Blocks(theme=theme )as demo:
    gr.Markdown("<h1 style='text-align: center;'>🎙️ Voice-to-Text-Translation")
    
    with gr.Row(): 
      with gr.Column():   
         
            gr.Label("🎵 Transcription section",min_width=100,scale=0)
            audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Record or Upload Audio 🎤",scale=0,min_width=100)
            youtube_url = gr.Textbox(label="Enter YouTube Link",scale=0,min_width=100)
            video_player = gr.HTML("")
            youtube_url.change(update_video, inputs=[youtube_url], outputs=[video_player])
        
      with gr.Column():
            transcribe_button = gr.Button("Generate Transcription", interactive=True,scale=0,min_width=300)
            detected_language = gr.Textbox(label="Detected Language", interactive=False,scale=0,min_width=300)
            transcription_output = gr.Textbox(label="Transcription", interactive=False,scale=0,min_width=300)
    
      with gr.Column():
        gr.Label("Translation",min_width=100,scale=0)
        language_selector = gr.Dropdown([
            'Assamese', 'Bengali', 'Bodo', 'Dogri', 'English', 'Gujarati', 'Hindi', 'Kannada', 'Kashmiri(Perso-Arabic script)', 
            'Kashmiri(Devanagari script)', 'Konkani', 'Maithili', 'Malayalam', 'Manipuri(Bengali script)', 
            'Manipuri(Meitei script)', 'Marathi', 'Nepali', 'Odia', 'Punjabi', 'Sanskrit', 'Santali(Ol Chiki script)', 
            'Sindhi(Perso-Arabic script)', 'Sindhi(Devanagari script)', 'Tamil', 'Telugu', 'Urdu'
        ], label="Select Target Language",min_width=100,scale=0)
        translate_button = gr.Button("Generate Translation", interactive=True,min_width=100,scale=0)
        translation_output = gr.Textbox(label="Translation", interactive=False,min_width=100,scale=0)
    
      with gr.Column():
        gr.Label("Subtitle Generation",min_width=100,scale=0)
        subtitle_button = gr.Button("Generate Subtitles", interactive=True,min_width=100,scale=0)
        subtitle_status = gr.Textbox(label="Subtitle Status", interactive=False,min_width=100,scale=0)
        subtitle_download = gr.File(label="Download Subtitles", visible=True,min_width=100,scale=0)
    
    '''with gr.Column():
        transliterate_button = gr.Button("Generate Transliteration", interactive=True)
        transliteration_output = gr.Textbox(label="Transliteration", interactive=False)'''
    
    transcribe_button.click(
        process_transcription, 
        inputs=[audio_input, youtube_url],
        outputs=[detected_language, transcription_output]
    )
    
    translate_button.click(
        process_translation, 
        inputs=[transcription_output, language_selector, detected_language], 
        outputs=[translation_output]
    )
    
    subtitle_button.click(
        process_subtitle, 
        inputs=[transcription_output, translation_output], 
        outputs=[subtitle_status, subtitle_download]
    )
    
    '''transliterate_button.click(
        process_transliteration, 
        inputs=[translation_output], 
        outputs=[transliteration_output]
    )'''

# Launch the Gradio Apps
if __name__ == "__main__":
    demo.launch(share=True, debug=True,pwa=True)
