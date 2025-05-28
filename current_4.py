# %% [markdown]
# # DD2417 Final Project - Dating Historical Texts

# %% [markdown]
# ## Libraries + Imports

# %%
import os
import csv
import random
import re
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# seed all experiments and setup
random.seed(42)

# %% [markdown]
# ## Data

# %%
# paths
raw_dataset_path = "./Datasets/raw_data"
clean_dataset_path = "./Datasets/clean_data"
model_dataset_path = "./Datasets/model_data"

# %%
# count all the data files in the raw data file
print(f"count the number of books in each decade directory in the raw data")
total_books = 0
for decade in range(1700, 1900, 10):
    decade_path = f"{raw_dataset_path}/{decade}"
    if os.path.exists(decade_path):
        text_files = [f for f in os.listdir(decade_path) if f.endswith(".txt")]
        print(f"{decade}: {len(text_files)} books")
        total_books += len(text_files)
print(f"total number of books for project: {total_books}")


# %%
# get all the titles of the books
def get_book_titles():
    book_titles = {}
    for year in range(1700, 1900, 10):
        decade_path = f"{raw_dataset_path}/{year}"
        book_titles[year] = []

        print(f"decade: {year}")
        text_files = sorted([f for f in os.listdir(decade_path) if f.endswith(".txt")])
        for filename in text_files:
            file_path = os.path.join(decade_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            title_match = re.search(r"^Title:\s*(.+)$", text, re.MULTILINE)
            book_title = title_match.group(1).strip()
            print(f"book_title: {book_title}")
            book_titles[year].append(book_title)
        print(f"number of titles in decade: {year} -> {len(book_titles[year])}")
        print()

    return book_titles


# %%
# remove all old data files
if os.path.exists(clean_dataset_path):
    print(f"clean up - previous clean_data_files")
    directories = os.listdir(clean_dataset_path)
    directories.sort()
    for dir in directories:
        decade_path = os.path.join(clean_dataset_path, dir)
        if os.path.isdir(decade_path):
            text_files = os.listdir(decade_path)
            text_files.sort()
            for file in text_files:
                if file.endswith(".txt"):
                    file_path = os.path.join(decade_path, file)
                    os.remove(file_path)
                    print(f"succesfully removed {file}")
            os.rmdir(decade_path)
            print(f"successfully removed directory {dir}")
            print()
    os.rmdir(clean_dataset_path)
    print(f"succesfully removed {clean_dataset_path}")
    print()

# create new data files
if os.path.exists(model_dataset_path):
    print(f"clean up - previous model data")
    data_files = [f for f in os.listdir(model_dataset_path) if f.endswith(".csv")]
    for file in data_files:
        file_path = os.path.join(model_dataset_path, file)
        os.remove(file_path)
        print(f"succesfully removed {file}")
    os.rmdir(model_dataset_path)
    print(f"succesfully removed {model_dataset_path}")
    print()

# %%
if not os.path.exists(clean_dataset_path):
    print(f"create clean data directory")
    os.makedirs(clean_dataset_path)

if not os.path.exists(model_dataset_path):
    print(f"create model data directory for storing data for building models")
    os.makedirs(model_dataset_path)

# %% [markdown]
# ### Data-Preprocessing


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
    # print(f"text files: {text_list}")
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
for year in years:
    preprocess_text(raw_dataset_path, year)


# %% [markdown]
# ### 1800's Data

# %%
years = [1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890]
for year in years:
    preprocess_text(raw_dataset_path, year)

# %% [markdown]
# ### Dataset Splits - Train, Validation, Test splits


# %%
def dataset_info():
    years = [i for i in range(1700, 1900, 10)]
    book_titles = get_book_titles()

    book_data = []
    for decade in years:
        decade_path = f"{clean_dataset_path}/{decade}"
        if os.path.exists(decade_path):
            text_files = sorted(
                [f for f in os.listdir(decade_path) if f.endswith(".txt")]
            )
            for index, filename in enumerate(text_files):
                if decade in book_titles and index < len(book_titles[decade]):
                    book_title = book_titles[decade][index]
                else:
                    book_title = f"unknown_book_{index + 1}"
                book_info = {
                    "decade": decade,
                    "filename": filename,
                    "book_title": book_title,
                    "filepath": os.path.join(decade_path, filename),
                    "book_id": f"{decade}_{book_title[:20].replace(' ', '_')}",
                }
                book_data.append(book_info)
    return book_data


# %%
def create_dataset_splits(book_data):
    train_books, valid_books, test_books = [], [], []

    # group books by decade
    books_by_decade = {}
    for book in book_data:
        decade = book["decade"]
        if decade not in books_by_decade:
            books_by_decade[decade] = []
        books_by_decade[decade].append(book)

    for decade, books in books_by_decade.items():
        num_books = len(books)
        if num_books == 4:
            train_books.extend(books[:2])
            valid_books.extend(books[2:3])
            test_books.extend(books[3:4])

        elif num_books == 5:
            train_books.extend(books[:3])
            valid_books.extend(books[3:4])
            test_books.extend(books[4:5])

        elif num_books == 6:
            train_books.extend(books[:4])
            valid_books.extend(books[4:5])
            test_books.extend(books[5:6])

    print(f"train data: {train_books}")
    print(f"valid data: {valid_books}")
    print(f"test data: {test_books}")
    print()

    return train_books, valid_books, test_books


# %%
book_data = dataset_info()
train_data, valid_data, test_data = create_dataset_splits(book_data)

# %% [markdown]
# ### Random Sampling Passages


# %%
def random_sampling_passages(book_list, num_passages=5, passage_length=1500):
    passages_data = []
    for book in book_list:
        with open(book["filepath"], "r", encoding="utf-8") as f:
            text = f.read()

        # randomly sample passages
        for i in range(num_passages):
            max_start = len(text) - passage_length
            start_pos = random.randint(0, max_start)
            passage = text[start_pos : start_pos + passage_length]
            passage_info = {
                "text": passage,
                "decade": book["decade"],
                "decade_id": (book["decade"] - 1700) // 10,
                "book_title": book["book_title"],
                "book_id": book["book_id"],
                "passage_id": f"{book['book_id']}_passage_{i}",
            }
            passages_data.append(passage_info)

    return passages_data


# %%
def write_data_to_csv(passages_data, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # write header
        writer.writerow(
            ["text", "decade", "book_title", "passage_id", "decade_id", "book_id"]
        )

        for passage in passages_data:
            writer.writerow(
                [
                    passage["text"].replace("\n", " ").replace("\r", " "),
                    passage["decade"],
                    passage["book_title"],
                    passage["passage_id"],
                    passage["decade_id"],
                    passage["book_id"],
                ]
            )
        print(f"Save {len(passages_data)} passages to {filepath}")


# %%
print(f"get book data and create splits")
book_data = dataset_info()
train_books, validation_books, test_books = create_dataset_splits(book_data)
print(
    f"Book splits: {len(train_books)} -> training_data, {len(validation_books)} -> validation_data, {len(test_books)} -> test_data"
)
print()
print(f"Randomly sample passages for creating datasets")
train_passages = random_sampling_passages(
    train_books, num_passages=20, passage_length=1500
)
validation_passages = random_sampling_passages(
    validation_books, num_passages=15, passage_length=1500
)
test_passages = random_sampling_passages(
    test_books, num_passages=10, passage_length=1500
)
print(
    f"Passage counts: {len(train_passages)} -> training_passages, {len(validation_passages)} -> validation_passages, {len(test_passages)} -> test_passages"
)
print()
print(f"write data to csv files")
write_data_to_csv(train_passages, f"{model_dataset_path}/train_passages.csv")
write_data_to_csv(validation_passages, f"{model_dataset_path}/validation_passages.csv")
write_data_to_csv(test_passages, f"{model_dataset_path}/test_passages.csv")

# %% [markdown]
# ##

# %%


# %%
