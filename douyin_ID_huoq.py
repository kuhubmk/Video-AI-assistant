import http.client
import json
import os
import logging

class DouyinIDFetcher:
    def __init__(self, user_urls=None, server_ip="", port=""):
        self.server_ip = server_ip
        self.port = port
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        self.counter = 1
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.logger.addHandler(self.log_handler)
        self.user_urls = user_urls if user_urls else []

    def fetch_id(self, user_url):
        conn = http.client.HTTPConnection(self.server_ip, self.port)
        try:
            conn.request("GET", f"/api/douyin/web/get_sec_user_id?url={user_url}", headers=self.headers)
            res = conn.getresponse()
            if res.status != 200:
                raise Exception(f"Failed to fetch sec_user_id. Status code: {res.status}")
            
            data = res.read().decode("utf-8")
            json_data = json.loads(data)
            sec_user_id = json_data.get('data')
            if not sec_user_id:
                raise KeyError("Expected 'data' field not found in JSON response.")
            
            return sec_user_id
        
        except (http.client.HTTPException, json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Error fetching sec_user_id for {user_url}: {e}")
            return None
        
        finally:
            conn.close()
    
    def save_to_file(self, sec_user_id, folder="douyin_ID"):
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = os.path.join(folder, f"douyin_ids_{self.counter}.txt")
        with open(file_path, 'w') as file:
            file.write(sec_user_id + "\n")
        self.logger.info(f"ID saved to {file_path}")
        
        self.counter += 1

    def fetch_and_save_all(self):
        if not self.user_urls:
            self.logger.warning("No user URLs provided.")
            return
        
        for url in self.user_urls:
            sec_user_id = self.fetch_id(url)
            if sec_user_id:
                self.save_to_file(sec_user_id)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Load configuration from config file
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    
    # Read user URLs input from config
    user_urls_input = config.get("user_urls_input")
    user_urls = user_urls_input.split()
    
    # Read server_ip and port from config
    server_ip = config.get("server_ip")
    port = config.get("port")
    
    # Initialize DouyinIDFetcher with user URLs from config
    fetcher = DouyinIDFetcher(user_urls=user_urls, server_ip=server_ip, port=port)
    fetcher.fetch_and_save_all()
