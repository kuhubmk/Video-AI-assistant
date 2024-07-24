import requests
from pprint import pprint
import os
import re

url = 'https://www.douyin.com/aweme/v1/web/general/search/single/'

headers = {
    "Cookie": "bd_ticket_guard_client_web_domain=2; LOGIN_STATUS=1; store-region=cn-hn; store-region-src=uid; d_ticket=2ca37430e41926f77a655a30e530eb2d6607f; live_use_vvc=%22false%22; SEARCH_RESULT_LIST_TYPE=%22single%22; my_rd=2; xgplayer_user_id=541495677123; n_mh=-tAF7qk-LcS_Fl7_pZXdQEaPg_l92hMfMy_vXWN8uT4; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=5a69b19dd99e5091fe7e300b812589fd; __security_server_data_status=1; ttwid=1%7CqXeksMw32gPlJcJmeKhUsk1BlK3d5dAwcZfH9ld2EC8%7C1717048015%7Cb6ff7c823159dbe582747f9d319f53416be7cf4099ae276168272f554835c839; odin_tt=1523adf6aebcb6d7d0314858e30c1c8d719bcf3c334c8b5ecfe7317bcd7bf2272ec74a137f669685fef9efe8f79f3cf4232ff93887b1df03888c7b4053c3a55ba82c90a27ae70eefebc973a5626fe369; uid_tt=a81a1d352e69d26dcbadd3010bac4683; uid_tt_ss=a81a1d352e69d26dcbadd3010bac4683; sid_tt=78c46210107bf4c73e863364b6e6154a; sessionid=78c46210107bf4c73e863364b6e6154a; sessionid_ss=78c46210107bf4c73e863364b6e6154a; UIFID_TEMP=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e385280804ef916d3e228e119c71fb7e46297c53d209006b0c9db4fd15165a4df14777b98e6e0a15d7adbcb38522da0a8c5a809; fpk1=U2FsdGVkX19nHboqOB/RlD4RGgGnJGYM5hQxYOiGP9fgwHdnq2hU030sqZD/dHIAXrMgi7IUm09oD2AbKY5cJg==; fpk2=5f4591689f71924dbd1e95e47aec4ed7; sid_guard=78c46210107bf4c73e863364b6e6154a%7C1719374783%7C5184000%7CSun%2C+25-Aug-2024+04%3A06%3A23+GMT; sid_ucp_v1=1.0.0-KGMzZGRiZjYzZjEyMmFkMWE2MzA1ZjViMzA4ZmYxM2Y5OTE1YWM5OWIKGAjMlsCFkY2QARC_p-6zBhjSkx04B0D0BxoCaGwiIDc4YzQ2MjEwMTA3YmY0YzczZTg2MzM2NGI2ZTYxNTRh; ssid_ucp_v1=1.0.0-KGMzZGRiZjYzZjEyMmFkMWE2MzA1ZjViMzA4ZmYxM2Y5OTE1YWM5OWIKGAjMlsCFkY2QARC_p-6zBhjSkx04B0D0BxoCaGwiIDc4YzQ2MjEwMTA3YmY0YzczZTg2MzM2NGI2ZTYxNTRh; __live_version__=%221.1.2.1340%22; UIFID=c4683e1a43ffa6bc6852097c712d14b81f04bc9b5ca6d30214b0e66b4e3852807eb7772bbb09fd05a861dc4e7a326d3b9ba06af7b819cb0761ddfd573683f597d5f71d5749404204b8a639b7bf79121789b1a2817677c6c965c3f4e0b9c3cd48ce6dcc7854719090a66fc10efbc9b9b1b43889361301d5186b7ae7cb4ae812fcc75751b59824609e5a3073167dae62765c6d9b69f378e58856080102fa4d76be; __ac_nonce=066939828005e6cd44eb4; __ac_signature=_02B4Z6wo00f01ixmMPAAAIDCG0L0rUO.9W4sRjRAAO2Y63PW4cavGaCwCJZTlMxT-LLFTsDht1Zm1.ac76J35kuhqfqWC0s1FCzl589d2vXVnSH8PWthfgM7vb-ySbWJ4NezkE18A3FcZbw.18; douyin.com; device_web_cpu_core=16; device_web_memory_size=8; architecture=amd64; dy_swidth=2560; dy_sheight=1440; strategyABtestKey=%221720948774.564%22; csrf_session_id=05e74f98e2bcb73a69bd5b145c7b0df0; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.7%7D; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A1%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAbro0KYLQTP7TWd-LwGDx4LW8bYUcKAWiv6pwrZW8Eyg%2F1720972800000%2F0%2F1720948777809%2F0%22; s_v_web_id=verify_lylcgzf5_niLMnsXa_jEmW_4xlu_BvVe_F4XF25ul0YjY; FRIEND_NUMBER_RED_POINT_INFO=%22MS4wLjABAAAAbro0KYLQTP7TWd-LwGDx4LW8bYUcKAWiv6pwrZW8Eyg%2F1720972800000%2F1720948783243%2F0%2F0%22; passport_csrf_token=0dd093325788d6a4f9615c0580ccd68b; passport_csrf_token_default=0dd093325788d6a4f9615c0580ccd68b; xg_device_score=6.998722829825748; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCR0FscWxFdWVhbTEveDFMU0RMTVFtcnB6Qk85TFJoZGgwOUM3SW5GKytPMkFBaVNMVFJwdFJJcXJmOEQ4T3UvcFVkU3VibDYxWjc1V3ZKQlkxYk9sVGc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; biz_trace_id=1ced40bb; download_guide=%222%2F20240714%2F0%22; pwa2=%220%7C0%7C2%7C0%22; publish_badge_show_info=%221%2C0%2C0%2C1720948812959%22; passport_fe_beating_status=false; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A2560%2C%5C%22screen_height%5C%22%3A1440%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.85%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A250%7D%22",
    "referer": "https://www.douyin.com/search/%E5%84%BF%E5%AD%90?aid=165d20aa-17b3-4b63-b831-645b2eb7f064&publish_time=0&sort_type=0&source=normal_search&type=general",
    "User-Agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
}

search = input('请输入你想搜索的名称：')
dian_zhan = int(input('请输入点赞数量：'))

while True:
    params = {
        'platform': 'PC',
        'aid': '6383',
        'channel': 'aweme_general',
        'type': '4g',
        'time': '50',
        'keyword': search,
        'source': 'normal_search',
        'search': '0',
        'id': '',
        'offset': '0',
        'count': '10',
    }

    html = requests.get(url=url, headers=headers, params=params)
    json_url = html.json()
    # print(json_url)
    for i in json_url['data'][:-1]:
        try:
            url = i['aweme_info']['video']['play_addr']['url_list'][0]
            name = i['aweme_info']['desc']
            aweme_id = i['aweme_info']['aweme_id']
            bofangliang = i['aweme_info']['statistics']['digg_count']
            if bofangliang > dian_zhan and search in name:
                if not os.path.exists(f'./{search}'):
                    os.mkdir(f'./{search}')
                video_name = name
                video_name = video_name.replace('\n', ' ')
                video_name = re.sub(r'[\/:*?"<>|]', '-', video_name)
                resp = requests.get(url)
                print(url)
                file_object = open(f'./{search}/{bofangliang}_{video_name}.mp4', mode='wb')
                file_object.write(resp.content)
                file_object.close()
                print(f'名称：{bofangliang}_{video_name}下载完成')
        except:
            pass
