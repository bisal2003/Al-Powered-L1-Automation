import os
import wave
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import detect_silence
from groq import Groq

# Audio configuration
RATE = 16000
SILENCE_THRESHOLD_DB = -40  # Adjust based on your environment
MIN_SILENCE_LEN_MS = 1000

def record_audio():
    print("Recording... Press Ctrl+C to stop.")
    
    # Using pydub to record audio
    try:
        audio = AudioSegment.from_file("input.wav")  # Input file (if available)
    except Exception as e:
        print("Error loading audio file:", e)
        return None

    # Playback for confirmation
    print("Playing audio for verification...")
    play(audio)
    
    return audio

def save_audio(audio, filename="audio_segment.wav"):
    """Save audio using pydub."""
    audio.export(filename, format="wav")
    print(f"Saved: {filename}")
    return filename

def detect_silence_and_trim(audio):
    """Detect silence and trim the audio."""
    silence_ranges = detect_silence(audio, min_silence_len=MIN_SILENCE_LEN_MS, silence_thresh=SILENCE_THRESHOLD_DB)
    
    if silence_ranges:
        start, end = silence_ranges[0]
        print(f"Detected silence from {start}ms to {end}ms")
        audio = audio[:start]  # Trim at the first silence
    else:
        print("No silence detected. Saving the entire audio.")
    
    return audio

def speech_to_text(filename):
    if not os.path.isfile(filename):
        print("Audio file not found!")
        return "Error: No audio found."
    
    client = Groq()

    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()), 
            model="whisper-large-v3-turbo", 
            prompt="Specify context or spelling",  
            response_format="json",  
            language="en",  
            temperature=0.0  
        )
        return transcription.text

if __name__ == "__main__":
    audio = record_audio()
    if audio:
        audio = detect_silence_and_trim(audio)
        filename = save_audio(audio)
        print("Transcription:", speech_to_text(filename))
