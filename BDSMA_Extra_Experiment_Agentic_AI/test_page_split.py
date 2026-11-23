import os, re, base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.print_page_options import PrintOptions
import time

with open('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/report.html', 'r', encoding='utf-8') as f:
    full_html = f.read()

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

for idx in range(1, 8):
    pattern = rf'<!-- ================= PAGE {idx} ================= -->\s*<div class="page">(.*?)</div>\s*(?=<!-- ================= PAGE|</body>)'
    match = re.search(pattern, full_html, re.DOTALL)
    if not match:
        print(f'Page {idx} not matched!')
        continue
    page_content = match.group(1)
    
    test_html = f"""<!DOCTYPE html><html><head><style>
    @page {{ size: A4 portrait; margin: 16mm 18mm 16mm 18mm; }}
    body {{ font-family: 'Times New Roman', serif; font-size: 11pt; line-height: 1.35; }}
    pre, code, .monospace-box {{ font-family: Consolas, monospace; font-size: 8pt; line-height: 1.2; background: #fafafa; border: 1px solid #222; padding: 6px 8px; margin: 4px 0 10px 0; }}
    table.data-table {{ width: 100%; border-collapse: collapse; font-family: Consolas, monospace; font-size: 8pt; margin: 4px 0 10px 0; border: 1px solid #333; }}
    table.data-table th, table.data-table td {{ border: 1px solid #555; padding: 3px 5px; }}
    table.data-table th {{ background: #f0f0f0; }}
    .arch-container {{ border: 1.5px solid #222; padding: 8px; margin: 6px 0 12px 0; }}
    .arch-header {{ background: #1e3a8a; color: #fff; text-align: center; font-weight: bold; padding: 5px; margin-bottom: 8px; }}
    .arch-grid {{ display: flex; gap: 8px; margin-bottom: 6px; }}
    .col-inputs {{ flex: 1.1; background: #eff6ff; border: 1px solid #93c5fd; padding: 6px; }}
    .col-agent {{ flex: 2.8; background: #f0fdf4; border: 1.5px solid #86efac; padding: 6px; }}
    .col-outputs {{ flex: 1.2; background: #fefce8; border: 1px solid #fde047; padding: 6px; }}
    .box-title {{ font-weight: bold; font-size: 9pt; text-align: center; margin-bottom: 4px; }}
    .arch-item {{ background: #fff; border: 1px solid #cbd5e1; padding: 4px; margin-bottom: 4px; font-size: 7.5pt; }}
    .arch-agent-row {{ display: flex; gap: 5px; margin-bottom: 5px; }}
    .agent-subbox {{ flex: 1; background: #fff; border: 1px solid #cbd5e1; padding: 4px; font-size: 7.5pt; }}
    .arch-bottom {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 5px; font-size: 7.8pt; text-align: center; }}
    .figure-container {{ text-align: center; margin: 4px 0 10px 0; }}
    .figure-container img {{ max-width: 100%; height: auto; }}
    .screen-img {{ width: 100%; border: 1px solid #333; margin-bottom: 8px; }}
    h1.doc-title {{ text-align: center; font-size: 15pt; font-weight: bold; margin: 0 0 20px 0; }}
    h2.section-title {{ font-size: 12pt; font-weight: bold; margin: 12px 0 6px 0; }}
    p {{ margin: 0 0 10px 0; text-align: justify; }}
    ol {{ margin: 4px 0 10px 0; padding-left: 20px; }}
    li {{ margin-bottom: 6px; text-align: justify; }}
    </style></head><body>{page_content}</body></html>"""
    
    with open('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/single_page_test.html', 'w', encoding='utf-8') as pf:
        pf.write(test_html)
    
    driver.get('file:///' + os.path.abspath('BDSMA_Extra_Experiment_Agentic_AI/output_artifacts/single_page_test.html').replace(os.sep, '/'))
    time.sleep(1)
    popts = PrintOptions()
    popts.background = True
    pdf_b64 = driver.print_page(popts)
    raw = base64.b64decode(pdf_b64)
    pgs = len(re.findall(b'/Type\s*/Page[^s]', raw))
    print(f'Page {idx} alone produces: {pgs} page(s)')

driver.quit()
