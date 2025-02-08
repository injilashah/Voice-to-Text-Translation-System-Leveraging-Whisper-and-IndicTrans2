  
def create_srt(transcription, translated_text):
    srt_content = ""
    for idx, (trans, trans_tr) in enumerate(zip(transcription.split("\n"), translated_text.split("\n"))):
        start_time = f"00:00:{idx:02d},000"
        end_time = f"00:00:{(idx + 1):02d},000"
        srt_content += f"{idx+1}\n{start_time} --> {end_time}\n{trans}\n{trans_tr}\n\n"

    # Save to a file
    subtitle_file = "translated_subtitles.srt"
    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write(srt_content)

    return subtitle_file
    
    