import os
import re
import csv
import glob
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Utility 
def sanitize_name(s):
    return re.sub(r'[^A-Za-z0-9]', '', s)

# === Inputs from user ===
print("### Step 0: Input Required")
product_name = sanitize_name(input("Product_Name (e.g. Iphone15): ").strip())
ecomm_website = sanitize_name(input("ECommerce_Website (e.g. Flipkart): ").strip())
no_of_reviews = int(input("No_of_reviews (pages): ").strip())
product_link = input("Product_Link (URL with 'page=1'): ").strip()
fetched_date = input("Fetched_Date (DDMMYY or empty for today): ").strip()
author_name = sanitize_name(input("Author_Name (for filename): ").strip())
if not fetched_date:
    fetched_date = datetime.now().strftime("%d%m%y")

# === Folder setup ===
base_folder = os.path.dirname(__file__)  # Where this run_all.py exists
scripts_folder = os.path.join(base_folder, "python_scripts")
review_html_folder = os.path.join(scripts_folder, "review_html")
review_csv_folder = os.path.join(scripts_folder, "review_csv")

os.makedirs(review_html_folder, exist_ok=True)
os.makedirs(review_csv_folder, exist_ok=True)

exec_log = []
def log_step(title, msg):
    header = f"\n## {title}\n"
    print("\n" + "="*60)
    print(f"### {title}")
    print("-" * len(title))
    print(msg)
    exec_log.append(header + msg)

# === Step 1: Download HTML pages ===

log_step("Step 1: Download HTML Pages", f"Downloading {no_of_reviews} pages from:\n{product_link}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
downloaded_pages = 0

for page_num in range(1, no_of_reviews + 1):
    url = product_link.replace("page=1", f"page={page_num}")
    filename = os.path.join(review_html_folder, f"review_html_{page_num}.html")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        downloaded_pages += 1
        print(f"[{page_num}] Saved HTML to {filename}")
    except Exception as e:
        print(f"[{page_num}] ERROR: {e}")

log_step("Step 1 Summary", f"Downloaded and saved {downloaded_pages} pages in '{review_html_folder}'.")

# === Step 2: Convert HTML files to CSV ===

def extract_reviews_from_html(html_content, page_num):
    soup = BeautifulSoup(html_content, 'html.parser')
    reviews = []
    review_containers = soup.find_all('div', class_='cPHDOP')
    if len(review_containers) == 0:
        review_containers = soup.find_all('div', class_='_27M712')
    for idx, review in enumerate(review_containers, 1):
        try:
            review_id = f"P{page_num}_REV_{idx:03d}"
            author_elem = review.find('p', class_='_2NsDsF AwS1CA') or review.find('p', class_='_2sc7ZR _1M4jBT')
            author = author_elem.text.strip() if author_elem else "Anonymous"
            rating_elem = review.find('div', class_='XQDdHH') or review.find('div', class_='_3LWZlK')
            rating = rating_elem.text.strip()[0] if rating_elem else "N/A"
            title_elem = review.find('p', class_='z9E0IG') or review.find('p', class_='_2-N8zT')
            title = title_elem.text.strip() if title_elem else "N/A"
            text_elem = review.find('div', class_='ZmyHeo') or review.find('div', class_='t-ZTKy')
            if text_elem:
                inner_div = text_elem.find('div')
                review_text = inner_div.text.strip() if inner_div else text_elem.text.strip()
            else:
                review_text = "N/A"
            location_elem = review.find('p', class_='MztJPv') or review.find('p', class_='_2mcZGG')
            city = ""
            if location_elem and ',' in location_elem.text:
                city = location_elem.text.split(',')[-1].strip()
            date_elems = review.find_all('p', class_='_2NsDsF')
            posted_date = date_elems[-1].text.strip() if len(date_elems) > 1 else "N/A"
            helpful_elem = review.find('span', class_='tl9VpF') or review.find('span', class_='_18Nubb')
            helpful = "0"
            if helpful_elem:
                import re
                numbers = re.findall(r'\d+', helpful_elem.text.strip())
                helpful = numbers[0] if numbers else "0"
            certified = "No"
            review_text_full = review.get_text()
            if 'Certified Buyer' in review_text_full or 'certified buyer' in review_text_full.lower():
                certified = "Yes"
            reviews.append({
                'Page': page_num,
                'Review_ID': review_id,
                'Author_Name': author,
                'Rating_Stars': rating,
                'Review_Title': title,
                'Review_Text': review_text,
                'City': city,
                'Posted_Date': posted_date,
                'Helpful_Count': helpful,
                'Certified_Buyer': certified
            })
        except Exception:
            continue
    return reviews

log_step("Step 2: Convert HTML to CSV", f"Converting downloaded HTML to CSV files in '{review_csv_folder}'")

os.makedirs(review_csv_folder, exist_ok=True)
all_reviews = []

for page in range(1, downloaded_pages + 1):
    html_file = os.path.join(review_html_folder, f"review_html_{page}.html")
    if not os.path.isfile(html_file):
        print(f"Skipping missing file: {html_file}")
        continue
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    page_reviews = extract_reviews_from_html(html_content, page)
    all_reviews.extend(page_reviews)
    csv_file = os.path.join(review_csv_folder, f"review_csv_{page}.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Page','Review_ID', 'Author_Name', 'Rating_Stars', 'Review_Title', 'Review_Text', 'City', 'Posted_Date', 'Helpful_Count', 'Certified_Buyer']
        import csv as csv_module
        writer = csv_module.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(page_reviews)
    print(f"[{page}] Saved CSV: {csv_file}")

log_step("Step 2 Summary", f"Converted {downloaded_pages} HTML files to CSV files in '{review_csv_folder}'.")

# === Step 3: Merge all CSVs to final CSV ===

log_step("Step 3: Merge CSV Files", f"Merging CSV files and creating final CSV file...")

csv_files = glob.glob(os.path.join(review_csv_folder, "*.csv"))
df_list = [pd.read_csv(f) for f in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

final_csv_name = f"{product_name}_{ecomm_website}_R{no_of_reviews}_D{fetched_date}_{author_name}_fetched.csv"

# Save in base folder (where run_all.py is)
final_csv_path = os.path.join(base_folder, final_csv_name)
merged_df.to_csv(final_csv_path, index=False, encoding='utf-8')

log_step("Final Summary", f"Final merged CSV created:\n{final_csv_path}\nTotal rows: {len(merged_df)}")

# Write execution log markdown file
exec_log_path = os.path.join(base_folder, "executed.md")
with open(exec_log_path, 'w', encoding='utf-8') as log_file:
    log_file.write("# Execution Log\n")
    log_file.write(f"**Run Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.write("\n".join(exec_log))

print("\n\n--- EXECUTION COMPLETE ---")
print(f"Final CSV saved as: {final_csv_path}")
print(f"Execution log saved as: {exec_log_path}")
