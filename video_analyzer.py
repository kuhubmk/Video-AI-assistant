import os
import json
import requests
import torch
import whisper

class VideoAnalyzer:
    def __init__(self, api_key, secret_key, ffmpeg_path, text_for_summarization):
        self.api_key = api_key
        self.secret_key = secret_key
        self.ffmpeg_path = ffmpeg_path
        self.text_for_summarization = text_for_summarization

        # Ensure ffmpeg path is added to environment variable
        os.environ['PATH'] += os.pathsep + ffmpeg_path

        # Whisper model initialization
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.whisper_model = whisper.load_model("small", device=self.device)

    def get_access_token(self):
        """
        Get access token using API Key and Secret Key
        """
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(url, headers=headers)
        response_data = response.json()
        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            raise Exception("Failed to get access_token: ", response_data)

    def transcribe_audio(self, audio_path):
        """
        Transcribe audio using Whisper
        """
        try:
            result = self.whisper_model.transcribe(audio_path)
            transcript = result["text"]
            return transcript
        except Exception as e:
            print(f"Audio transcription failed: {e}")
            return ""

    def summarize_text_baidu(self, text):
        """
        Summarize text using Baidu Wenxin API
        """
        try:
            access_token = self.get_access_token()
            url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

            payload = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": f"{self.text_for_summarization}:\n\n{text}"
                    }
                ]
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            result = response.json()
            if 'result' in result:
                summary = result['result']
                return summary
            else:
                return "Summary failed"
        except Exception as e:
            print(f"Text summarization failed: {e}")
            return "Summary failed"

    def process_audio(self, audio_path):
        try:
            base_audio_name = os.path.splitext(os.path.basename(audio_path))[0]
            compare_suffix = base_audio_name[-5:]  # Get last 5 characters from the right

            # Create subfolder in Analyze_notes based on the audio's subfolder
            analyze_subfolder = os.path.join("Analyze_notes", os.path.basename(os.path.dirname(audio_path)))
            if not os.path.exists(analyze_subfolder):
                os.makedirs(analyze_subfolder)

            # Check if notes file already exists
            existing_notes = os.listdir(analyze_subfolder)
            notes_already_exist = False
            print(f"Checking notes for {audio_path} in {analyze_subfolder}: {existing_notes}")
            for existing_note in existing_notes:
                if existing_note.endswith(compare_suffix + ".txt"):
                    print(f"Notes already exist for {audio_path}. Skipping.")
                    notes_already_exist = True
                    break

            if not notes_already_exist:
                print(f"Processing {audio_path}")
                transcript = self.transcribe_audio(audio_path)
                if not transcript:
                    print("Transcription text generation failed")
                    return False

                summary = self.summarize_text_baidu(transcript)
                print(f"Text summarization completed: {summary}")

                notes_file_name = f"{base_audio_name}.txt"
                notes_file_path = os.path.join(analyze_subfolder, notes_file_name)

                with open(notes_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Audio file: {audio_path}\n\n")
                    f.write(f"Transcript:\n{transcript}\n\n")
                    f.write(f"Summary:\n{summary}\n")

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def create_audio_notes(self, root_folder):
        """
        Create notes for all MP3 audio files in the specified root folder and its subfolders, skipping those already processed.
        """
        try:
            if not os.path.exists(root_folder):
                raise FileNotFoundError(f"Root folder {root_folder} does not exist.")
            
            notes_list = []
            if not os.path.exists("Analyze_notes"):
                os.makedirs("Analyze_notes")

            for subdir, _, files in os.walk(root_folder):
                for file in files:
                    if file.endswith(".mp3"):
                        audio_path = os.path.join(subdir, file)
                        result = self.process_audio(audio_path)
                        if result:
                            notes_list.append(audio_path)

            return notes_list

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    # Specify the root folder containing the downloaded audio files
    root_folder = "downloaded_audio"

    API_KEY = config.get("API_KEY", "")
    SECRET_KEY = config.get("SECRET_KEY", "")
    ffmpeg_path = config.get("ffmpeg_path", "")
    text_for_summarization = config.get("text_for_summarization", "")

    # Create an instance of VideoAnalyzer
    analyzer = VideoAnalyzer(API_KEY, SECRET_KEY, ffmpeg_path, text_for_summarization)

    # Create audio notes
    notes = analyzer.create_audio_notes(root_folder)

    if notes:
        print("Audio files processed successfully:")
        for note in notes:
            print(f"Processed: {note}")
    else:
        print("Failed to process audio files.")
import os
import json
import requests
import torch
import whisper

class VideoAnalyzer:
    def __init__(self, api_key, secret_key, ffmpeg_path, text_for_summarization):
        self.api_key = api_key
        self.secret_key = secret_key
        self.ffmpeg_path = ffmpeg_path
        self.text_for_summarization = text_for_summarization

        # Ensure ffmpeg path is added to environment variable
        os.environ['PATH'] += os.pathsep + ffmpeg_path

        # Whisper model initialization
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.whisper_model = whisper.load_model("small", device=self.device)

    def get_access_token(self):
        """
        Get access token using API Key and Secret Key
        """
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.post(url, headers=headers)
        response_data = response.json()
        if 'access_token' in response_data:
            return response_data['access_token']
        else:
            raise Exception("Failed to get access_token: ", response_data)

    def transcribe_audio(self, audio_path):
        """
        Transcribe audio using Whisper
        """
        try:
            result = self.whisper_model.transcribe(audio_path)
            transcript = result["text"]
            return transcript
        except Exception as e:
            print(f"Audio transcription failed: {e}")
            return ""

    def summarize_text_baidu(self, text):
        """
        Summarize text using Baidu Wenxin API
        """
        try:
            access_token = self.get_access_token()
            url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token={access_token}"

            payload = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": f"{self.text_for_summarization}:\n\n{text}"
                    }
                ]
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            result = response.json()
            if 'result' in result:
                summary = result['result']
                return summary
            else:
                return "Summary failed"
        except Exception as e:
            print(f"Text summarization failed: {e}")
            return "Summary failed"

    def process_audio(self, audio_path):
        try:
            base_audio_name = os.path.splitext(os.path.basename(audio_path))[0]
            compare_suffix = base_audio_name[-5:]  # Get last 5 characters from the right

            # Create subfolder in Analyze_notes based on the audio's subfolder
            analyze_subfolder = os.path.join("Analyze_notes", os.path.basename(os.path.dirname(audio_path)))
            if not os.path.exists(analyze_subfolder):
                os.makedirs(analyze_subfolder)

            # Check if notes file already exists
            existing_notes = os.listdir(analyze_subfolder)
            notes_already_exist = False
            print(f"Checking notes for {audio_path} in {analyze_subfolder}: {existing_notes}")
            for existing_note in existing_notes:
                if existing_note.endswith(compare_suffix + ".txt"):
                    print(f"Notes already exist for {audio_path}. Skipping.")
                    notes_already_exist = True
                    break

            if not notes_already_exist:
                print(f"Processing {audio_path}")
                transcript = self.transcribe_audio(audio_path)
                if not transcript:
                    print("Transcription text generation failed")
                    return False

                summary = self.summarize_text_baidu(transcript)
                print(f"Text summarization completed: {summary}")

                notes_file_name = f"{base_audio_name}.txt"
                notes_file_path = os.path.join(analyze_subfolder, notes_file_name)

                with open(notes_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Audio file: {audio_path}\n\n")
                    f.write(f"Transcript:\n{transcript}\n\n")
                    f.write(f"Summary:\n{summary}\n")

            return True

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def create_audio_notes(self, root_folder):
        """
        Create notes for all MP3 audio files in the specified root folder and its subfolders, skipping those already processed.
        """
        try:
            if not os.path.exists(root_folder):
                raise FileNotFoundError(f"Root folder {root_folder} does not exist.")
            
            notes_list = []
            if not os.path.exists("Analyze_notes"):
                os.makedirs("Analyze_notes")

            for subdir, _, files in os.walk(root_folder):
                for file in files:
                    if file.endswith(".mp3"):
                        audio_path = os.path.join(subdir, file)
                        result = self.process_audio(audio_path)
                        if result:
                            notes_list.append(audio_path)

            return notes_list

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    # Specify the root folder containing the downloaded audio files
    root_folder = "downloaded_audio"

    API_KEY = config.get("API_KEY", "")
    SECRET_KEY = config.get("SECRET_KEY", "")
    ffmpeg_path = config.get("ffmpeg_path", "")
    text_for_summarization = config.get("text_for_summarization", "")

    # Create an instance of VideoAnalyzer
    analyzer = VideoAnalyzer(API_KEY, SECRET_KEY, ffmpeg_path, text_for_summarization)

    # Create audio notes
    notes = analyzer.create_audio_notes(root_folder)

    if notes:
        print("Audio files processed successfully:")
        for note in notes:
            print(f"Processed: {note}")
    else:
        print("Failed to process audio files.")
