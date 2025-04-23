"""
Voice interface tools for SuperNova AI.
"""

import os
import base64
import tempfile
from typing import Optional, Dict, Any
from ..config.env import DEBUG

# Check for speech recognition library
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

# Check for text-to-speech library
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

class VoiceInterface:
    """Voice interface for speech recognition and text-to-speech."""

    def __init__(self):
        """Initialize the voice interface."""
        # Initialize speech recognition if available
        self.recognizer = sr.Recognizer() if SPEECH_RECOGNITION_AVAILABLE else None
        
        # Initialize text-to-speech engine if available
        self.tts_engine = None
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Set properties
                self.tts_engine.setProperty('rate', 175)  # Speed
                self.tts_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
                
                # Get available voices
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Try to find a female voice
                    female_voices = [v for v in voices if 'female' in v.name.lower()]
                    if female_voices:
                        self.tts_engine.setProperty('voice', female_voices[0].id)
                    else:
                        # Default to the first voice
                        self.tts_engine.setProperty('voice', voices[0].id)
            except Exception as e:
                if DEBUG:
                    print(f"Error initializing text-to-speech engine: {e}")
                self.tts_engine = None

    def speech_to_text(self, audio_data: bytes) -> Dict[str, Any]:
        """
        Convert speech to text.
        
        Args:
            audio_data: Audio data in bytes
            
        Returns:
            Dictionary containing recognition results
        """
        if not SPEECH_RECOGNITION_AVAILABLE or not self.recognizer:
            return {
                "success": False,
                "error": "Speech recognition is not available. Please install the speech_recognition package."
            }
        
        try:
            # Save audio data to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Recognize speech from the temporary file
            with sr.AudioFile(temp_file_path) as source:
                audio = self.recognizer.record(source)
                
                # Try to recognize with Google (requires internet)
                try:
                    text = self.recognizer.recognize_google(audio)
                    return {
                        "success": True,
                        "text": text,
                        "engine": "google"
                    }
                except sr.RequestError:
                    # If Google fails, try with Sphinx (offline)
                    try:
                        text = self.recognizer.recognize_sphinx(audio)
                        return {
                            "success": True,
                            "text": text,
                            "engine": "sphinx"
                        }
                    except Exception as e:
                        return {
                            "success": False,
                            "error": f"Could not recognize speech: {str(e)}"
                        }
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Could not recognize speech: {str(e)}"
                    }
            
        except Exception as e:
            if DEBUG:
                print(f"Error in speech recognition: {e}")
            return {
                "success": False,
                "error": f"Error in speech recognition: {str(e)}"
            }
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    def text_to_speech(self, text: str, voice: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (if available)
            
        Returns:
            Dictionary containing speech synthesis results
        """
        if not PYTTSX3_AVAILABLE or not self.tts_engine:
            return {
                "success": False,
                "error": "Text-to-speech is not available. Please install the pyttsx3 package."
            }
        
        try:
            # Set voice if specified and available
            if voice:
                voices = self.tts_engine.getProperty('voices')
                matching_voices = [v for v in voices if voice.lower() in v.name.lower()]
                if matching_voices:
                    self.tts_engine.setProperty('voice', matching_voices[0].id)
            
            # Create a temporary file for the audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file_path = temp_file.name
            
            # Generate speech
            self.tts_engine.save_to_file(text, temp_file_path)
            self.tts_engine.runAndWait()
            
            # Read the audio file
            with open(temp_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode("utf-8")
            
            return {
                "success": True,
                "audio_path": temp_file_path,
                "audio_base64": audio_base64,
                "text": text
            }
            
        except Exception as e:
            if DEBUG:
                print(f"Error in text-to-speech: {e}")
            return {
                "success": False,
                "error": f"Error in text-to-speech: {str(e)}"
            }
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

# Create a singleton instance
voice_interface = VoiceInterface()
