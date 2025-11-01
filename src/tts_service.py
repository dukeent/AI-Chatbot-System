"""
Text-to-Speech Service using HuggingFace Transformers
Converts text responses into spoken audio files.
"""
import torch
import soundfile as sf
from transformers import VitsModel, AutoTokenizer
from src import config
from pathlib import Path
from datetime import datetime
import numpy as np
from typing import Optional
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class TTSService:
    """Text-to-Speech service using HuggingFace VITS model."""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize the TTS service.
        
        Args:
            model_name: HuggingFace model name (defaults to config setting)
        """
        print("🔊 Initializing Text-to-Speech Service...")
        
        self.model_name = model_name or config.TTS_MODEL_NAME
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"   Model: {self.model_name}")
        print(f"   Device: {self.device}")
        
        # Load model and tokenizer
        try:
            print("   Loading TTS model (this may take a moment on first run)...")
            self.model = VitsModel.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Move model to appropriate device
            self.model = self.model.to(self.device)  # type: ignore
            
            print("✅ TTS Service initialized successfully")
            
        except Exception as e:
            print(f"❌ Error loading TTS model: {e}")
            print("   The service will continue but audio generation will fail.")
            self.model = None
            self.tokenizer = None
    
    def text_to_speech(
        self, 
        text: str, 
        output_filename: Optional[str] = None,
        save_audio: bool = True,
        play_audio: bool = False
    ) -> Optional[str]:
        """
        Convert text to speech and save as audio file.
        
        Args:
            text: Text to convert to speech
            output_filename: Custom filename (auto-generated if None)
            save_audio: Whether to save the audio file
            play_audio: Whether to play the audio (macOS/Linux only)
            
        Returns:
            Path to the generated audio file, or None if failed
        """
        if self.model is None or self.tokenizer is None:
            print("❌ TTS model not loaded. Cannot generate audio.")
            return None
        
        try:
            # Prepare text - limit length for better quality
            if len(text) > 500:
                print("⚠️  Text is long. Truncating to 500 characters for better audio quality.")
                text = text[:497] + "..."
            
            # Tokenize input text
            inputs = self.tokenizer(text, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate speech
            with torch.no_grad():
                output = self.model(**inputs).waveform
            
            # Convert to numpy array
            audio = output.squeeze().cpu().numpy()
            
            # Normalize audio
            audio = self._normalize_audio(audio)
            
            # Generate filename if not provided
            if output_filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"response_{timestamp}.wav"
            
            # Ensure .wav extension
            if not output_filename.endswith('.wav'):
                output_filename += '.wav'
            
            # Full path
            output_path = Path(config.AUDIO_OUTPUT_PATH) / output_filename
            
            # Save audio file
            if save_audio:
                # Get sample rate from model config
                sample_rate = self.model.config.sampling_rate
                sf.write(str(output_path), audio, sample_rate)
                print(f"🔊 Audio saved to: {output_path}")
            
            # Play audio if requested (macOS/Linux)
            if play_audio:
                self._play_audio(output_path)
            
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return None
    
    def _normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio to prevent clipping.
        
        Args:
            audio: Audio array
            
        Returns:
            Normalized audio array
        """
        max_val = np.abs(audio).max()
        if max_val > 0:
            audio = audio / max_val * 0.95  # Scale to 95% to prevent clipping
        return audio
    
    def _play_audio(self, audio_path: Path):
        """
        Play audio file using system command.
        
        Args:
            audio_path: Path to audio file
        """
        import subprocess
        import platform
        
        try:
            system = platform.system()
            
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", str(audio_path)], check=True)
                print("🔊 Playing audio...")
            elif system == "Linux":
                # Try common Linux audio players
                players = ["aplay", "paplay", "ffplay"]
                for player in players:
                    try:
                        subprocess.run([player, str(audio_path)], check=True)
                        print("🔊 Playing audio...")
                        break
                    except FileNotFoundError:
                        continue
            else:
                print("⚠️  Audio playback not supported on this platform.")
                print(f"   Please play manually: {audio_path}")
                
        except Exception as e:
            print(f"⚠️  Could not play audio: {e}")
            print(f"   Audio file saved at: {audio_path}")
    
    def batch_convert(self, texts: list, prefix: str = "batch") -> list:
        """
        Convert multiple texts to speech.
        
        Args:
            texts: List of text strings to convert
            prefix: Prefix for output filenames
            
        Returns:
            List of generated audio file paths
        """
        print(f"🔊 Converting {len(texts)} texts to speech...")
        
        audio_files = []
        for i, text in enumerate(texts, 1):
            filename = f"{prefix}_{i}.wav"
            audio_path = self.text_to_speech(
                text, 
                output_filename=filename,
                save_audio=True,
                play_audio=False
            )
            if audio_path:
                audio_files.append(audio_path)
                print(f"   ✓ {i}/{len(texts)} completed")
        
        print(f"✅ Batch conversion complete. Generated {len(audio_files)} audio files.")
        return audio_files
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if self.model is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.model_name,
            "device": self.device,
            "sample_rate": self.model.config.sampling_rate,
            "cuda_available": torch.cuda.is_available(),
            "model_params": sum(p.numel() for p in self.model.parameters())
        }
    
    def cleanup_old_files(self, days: int = 7) -> int:
        """
        Remove audio files older than specified days.
        
        Args:
            days: Number of days to keep files
            
        Returns:
            Number of files deleted
        """
        import time
        
        audio_dir = Path(config.AUDIO_OUTPUT_PATH)
        current_time = time.time()
        days_in_seconds = days * 24 * 60 * 60
        
        deleted_count = 0
        
        for audio_file in audio_dir.glob("*.wav"):
            file_age = current_time - audio_file.stat().st_mtime
            if file_age > days_in_seconds:
                audio_file.unlink()
                deleted_count += 1
        
        if deleted_count > 0:
            print(f"🗑️  Cleaned up {deleted_count} old audio files (older than {days} days)")
        
        return deleted_count


