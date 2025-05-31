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
# ## Data - Setup and Analysis

# %% [markdown]
# ### Path Setup

# %%
# paths
raw_dataset_path = "./Datasets/raw_data"

# raw split
raw_train_split_path = "./Datasets/raw_train_split"
raw_test_split_path = "./Datasets/raw_test_split"

# clean split
clean_train_split_path = "./Datasets/clean_train_split"
clean_test_split_path = "./Datasets/clean_test_split"


# %%
def cleanup(train_path, test_path):
    print(f"clean up train path - {train_path}")
    train_dir = os.listdir(train_path)
    train_dir.sort()
    for dir in train_dir:
        decade_path = os.path.join(train_path, dir)
        if os.path.isdir(decade_path):
            text_files = os.listdir(decade_path)
            text_files.sort()
            for file in text_files:
                if file.endswith(".txt"):
                    file_path = os.path.join(decade_path, file)
                    os.remove(file_path)
                    print(f"succesfully remove {file}")
            os.rmdir(decade_path)
            print(f"succesfully removed directory {dir}")
            print()

    print(f"clean up test path - {test_path}")
    test_dir = os.listdir(test_path)
    test_dir.sort()
    for dir in test_dir:
        decade_path = os.path.join(test_path, dir)
        if os.path.isdir(decade_path):
            text_files = os.listdir(decade_path)
            text_files.sort()
            for file in text_files:
                if file.endswith(".txt"):
                    file_path = os.path.join(decade_path, file)
                    os.remove(file_path)
                    print(f"succesfully remove {file}")
            os.rmdir(decade_path)
            print(f"succesfully removed directory {dir}")
            print()

    os.rmdir(train_path)
    print(f"succesfully removed {train_path}")
    os.rmdir(test_path)
    print(f"succesfully removed {test_path}")

    print("succesfully cleaned up training test files")


# %%
# raw split
if os.path.exists(raw_train_split_path) and os.path.exists(raw_test_split_path):
    cleanup(raw_train_split_path, raw_test_split_path)

os.makedirs(raw_train_split_path)
print(f"create raw train split directory")
os.makedirs(raw_test_split_path)
print(f"create raw test split directory")

# %%
# clean split
if os.path.exists(clean_train_split_path) and os.path.exists(clean_test_split_path):
    cleanup(clean_train_split_path, clean_test_split_path)

os.makedirs(clean_train_split_path)
print(f"create clean train split directory")
os.makedirs(clean_test_split_path)
print(f"create clean test split directory")

# %% [markdown]
# ### Book Data Analysis

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
    for year in range(1770, 1900, 10):
        decade_path = f"{raw_dataset_path}/{year}"
        book_titles[year] = []

        # print(f"decade: {year}")
        text_files = sorted([f for f in os.listdir(decade_path) if f.endswith(".txt")])
        for filename in text_files:
            file_path = os.path.join(decade_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            title_match = re.search(r"^Title:\s*(.+)$", text, re.MULTILINE)
            book_title = title_match.group(1).strip()
            # print(f"book_title: {book_title}")
            book_titles[year].append(book_title)
        # print(f"number of titles in decade: {year} -> {len(book_titles[year])}")
        print()
    return book_titles


book_titles = get_book_titles()
print(f"{book_titles[1770][0]}")


# %%
def dataset_info():
    years = [i for i in range(1770, 1900, 10)]
    book_titles = get_book_titles()

    book_data = []
    for decade in years:
        decade_path = f"{raw_dataset_path}/{decade}"
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
    print(f"total number of books processed: {len(book_data)}")
    return book_data


book_info = dataset_info()
print(f"{book_info[0]}")

# %% [markdown]
# ## Data Split - Stratified Split of Books - Training Books, Testing Books


# %%
def create_stratified_split(book_data, train_split=0.8):
    train_books, test_books = [], []
    books_by_decade = {}

    books_by_decade = {}
    for book in book_data:
        decade = book["decade"]
        if decade not in books_by_decade:
            books_by_decade[decade] = []
        books_by_decade[decade].append(book)

    # debug check
    # for decade, books in books_by_decade.items():
    #     print(f"decade: {decade}, number of books: {len(books)}")

    for decade, books in sorted(books_by_decade.items()):
        shuffled_books = books.copy()
        random.shuffle(shuffled_books)

        total_books = len(books)
        train_size = max(1, int(total_books * train_split))
        test_size = total_books - train_size
        decade_train = shuffled_books[:train_size]
        decade_test = shuffled_books[train_size:]

        train_books.extend(decade_train)
        test_books.extend(decade_test)

    print(f"TRAIN BOOKS: {len(train_books)}")
    print(f"TEST BOOKS: {len(test_books)}")

    return train_books, test_books


book_data = dataset_info()
raw_train, raw_test = create_stratified_split(book_data)


# %%
def write_stratified_split(dataset, file_path):
    for i, book in enumerate(dataset):
        print(f"book: {i + 1}")
        # decade
        book_decade = str(book["decade"])
        # title
        book_title = book["book_title"]
        # filename
        book_filename = book["filename"]
        # path
        book_path = book["filepath"]

        print(f"read book <- {book_path}")
        with open(book_path, "r", encoding="utf-8") as f:
            raw_book = f.read()

        decade_path = os.path.join(file_path, book_decade)
        if not os.path.isdir(decade_path):
            os.makedirs(decade_path)
        out_file = decade_path + "/" + book_filename
        book["file_path"] = out_file
        print(f"new book filepath: {book_path}")
        print(f"write book -> {out_file}")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(raw_book)
        print(f"wrote book successfully!!!")
        print()


# %%
write_stratified_split(raw_train, raw_train_split_path)

# %%
write_stratified_split(raw_test, raw_test_split_path)

# %% [markdown]
# ## Data-Preprocessing

# %% [markdown]
# ## Data-Cleaning


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
def clean_stratified_split(raw_split_path, clean_split_path):
    decade_dirs = [
        dir
        for dir in os.listdir(raw_split_path)
        if os.path.isdir(os.path.join(raw_split_path, dir))
    ]
    decade_dirs.sort()

    total_books = 0
    for decade_dir in decade_dirs:
        clean_decade_path = os.path.join(clean_split_path, decade_dir)
        print(f"clean decade path: {clean_decade_path}")
        if not os.path.exists(clean_decade_path):
            os.makedirs(clean_decade_path)
        raw_decade_path = os.path.join(raw_split_path, decade_dir)
        print(f"raw decade path: {raw_decade_path}")
        text_files = [f for f in os.listdir(raw_decade_path) if f.endswith(".txt")]

        for text_file in text_files:
            total_books += 1
            print(f"books processed: {total_books}")
            raw_file_path = os.path.join(raw_decade_path, text_file)
            # print(f"raw data path: {raw_file_path}")
            clean_file_path = os.path.join(clean_decade_path, text_file)
            # print(f"clean file path: {clean_file_path}")
            # print(f"read raw data: {raw_file_path} -> clean -> write clean data: {clean_file_path}")
            with open(raw_file_path, "r", encoding="utf-8") as f:
                raw_data = f.read()
                print(f"read raw data <- {raw_file_path}")

            cleaned_data = clean_text(raw_data)
            with open(clean_file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_data)
                print(f"write clean data -> {clean_file_path}")

            print(f"wrote cleaned data successfully!!!")
            print()


# %%
clean_stratified_split(raw_train_split_path, clean_train_split_path)

# %%
clean_stratified_split(raw_test_split_path, clean_test_split_path)

# %% [markdown]
# ##

# %%
