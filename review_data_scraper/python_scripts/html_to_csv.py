import os
import re
import csv
from bs4 import BeautifulSoup

input_folder = "review_html"
output_folder = "review_csv"
os.makedirs(output_folder, exist_ok=True)
csv_filename = os.path.join(output_folder, "review_csv_1to100.csv")

all_reviews = []

# Function to extract reviews from one HTML file
def extract_reviews_from_html(html_content, page_num):
    soup = BeautifulSoup(html_content, 'html.parser')
    reviews = []
    review_containers = soup.find_all('div', class_='cPHDOP')
    if len(review_containers) == 0:
        review_containers = soup.find_all('div', class_='_27M712')
    for idx, review in enumerate(review_containers, 1):
        try:
            review_id = f"P{page_num}_REV_{idx:03d}"
            # Author
            author_elem = review.find('p', class_='_2NsDsF AwS1CA')
            if not author_elem:
                author_elem = review.find('p', class_='_2sc7ZR _1M4jBT')
            author = author_elem.text.strip() if author_elem else "Anonymous"
            # Rating
            rating_elem = review.find('div', class_='XQDdHH')
            if not rating_elem:
                rating_elem = review.find('div', class_='_3LWZlK')
            rating = rating_elem.text.strip()[0] if rating_elem else "N/A"
            # Title
            title_elem = review.find('p', class_='z9E0IG')
            if not title_elem:
                title_elem = review.find('p', class_='_2-N8zT')
            title = title_elem.text.strip() if title_elem else "N/A"
            # Review Text
            text_elem = review.find('div', class_='ZmyHeo')
            if not text_elem:
                text_elem = review.find('div', class_='t-ZTKy')
            review_text = "N/A"
            if text_elem:
                inner_div = text_elem.find('div')
                review_text = inner_div.text.strip() if inner_div else text_elem.text.strip()
            # City
            location_elem = review.find('p', class_='MztJPv')
            if not location_elem:
                location_elem = review.find('p', class_='_2mcZGG')
            city = ""
            if location_elem:
                location_text = location_elem.text
                if ',' in location_text:
                    city = location_text.split(',')[-1].strip()
            # Date
            date_elems = review.find_all('p', class_='_2NsDsF')
            posted_date = "N/A"
            if len(date_elems) > 1:
                posted_date = date_elems[-1].text.strip()
            else:
                date_elem = review.find('p', class_='_2sc7ZR')
                if date_elem:
                    date_text = date_elem.text.strip()
                    if 'ago' in date_text.lower() or 'month' in date_text.lower() or 'day' in date_text.lower():
                        posted_date = date_text
            # Helpful
            helpful_elem = review.find('span', class_='tl9VpF')
            if not helpful_elem:
                helpful_elem = review.find('span', class_='_18Nubb')
            helpful = "0"
            if helpful_elem:
                helpful_text = helpful_elem.text.strip()
                numbers = re.findall(r'\d+', helpful_text)
                helpful = numbers[0] if numbers else "0"
            # Certified Buyer
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
        except Exception as e:
            continue
    return reviews

# Process all files from review_html/review_html_1.html to review_html_100.html
for file_num in range(1, 101):
    html_file = os.path.join(input_folder, f"review_html_{file_num}.html")
    if not os.path.isfile(html_file):
        print(f"Skipped missing {html_file}")
        continue
    print(f"Processing {html_file} ...")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    all_reviews.extend(extract_reviews_from_html(html_content, file_num))

print(f"\n✅ Total reviews extracted: {len(all_reviews)}")
print(f"Saving to: {csv_filename}")

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Page','Review_ID', 'Author_Name', 'Rating_Stars', 'Review_Title', 'Review_Text', 'City', 'Posted_Date', 'Helpful_Count', 'Certified_Buyer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_reviews)

print("\n🎉 All done! Combined CSV created.")
print(f"Sample:\n")
for review in all_reviews[:3]:
    print(f"Page: {review['Page']}, Author: {review['Author_Name']}, Stars: {review['Rating_Stars']}, Title: {review['Review_Title']}")