def main():
    """Test the TTS service."""
    print("\n" + "="*70)
    print("Text-to-Speech Service - Test Mode")
    print("="*70 + "\n")
    
    # Initialize TTS service
    tts = TTSService()
    
    # Display model info
    print("\n" + "-"*70)
    print("📊 Model Information")
    print("-"*70)
    model_info = tts.get_model_info()
    for key, value in model_info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Test single conversion
    print("\n" + "-"*70)
    print("Test 1: Single Text Conversion")
    print("-"*70)
    
    test_text = "Hello! I am your helpful customer service chatbot. How can I assist you today?"
    print(f"Text: {test_text}")
    
    audio_file = tts.text_to_speech(
        test_text,
        output_filename="test_greeting.wav",
        save_audio=True,
        play_audio=False  # Set to True to hear the audio
    )
    
    if audio_file:
        print(f"✅ Audio generated successfully: {audio_file}")
    
    # Test batch conversion
    print("\n" + "-"*70)
    print("Test 2: Batch Conversion")
    print("-"*70)
    
    batch_texts = [
        "Our business hours are Monday through Friday, 9 AM to 6 PM.",
        "You can reset your password by clicking the forgot password link.",
        "We accept all major credit cards and PayPal for payments."
    ]
    
    batch_files = tts.batch_convert(batch_texts, prefix="test_batch")
    print(f"✅ Generated {len(batch_files)} audio files")
    
    # List generated files
    print("\n" + "-"*70)
    print("📁 Generated Audio Files")
    print("-"*70)
    audio_dir = Path(config.AUDIO_OUTPUT_PATH)
    audio_files = list(audio_dir.glob("*.wav"))
    
    if audio_files:
        for i, file in enumerate(audio_files, 1):
            file_size = file.stat().st_size / 1024  # KB
            print(f"{i}. {file.name} ({file_size:.1f} KB)")
    else:
        print("No audio files found.")
    
    print("\n" + "="*70)
    print("✅ TTS Service test complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
