import whisperx
import torchvision
from config.config import settings
from shared.logging import logger

torchvision.disable_beta_transforms_warning()

class AudioPipeline():
    def __init__(self, audio_file):
        model_config = settings.whisper_worker.whisper_model
        self.batch_size = model_config.batch_size 
        self.compute_type = model_config.compute_type 
        self.device = model_config.compute_type 
        self.model_dir = settings.whisper_worker.local_model_dir 
        self.model_size = model_config.model_size 
        self.result = None
        self.audio_file = audio_file
        self._hf_token = settings.whisper_worker.hf_token 
        self.language = model_config.language
        logger.info("🚀 Initialized AudioPipeline!")

    def transcribe_with_whisper(self):
        logger.info("🎤 Loading Whisper model...")
        model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type, language=self.language)

        if self.model_dir:
            logger.info(f"📂 Using local model directory: {self.model_dir}")
            model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type, download_root=self.model_dir, language=self.language)

        logger.info("🎧 Loading audio file...")
        self.audio = whisperx.load_audio(self.audio_file)

        logger.info("📝 Transcribing audio...")
        self.result = model.transcribe(self.audio, batch_size=self.batch_size)
        logger.info("✅ Transcription complete!")
    
    def align_output(self):
        logger.info("📏 Aligning transcription output...")
        model_a, metadata = whisperx.load_align_model(language_code=self.language, device=self.device)
        self.result = whisperx.align(self.result["segments"], model_a, metadata, self.audio, self.device, return_char_alignments=False)
        logger.info("✅ Alignment complete!")
    
    def assign_speaker_labels(self):
        logger.info("🗣️ Assigning speaker labels...")
        diarize_model = whisperx.DiarizationPipeline(use_auth_token=self._hf_token, device=self.device)

        diarize_segments = diarize_model(self.audio)

        self.result = whisperx.assign_word_speakers(diarize_segments, self.result)
        logger.info("🎭 Speaker identification complete!")
    
    def merge_segments(self):
        logger.info("🧬 Merging segments...")
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
        logger.info("✅ Segment Merging Complete!")
   
    def run_pipeline(self):
        """ Runs the entire pipeline in one method. """
        logger.info("🚀 Starting full audio processing pipeline...")
        self.transcribe_with_whisper()
        self.align_output()
        self.assign_speaker_labels()
        self.merge_segments()
        logger.info("✅ Audio pipeline complete!")
        return self.result

