# %% [markdown]
# # DD2417 Final Project - Dating Historical Texts

# %% [markdown]
# ## Libraries + Imports

# %%
import os
import random
import re
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# %% [markdown]
# ## Data

# %%
# paths
raw_dataset_path = "./Datasets/raw_data"
clean_dataset_path = "./Datasets/clean_data"

# create directories
if not os.path.exists(clean_dataset_path):
    print(f"create clean data directory")
    os.makedirs(clean_dataset_path)


# %% [markdown]
# ### Data Preprocessing


# %%
def clean_text(text):
    # remove everything up to and including start
    start_match = re.search(
        r"\*\*\* START OF.*?\*\*\*", text, re.IGNORECASE | re.DOTALL
    )
    if start_match:
        text = text[start_match.end() :]

    # remove everything after end
    end_match = re.search(r"\*\*\* END OF.*?\*\*\*", text, re.IGNORECASE | re.DOTALL)
    if end_match:
        text = text[: end_match.start()]

    # remove years
    text = re.sub(r"\b1[0-9]{3}\b", "", text)

    # remove whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# %%
def preprocess_text(dataset_path, year):
    print(f"preprocess text")
    print(f"directory year: {year}")
    decade_path = dataset_path + "/" + str(year) + "/"
    cleaned_data_path = f"{clean_dataset_path}/{year}/"
    if not os.path.exists(cleaned_data_path):
        os.makedirs(cleaned_data_path)
    text_list = os.listdir(decade_path)
    print(f"text files: {text_list}")
    for text_file in text_list:
        if text_file.endswith(".txt"):
            print(f"file name: {text_file}")
            # read file
            with open(decade_path + text_file, "r", encoding="utf-8") as f:
                raw_text = f.read()
                print(f"read file sucessfully")

            cleaned_text = clean_text(raw_text)
            print(f"text cleaned succesfully")

            # save file
            out_file = cleaned_data_path + text_file
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
                print(f"cleaned text succesfully saved to {out_file}")
                print()


# %% [markdown]
# ### 1700s Data

# %%
years = [1700, 1710, 1720, 1730, 1740, 1750, 1760, 1770, 1780, 1790]
# test_year = years[0]
# preprocess_text(raw_dataset_path, test_year)
for year in years:
    preprocess_text(raw_dataset_path, year)


# %% [markdown]
# ### 1800's Data

# %%
years = [1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890]
# test_year = years[0]
# preprocess_text(raw_dataset_path, test_year)
for year in years:
    preprocess_text(raw_dataset_path, year)

# %% [markdown]
# ##
