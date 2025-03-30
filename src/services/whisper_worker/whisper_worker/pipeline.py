from math import log
import whisperx
from config.config import settings
from shared.util.logging import logger

class AudioPipeline():
    def __init__(self, audio_file):
        model_config = settings.whisper_worker.whisper_model # type: ignore
        self.batch_size = model_config.batch_size # type: ignore 
        self.compute_type = model_config.compute_type # type: ignore 
        self.device = model_config.device # type: ignore 
        self.model_dir = settings.whisper_worker.local_model_dir # type: ignore 
        self.model_size = model_config.model_size # type: ignore 
        self.result = None
        self.audio_file = audio_file
        self._hf_token = settings.whisper_worker.hf_token # type: ignore 
        self.language = model_config.language  # type: ignore
        logger.info(f"🚀 Initialized AudioPipeline with device: {self.device}, model: {self.model_size}, compute type: {self.compute_type}, batch size: {self.batch_size}")

    def transcribe_with_whisper(self):
        logger.info("🎤 Loading Whisper model...")

        if self.model_dir:
            logger.info(f"📂 Using local model directory: {self.model_dir}")
            model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type, download_root=self.model_dir, language=self.language)
        else:
            model = whisperx.load_model(self.model_size, self.device, compute_type=self.compute_type, language=self.language)

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
        diarize_segments = diarize_model(self.audio, min_speakers=2, max_speakers=10)

        self.result = whisperx.assign_word_speakers(diarize_segments, self.result)
        logger.info("🎭 Speaker identification complete!")
    
    def merge_segments(self):
        """
        Merges consecutive segments spoken by the same speaker.
        Each merged segment includes combined text and start/end timestamps.
        """
        logger.info("🧬 Merging segments...")

        merged, buffer = [], []
        speaker, start_ts, end_ts = None, None, None

        def flush_buffer():
            if buffer:
                merged.append({
                    'speaker': speaker,
                    'text': " ".join(buffer),
                    'start': start_ts,
                    'end': end_ts
                })

        for seg in self.result['segments']:
            seg_speaker = seg.get('speaker')
            seg_text = seg.get('text', '').strip()
            seg_start = seg.get('start')
            seg_end = seg.get('end')

            if not seg_speaker or not seg_text:
                logger.info(f"⚠️ Skipping segment {seg}")
                continue

            if seg_speaker == speaker:
                buffer.append(seg_text)
                end_ts = seg_end
            else:
                flush_buffer()
                speaker = seg_speaker
                buffer = [seg_text]
                start_ts = seg_start
                end_ts = seg_end

        flush_buffer()
        logger.info("✅ Segment merging complete.")
        return merged
    
    def calculate_duration(self):
        """ Calculates the total duration of the audio file. """
        start_timestamp = self.result['segments'][0]['start']
        end_timestamp = self.result['segments'][-1]['end']
        duration = end_timestamp - start_timestamp
        logger.info(f"⏱️ Total duration: {duration} seconds")
        return duration
    
    def create_metadata(self):
        """ Adds metadata to the result. """
        logger.info("📝 Creating metadata for the result...")
        duration = self.calculate_duration()
        metadata = {
            'language': self.language,
            'model_size': self.model_size,
            'batch_size': self.batch_size,
            'compute_type': self.compute_type,
            'device': self.device,
            'duration': duration,
        }
        return metadata

   
    def run_pipeline(self):
        """ Runs the entire pipeline in one method. """
        logger.info("🚀 Starting full audio processing pipeline...")
        self.transcribe_with_whisper()
        self.align_output()
        self.assign_speaker_labels()
        merged_results = self.merge_segments()
        metadata = self.create_metadata()

        self.result = {
            'transcription': self.result,
            'metadata': metadata,
        }

        merged_results = {
            'transcription': merged_results,
            'metadata': metadata,
        }

        logger.info("✅ Audio pipeline complete!")
        return self.result, merged_results

