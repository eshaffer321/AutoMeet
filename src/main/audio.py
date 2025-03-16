import whisperx
import json
import torchvision

torchvision.disable_beta_transforms_warning()

class AudioPipeline():
    def __init__(self, config, audio_file):
        self.batch_size = config['batch_size']
        self.compute_type = config['compute_type']
        self.device = config['device']
        self.model_dir = config.get('local_model_dir', None) 
        self.model_size = config['model_size']
        self.result = None
        self.audio_file = audio_file
        self._hf_token = config['HF_TOKEN']
        self.language = config['language']
        self.output_file = 'output2.json'
        print("🚀 Initialized AudioPipeline!")

    def transcribe_with_whisper(self):
        print("🎤 Loading Whisper model...")
        model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type, language=self.language)

        if self.model_dir:
            print(f"📂 Using local model directory: {self.model_dir}")
            model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type, download_root=self.model_dir, language=self.language)

        print("🎧 Loading audio file...")
        self.audio = whisperx.load_audio(self.audio_file)

        print("📝 Transcribing audio...")
        self.result = model.transcribe(self.audio, batch_size=self.batch_size)
        print("✅ Transcription complete!")
        return self
    
    def align_output(self):
        print("📏 Aligning transcription output...")
        model_a, metadata = whisperx.load_align_model(language_code=self.language, device=self.device)
        self.result = whisperx.align(self.result["segments"], model_a, metadata, self.audio, self.device, return_char_alignments=False)
        print("✅ Alignment complete!")
        return self
    
    def assign_speaker_labels(self):
        print("🗣️ Assigning speaker labels...")
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=self._hf_token, device=self.device)

        diarize_segments = diarize_model(self.audio)

        self.result = whisperx.assign_word_speakers(diarize_segments, self.result)
        print("🎭 Speaker identification complete!")
        return self
    
    def merge_segments(self):
        print("🧬 Merging segments...")
        new_result = []
        current_speaker, current_lines = None, []
        
        for segment in self.result['segments']:
            if 'speaker' not in segment:
                continue
            next_speaker = segment['speaker']
            
            if next_speaker == current_speaker:
                current_lines.append(segment['text'])
            else:
                new_result.append({'speaker': current_speaker, 'text': " ".join(current_lines)})
                current_speaker = next_speaker
                current_lines = [segment['text']]  
        
        # Add the last speaker's lines
        if current_lines:
            new_result.append({'speaker': current_speaker, 'text': " ".join(current_lines)})
        
        self.result = new_result
        print("✅ Segment Merging Complete!")
        return self
    
    def save(self):
        print(f"💾 Saving results to {self.output_file}...")
        with open(self.output_file, "w") as f:
            json.dump(self.result, f, indent=4)
        print("✅ Output saved successfully!")