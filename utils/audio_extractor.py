import os
import subprocess
import speech_recognition as sr

def extract_audio_text(video_path, audio_output='temp_audio.wav', chunk_length=30):
    try:
        recognizer = sr.Recognizer()

        # Remove existing audio file if it exists
        if os.path.exists(audio_output):
            os.remove(audio_output)

        # Extract audio using ffmpeg
        ffmpeg_command = f"ffmpeg -i {video_path} -vn -ar 16000 -ac 1 -b:a 192k -f wav {audio_output}"
        subprocess.run(ffmpeg_command, shell=True, check=True)

        # Use speech recognition to convert audio to text
        full_text = []
        with sr.AudioFile(audio_output) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_sphinx(audio)
                full_text.append(text)
            except sr.UnknownValueError:
                pass  # Skip unrecognized chunks
            except sr.RequestError as e:
                raise Exception(f"Sphinx error; {e}")

        return " ".join(full_text)
    except sr.UnknownValueError:
        raise Exception("Sphinx could not understand the audio")
    except sr.RequestError as e:
        raise Exception(f"Sphinx error; {e}")
    except subprocess.CalledProcessError as e:
        raise Exception(f"ffmpeg error; {e}")
    except Exception as e:
        raise Exception(f"Error extracting audio text: {e}")
