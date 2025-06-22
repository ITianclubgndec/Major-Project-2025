import pandas as pd
import os
import re

# ====== CONFIG ======
input_csv = "major.csv"  # 🔁 Replace with your actual CSV filename
group_col = "Group no. "
source_col = "Source Code (zip file) & Link "
poster_col = "Project Poster "

# ✅ Only these columns should be in final CSV
desired_columns = ["Name ", "Project Guide ", "Project Title "]


# ====== READ CSV ======
df = pd.read_csv(input_csv)

# ====== NORMALIZE GROUP NAMES ======
def normalize_group(val):
    match = re.search(r'(\d+)', str(val))
    return f"G-{int(match.group(1))}" if match else None

df[group_col] = df[group_col].apply(normalize_group)
df = df.dropna(subset=[group_col])

# ====== PROCESS EACH GROUP ======
grouped = df.groupby(group_col)

for group, group_df in grouped:
    folder = group  # e.g., G-1

    if not os.path.isdir(folder):
        print(f"❌ Skipping: Folder '{folder}' not found.")
        continue

    # 1️⃣ Keep only Name, Project Guide, Project Title
    clean_df = group_df[desired_columns].copy()
    csv_path = os.path.join(folder, f"{folder}.csv")
    clean_df.to_csv(csv_path, index=False)

    # 2️⃣ Write source code to sourcecode.txt
    source_val = str(group_df[source_col].iloc[0])
    with open(os.path.join(folder, "sourcecode.txt"), "w", encoding="utf-8") as f:
        f.write(source_val)

    # 3️⃣ Write poster link to projectposter.txt
    poster_val = str(group_df[poster_col].iloc[0])
    with open(os.path.join(folder, "projectposter.txt"), "w", encoding="utf-8") as f:
        f.write(poster_val)

    print(f"✅ Processed: {folder}")
