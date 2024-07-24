import os
import requests
import json
import logging

class DouyinVideoFetcher:
    def __init__(self, server_ip="", port=""):
        self.server_ip = server_ip
        self.port = port

    def find_nickname(self, json_data):
        nickname = 'unknown_nickname'
        stack = [json_data]
        
        while stack:
            current = stack.pop()
            
            if isinstance(current, dict):
                for key, value in current.items():
                    if key == 'nickname' and isinstance(value, str):
                        nickname = value.strip()[:20]  # Limit to 20 characters
                        return nickname
                    elif isinstance(value, (dict, list)):
                        stack.append(value)
            elif isinstance(current, list):
                for item in current:
                    stack.append(item)
        
        return nickname

    def fetch_douyin_user_videos(self, sec_user_id=None, max_cursor=0, count=1):
        if not sec_user_id:
            logging.warning("sec_user_id is None or empty.")
            return
        
        url = f"http://{self.server_ip}:{self.port}/api/douyin/web/fetch_user_post_videos"
        params = {
            'sec_user_id': sec_user_id,
            'max_cursor': max_cursor,
            'count': count
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            
            # Parse JSON response
            json_data = response.json()
            
            # Find nickname
            nickname = self.find_nickname(json_data)
            
            # Create a directory for saving files
            directory = "downloaded_json"
            os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
            
            # Determine the filename
            filename = f"{nickname}_videos.json"
            filepath = os.path.join(directory, filename)
            
            # Save JSON data to a file in the created directory, overwrite if exists
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"JSON data saved to: {filepath}")
            
            return json_data
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error occurred: {e}")
        
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON response: {e}")

# Example usage in main.py
if __name__ == "__main__":
    import json
    import logging

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load configuration from config file
    with open('config.json', 'r',encoding="utf-8") as config_file:
        config = json.load(config_file)
    
    douyin_id_folder = config.get("douyin_id_folder", "douyin_ID")
    count = config.get("count", 1)
    
    # List all files in the folder
    try:
        file_list = os.listdir(douyin_id_folder)
    except FileNotFoundError as e:
        logging.error(f"The folder '{douyin_id_folder}' does not exist.")
        exit(1)
    
    # Initialize DouyinVideoFetcher with server_ip and port from config
    server_ip = config.get("server_ip")
    port = config.get("port")
    fetcher = DouyinVideoFetcher(server_ip=server_ip, port=port)
    
    # Process each file in the folder
    for file_name in file_list:
        file_path = os.path.join(douyin_id_folder, file_name)
        
        try:
            # Read sec_user_id from each file
            with open(file_path, 'r') as f:
                sec_user_id = f.read().strip()  # Read the entire content and strip any surrounding whitespace
                
                if sec_user_id:
                    # Call fetch_douyin_user_videos method
                    fetcher.fetch_douyin_user_videos(sec_user_id, count=count)
                else:
                    logging.warning(f"The file '{file_name}' is empty or invalid.")
        
        except FileNotFoundError as e:
            logging.error(f"File not found: {file_path}")
        except Exception as e:
            logging.error(f"An error occurred while processing the file '{file_name}': {e}")
