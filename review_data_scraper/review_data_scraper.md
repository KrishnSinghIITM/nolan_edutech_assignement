
# Automated Product Review Data Scraping Tool

---

## Overview

This toolkit subsection automates scraping product reviews from Flipkart, converting them into CSV files, and merging into a single dataset. It uses anti-bot bypass techniques to reliably fetch data, ensuring access even if standard scraping attempts are blocked.

---

## Folder Structure

```
.
├── run_all.py                 # Main orchestrator script
├── executed.md                # Execution log report
├── {Final_CSV}.csv            # Final merged CSV file (named dynamically)
├── python_scripts/            # Helper scripts folder
│   ├── scrap_html.py          # Scraper that bypasses anti-bot restrictions
│   ├── html_to_csv.py         # HTML to CSV converter
│   ├── review_html/           # Scraped HTML pages stored here
│   └── review_csv/            # Per-page CSV files saved here
```

---

## How to Use

1. **Install dependencies:**

   ```
   pip install requests beautifulsoup4 pandas
   ```

2. **Run the main orchestrator:**

   ```
   python run_all.py
   ```

3. **Enter requested details:**
   - Product Name (e.g., `Iphone15`)
   - E-commerce Website (e.g., `Flipkart`)
   - Number of pages to scrape
   - Product review URL with `?page=1`
   - Fetch date (DDMMYY or press Enter for today)
   - Author name for file tagging

4. **Output:**
   - HTML files scraped bypassing bot restrictions
   - CSV files generated for each page
   - Merged CSV dataset named:
     ```
     {Product}_{Website}_R{Num}_D{Date}_{Author}_fetched.csv
     ```
   - Execution details saved in `executed.md`

---

## Advantages

- Bypasses anti-bot protections by smartly managing headers and request patterns
- Modular, easy to extend or adapt to other ecommerce sites
- Provides transparent and detailed logging for reproducibility
- Enables reliable large-scale review data collection otherwise blocked by sites

---

## Usage Terms

- This is not free software.  
- Use only with explicit permission from the author.  
- Redistribution or commercial use strictly prohibited.

---

## Author & Copyright

Made by [Krishn SIngh](https://github.com/KrishnSinghIITM) 

Minor in DSML, IITMandi x Masai, Batch 1  
Std_ID: IITMCS_2406170  

© All rights reserved.

"[test_link_samsungS24](https://www.flipkart.com/samsung-galaxy-s24-5g-snapdragon-amber-yellow-128-gb/product-reviews/itmd4baa945a78ef?pid=MOBHDVFKSZNEZGXW&lid=LSTMOBHDVFKSZNEZGXWFNGEN2&marketplace=FLIPKART&page=1)"
