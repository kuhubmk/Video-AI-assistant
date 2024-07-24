import os
import json
import requests
import logging
import concurrent.futures
import re 

class DouyinVideoDownloader:
    def __init__(self, json_folder='downloaded_json', download_folder='downloaded_audio', urls_folder='download_urls'):
        self.json_folder = json_folder
        self.download_folder = download_folder
        self.urls_folder = urls_folder
        self.json_files = None
        self.current_json_index = 0
        self.counter = 1  # Initialize counter for audio numbering
        self.downloaded_files = set()  # Track downloaded files
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def load_json_files(self):
        self.json_files = [f for f in os.listdir(self.json_folder) if f.endswith('.json')]
        if not self.json_files:
            self.logger.info("No JSON files found in the downloaded_json folder.")
        else:
            self.logger.info(f"Found {len(self.json_files)} JSON files.")
    
    def load_next_json_data(self):
        if not self.json_files:
            self.load_json_files()
        
        if self.current_json_index >= len(self.json_files):
            self.logger.info("All JSON files processed.")
            return None
        
        json_file_path = os.path.join(self.json_folder, self.json_files[self.current_json_index])
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.current_json_index += 1
        return data
    
    def fetch_audio_url(self, music_info):
        play_url = music_info.get('play_url', {}).get('uri')
        return play_url
    
    def download_audio(self, filename, url, save_folder):
        try:
            audio_name = f"{self.counter}_{filename}.mp3"
            save_path = os.path.join(self.download_folder, save_folder)
            os.makedirs(save_path, exist_ok=True)
            filepath = os.path.join(save_path, audio_name)
            
            # Check if the audio has already been downloaded
            if audio_name in self.downloaded_files:
                self.logger.info(f"{audio_name} already downloaded, skipping.")
                return
            
            audio_response = requests.get(url, stream=True)
            audio_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in audio_response.iter_content(chunk_size=8096):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Downloaded {audio_name}")
            self.downloaded_files.add(audio_name)
            self.counter += 1  # Increment counter for next audio
        except requests.RequestException as req_e:
            self.logger.error(f"Error downloading audio {url}: {req_e}")
        except Exception as e:
            self.logger.error(f"Error saving audio file {filename}: {e}")
    
    def process_video(self, video, folder_name):
        video_name = video['desc']
        music_info = video['music']
        play_url = self.fetch_audio_url(music_info)
        
        if play_url:
            short_name = re.sub(r'[<>:"/\\|?*]', '_', video_name[8:18] if len(video_name) > 8 else video_name)
            filename = f"{self.counter}_{short_name}"
            folder_path = os.path.join(self.urls_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            filepath = os.path.join(folder_path, f"{filename}.txt")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(play_url)
                self.logger.info(f"Download URL saved to {filepath}")
            
            return (filename, play_url, folder_name)
        
        return None
    
    def download_audios_concurrently(self):
        self.load_json_files()  # Load JSON files initially
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                audio_urls_futures = []
                
                while True:
                    data = self.load_next_json_data()
                    if not data:
                        break
                    
                    json_filename = self.json_files[self.current_json_index - 1]
                    folder_name = os.path.splitext(json_filename)[0]
                    videos = data['data']['aweme_list']
                    
                    for video in videos:
                        audio_urls_futures.append(executor.submit(self.process_video, video, folder_name))
                
                download_futures = []
                for future in concurrent.futures.as_completed(audio_urls_futures):
                    result = future.result()
                    if result:
                        filename, url, folder_name = result
                        save_folder = f"{folder_name}_mp3"
                        download_futures.append(executor.submit(self.download_audio, filename, url, save_folder))
                
                for future in concurrent.futures.as_completed(download_futures):
                    try:
                        future.result()
                    except Exception as e:
                        self.logger.error(f"Exception occurred during downloading: {e}")
        
        except Exception as e:
            self.logger.error(f"An error occurred during audio processing: {e}")
        
        self.logger.info("All audios processed and downloaded.")

# Example usage:
if __name__ == "__main__":
    downloader = DouyinVideoDownloader()
    try:
        downloader.download_audios_concurrently()
    except Exception as e:
        logging.error(f"An error occurred during audio download: {e}")
