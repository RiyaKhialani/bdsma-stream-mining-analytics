from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1440,950')
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8501')
print("Connecting to Streamlit and waiting for app to render...")

# Wait for main header to appear
for i in range(25):
    time.sleep(1)
    body = driver.find_element(By.TAG_NAME, 'body').text
    if 'Venture Discovery Agent' in body and 'Discussions Streamed' in body:
        print(f"App rendered completely after {i+1} seconds!")
        break
else:
    print("Warning: Timed out waiting for render.")

time.sleep(2)
driver.save_screenshot('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/streamlit_screen1.png')
print("Screenshot 1 (Executive Dashboard) captured.")

# Switch to Tab 2 (Lean Canvas)
all_p = driver.find_elements(By.TAG_NAME, 'p')
for p in all_p:
    if 'Lean Canvas' in p.text:
        driver.execute_script("arguments[0].click();", p)
        print("Clicked Lean Canvas tab.")
        time.sleep(2)
        driver.save_screenshot('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/streamlit_screen2.png')
        print("Screenshot 2 (Lean Canvas) captured.")
        break
else:
    print("Could not find Lean Canvas tab paragraph.")

driver.quit()
