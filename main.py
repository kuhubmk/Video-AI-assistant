import logging
import os
import json
from douyin_ID_huoq import DouyinIDFetcher
from douyin_video_downloader import DouyinVideoDownloader
from douyin_video_fetcher import DouyinVideoFetcher
from video_analyzer import VideoAnalyzer

def main():
    try:
            # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        
        # Load configuration from config file
        with open('config.json', 'r',encoding="utf-8") as config_file:
            config = json.load(config_file)
        
        # Read user URLs input from config
        user_urls_input = config.get("user_urls_input")
        user_urls = user_urls_input.split()
        
        # Read server_ip and port from config
        server_ip = config.get("server_ip", "")
        port = config.get("port", "")
        
        # Initialize DouyinIDFetcher with user URLs from config
        fetcher = DouyinIDFetcher(user_urls=user_urls, server_ip=server_ip, port=port)
        fetcher.fetch_and_save_all()


        # Fetch Douyin videos using DouyinVideoFetcher
        douyin_id_folder = config.get("douyin_id_folder", "douyin_ID")
        count = int(config.get("count", 1))  # Ensure count is an integer
        
        # List all files in the specified folder
        try:
            file_list = os.listdir(douyin_id_folder)
        except FileNotFoundError:
            logging.error(f"The folder '{douyin_id_folder}' does not exist.")
            return
        
        # Initialize DouyinVideoFetcher instance
        server_ip = config.get("server_ip")
        port = int(config.get("port"))  # Ensure port is an integer
        video_fetcher = DouyinVideoFetcher(server_ip=server_ip, port=port)
        
        # Process each file in the folder
        for file_name in file_list:
            file_path = os.path.join(douyin_id_folder, file_name)
            
            try:
                # Read sec_user_id from each file
                with open(file_path, 'r',encoding="utf-8") as f:
                    sec_user_id = f.read().strip()
                    
                    if sec_user_id:
                        # Call fetch_douyin_user_videos method
                        video_fetcher.fetch_douyin_user_videos(sec_user_id, count=count)
                    else:
                        logging.warning(f"The file '{file_name}' is empty or invalid.")
            
            except FileNotFoundError:
                logging.error(f"File not found: {file_path}")
            except Exception as e:
                logging.error(f"An error occurred while processing the file '{file_name}': {e}")

        # Concurrent video download using DouyinVideoDownloader
        downloader = DouyinVideoDownloader()

        try:
            downloader.download_audios_concurrently()
        except Exception as e:
            logging.error(f"An error occurred during audio download: {e}")

        # Initialize VideoAnalyzer instance
       
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


    except Exception as e:
        logging.error(f"An error occurred during the execution: {e}")

if __name__ == "__main__":
    main()
