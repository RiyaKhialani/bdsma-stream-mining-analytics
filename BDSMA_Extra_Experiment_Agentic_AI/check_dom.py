from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1440,950')
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8501')
print("Waiting for pipeline to execute in Streamlit...")

# Poll for tabs to appear
for i in range(20):
    time.sleep(1)
    tabs = driver.find_elements(By.XPATH, "//button[contains(., 'Opportunities') or contains(., 'Lean Canvas')]")
    if tabs:
        print(f"Tabs appeared after {i+1} seconds!")
        break
else:
    print("Polling timed out.")

time.sleep(2)
driver.save_screenshot('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/streamlit_screen1.png')
print("Screenshot 1 saved.")

# Click Tab 2 (Lean Canvas & Venture Lab)
tabs = driver.find_elements(By.XPATH, "//button[contains(., 'Lean Canvas')]")
if tabs:
    driver.execute_script("arguments[0].click();", tabs[0])
    time.sleep(2)
    driver.save_screenshot('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/streamlit_screen2.png')
    print("Screenshot 2 (Lean Canvas) saved.")
else:
    print("Lean Canvas tab not found.")

driver.quit()
