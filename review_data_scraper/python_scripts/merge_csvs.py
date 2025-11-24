import os
import glob
import pandas as pd

input_folder = "review_csv"
output_file = "final_review_csv.csv"

csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

if not csv_files:
    print(f"No CSV files found in folder '{input_folder}'")
    exit(1)

print(f"Found {len(csv_files)} CSV files. Merging...")

# Read and concatenate all CSVs
df_list = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

merged_df.to_csv(output_file, index=False, encoding='utf-8')

print(f"✅ Merged {len(csv_files)} files into '{output_file}' with {len(merged_df)} total rows.")
