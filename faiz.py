import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIG ---
GUEST_URL = "https://streamyard.com/6ihfwcdmwx" 

def start_stream():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Screen size fix karni zaroori hai taaki coordinates exactly kaam karein
    chrome_options.add_argument("--window-size=1920,1080") 
    
    # Permissions Bypass
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--autoplay-policy=no-user-gesture-required")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1, 
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.notifications": 1
    })

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 25) 
    
    try:
        print("Opening StreamYard...")
        driver.get(GUEST_URL)

        # STEP 1: FORCE CLICK POPUPS
        driver.execute_script("""
            function clickAnything() {
                let buttons = Array.from(document.querySelectorAll('button'));
                buttons.forEach(btn => {
                    let txt = btn.innerText.toLowerCase();
                    if(txt.includes('accept') || txt.includes('continue') || txt.includes('allow') || txt.includes('got it')) {
                        btn.click();
                    }
                });
            }
            setInterval(clickAnything, 2000); 
        """)
        time.sleep(8)
        
        # STEP 2: ENTER NAME & STUDIO
        print("Waiting for visible Name input field...")
        input_xpath = "//input[not(@type='hidden')]"
        name_input = wait.until(EC.visibility_of_element_located((By.XPATH, input_xpath)))
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        
        try:
            name_input.clear()
        except:
            pass 
        
        print("Typing name as a real human...")
        name_input.send_keys("Faiz")
        time.sleep(2) 

        print("Hunting for the 'Enter studio' button...")
        enter_button_xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter studio')]"
        enter_button = wait.until(EC.element_to_be_clickable((By.XPATH, enter_button_xpath)))
        enter_button.click()
        print("Successfully bypassed and entered the Studio! 🥀")

        # Studio load hone ka extra time (taaki video player poora aa jaye)
        time.sleep(12) 

        # STEP 3: THE ULTIMATE COORDINATE CLICK 🎯
        print("Executing exact coordinate click on the bottom-right corner... 🖥️")
        driver.execute_script("""
            function clickByCoordinates() {
                // 1. Screen par sabse bada div (Main Stage area) dhoondo
                let largestArea = 0;
                let stage = null;
                document.querySelectorAll('div').forEach(el => {
                    let r = el.getBoundingClientRect();
                    let area = r.width * r.height;
                    if (r.width >= 600 && r.width <= 1600 && r.height >= 400 && area > largestArea) {
                        largestArea = area;
                        stage = el;
                    }
                });

                if (stage) {
                    let r = stage.getBoundingClientRect();
                    
                    // 2. Mouse ko stage ke beecho-beech move karo taaki controls 'Wake Up' ho jayein
                    let centerX = r.left + (r.width / 2);
                    let centerY = r.top + (r.height / 2);
                    stage.dispatchEvent(new MouseEvent('mousemove', {bubbles: true, clientX: centerX, clientY: centerY}));
                    
                    // Saath mein ek Double Click bhi maar do
                    stage.dispatchEvent(new MouseEvent('dblclick', {bubbles: true, clientX: centerX, clientY: centerY}));

                    // 3. 1 second wait karo aur bottom-right corner pe click maar do
                    setTimeout(() => {
                        let clickX = r.right - 30; 
                        let clickY = r.bottom - 30; 
                        
                        let targetEl = document.elementFromPoint(clickX, clickY);
                        if (targetEl) {
                            targetEl.dispatchEvent(new MouseEvent('mouseover', {bubbles: true, clientX: clickX, clientY: clickY}));
                            targetEl.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, clientX: clickX, clientY: clickY}));
                            targetEl.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, clientX: clickX, clientY: clickY}));
                            targetEl.dispatchEvent(new MouseEvent('click', {bubbles: true, clientX: clickX, clientY: clickY}));
                            console.log("🎯 BOOM! Coordinate clicked exactly at:", clickX, clickY);
                        }
                    }, 1500); 
                }
            }
            clickByCoordinates();
        """)
        
        # Maximize hone ka waqt aur browser ko khula rakhne ke liye wait
        print("Studio screen setup complete. Press Ctrl+C in terminal to close.")
        while True:
            time.sleep(1)

    except Exception as e:
        print(f"Error encountered: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_stream()
    
