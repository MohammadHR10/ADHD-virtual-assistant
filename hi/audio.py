import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import sounddevice as sd
import numpy as np

class SpeechRecognition:
    def __init__(self):
        # Initialize Whisper model (tiny version for minimal resource usage)
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
        self.sample_rate = 16000
        self.duration = 10  # seconds

    def record_and_transcribe(self):
        print("Recording...")
        # Record audio
        recording = sd.rec(int(self.duration * self.sample_rate), 
                        samplerate=self.sample_rate, 
                        channels=1)
        sd.wait()
        #print("Processing...")
        
        # Convert to format expected by Whisper
        audio_array = recording.flatten()
        
        # Process with Whisper
        input_features = self.processor(
        audio_array,
        sampling_rate=self.sample_rate,
        return_tensors="pt",
        language="en"
        ).input_features

        
        # Generate transcription
        predicted_ids = self.model.generate(input_features)
        
        # Decode transcription
        transcription = self.processor.batch_decode(
            predicted_ids, 
            skip_special_tokens=True
        )[0]
        
        return transcription
    
# Export instance so frontend can import it
speech_recognition = SpeechRecognition()


