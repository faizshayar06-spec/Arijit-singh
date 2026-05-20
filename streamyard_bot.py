import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
GUEST_URL = "https://streamyard.com/jktgf2iug5" 
STREAM_KEY = os.getenv("YT_STREAM_KEY")

def start_stream():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 25) 
    
    try:
        driver.get(GUEST_URL)

        # Click Popups
        driver.execute_script("""
            setInterval(() => {
                document.querySelectorAll('button').forEach(btn => {
                    if(['accept', 'continue', 'allow', 'got it'].some(t => btn.innerText.toLowerCase().includes(t))) btn.click();
                });
            }, 2000);
        """)
        time.sleep(8)
        
        # Enter Name
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[not(@type='hidden')]")))
        name_input.send_keys("Faiz")
        
        enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter studio')]")))
        enter_button.click()
        time.sleep(15) 

        # FFmpeg Setup
        ffmpeg_cmd = [
            'ffmpeg', '-f', 'x11grab', '-video_size', '1920x1080', '-i', ':99.0',
            '-f', 'pulse', '-i', 'default', '-c:v', 'libx264', '-preset', 'veryfast', 
            '-b:v', '4000k', '-pix_fmt', 'yuv420p', '-f', 'flv', f'rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}'
        ]
        
        process = subprocess.Popen(ffmpeg_cmd)
        print("Stream started... running for 2 hours.")
        
        # 2 Ghante (7000 seconds) tak chalega
        time.sleep(7000) 
        process.terminate()

    finally:
        driver.quit()

if __name__ == "__main__":
    start_stream()
    
