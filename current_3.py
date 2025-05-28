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
# remove all old data files
if os.path.exists(clean_dataset_path):
    print(f"clean up - previous clean_data_files")
    directories = os.listdir(clean_dataset_path)
    directories.sort()
    for dir in directories:
        decade_path = os.path.join(clean_dataset_path, dir)
        if os.path.isdir(decade_path):
            for file in os.listdir(decade_path):
                if file.endswith(".txt"):
                    file_path = os.path.join(decade_path, file)
                    os.remove(file_path)
                    print(f"succesfully removed a file")
            os.rmdir(decade_path)
            print(f"successfully removed directory{dir}")
    os.rmdir(clean_dataset_path)
    print(f"succesfully removed {clean_dataset_path}")

# create new data files
if os.path.exists(model_dataset_path):
    print(f"clean up - previous model data")
    data_files = [f for f in os.listdir(model_dataset_path) if f.endswith(".csv")]
    for file in data_files:
        file_path = os.path.join(model_dataset_path, file)
        os.remove(file_path)
        print(f"removed {file}")
    os.rmdir(model_dataset_path)
    print(f"succesfully removed {model_dataset_path}")

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
# ### Dataset Splits - Train, Validation, Test splits


# %%
def dataset_info():
    years = [i for i in range(1700, 1900, 10)]
    book_titles = {
        1700: [
            "The Battle of the Books, and other Short Pieces",
            "The Way of the World",
            "A Tale of a Tub",
            "An Essay Towards a New Theory of Vision",
        ],
        1710: [
            "The Spectator, Volume 1",
            "An Essay on Criticism",
            "The Rape of the Lock, and Other Poems",
            "The Journal to Stella",
            "Three Dialogues Between Hylas and Philonous in Opposition to Sceptics and Atheists",
        ],
        1720: [
            "Robinson Crusoe",
            "Gulliver's Travels",
            "The Beggar's Opera",
            "The Fable of the Bees; Or, Private Vices, Public Benefits",
        ],
        1730: [
            "A Discourse Concerning Ridicule and Irony in Writing (1729)",
            "A Letter to Dion",
            "An Essay on Man; Moral Essays and Satires",
            "A Treatise of Human Nature",
        ],
        1740: [
            "History of Tom Jones, a Foundling",
            "Clarissa Harlowe; or the history of a young lady — Volume 1",
            "Joseph Andrews, Vol. 1",
            "The Fortunate Foundlings",
            "Pamela, or Virtue Rewarded",
        ],
        1750: [
            "The Adventures of Peregrine Pickle",
            "Preface to a Dictionary of the English Language",
            "Amelia — Volume 1",
            "The History of Sir Charles Grandison, Volume 4 (of 7)",
            "The History of Miss Betsy Thoughtless",
        ],
        1760: [
            "The Castle of Otranto",
            "A Sentimental Journey Through France and Italy",
            "The Vicar of Wakefield",
            "The Life and Opinions of Tristram Shandy, Gentleman",
            "The History of England in Three Volumes, Vol. I., Part B.",
        ],
        1770: [
            "She Stoops to Conquer; Or, The Mistakes of a Night: A Comedy",
            "The School for Scandal",
            "The Expedition of Humphry Clinker",
            "Evelina, Or, the History of a Young Lady's Entrance into the World",
            "The Rivals: A Comedy",
        ],
        1780: [
            "History of the Decline and Fall of the Roman Empire — Volume 5",
            "Songs of Innocence and of Experience",
            "The Journal of a Tour to the Hebrides with Samuel Johnson, LL.D.",
            "Emmeline, the Orphan of the Castle",
            "The Task, and Other Poems",
        ],
        1790: [
            "The Monk: A Romance",
            "The Mysteries of Udolpho",
            "A Vindication of the Rights of Woman",
            "A Sicilian Romance",
        ],
        1800: [
            "Sense and Sensibility",
            "The Sorrows of Young Werther",
            "Castle Rackrent",
            "St. Leon: A Tale of the Sixteenth Century",
            "Fundamental Principles of the Metaphysic of Morals",
            "Thalaba the Destroyer",
        ],
        1810: [
            "Mansfield Park",
            "Pride and Prejudice",
            "The Life of Horatio, Lord Nelson",
            "Rob Roy — Complete",
            "Roderick, the last of the Goths A tragic poem",
        ],
        1820: [
            "The Last of the Mohicans; A narrative of 1757",
            "The Pioneers; Or, The Sources of the Susquehanna",
            "Woodstock; or, the Cavalier",
            "History of the Peninsular War, Volume 1 (of 6)",
            "Adonais",
            "Anne of Geierstein; Or, The Maiden of the Mist. Volume 2 (of 2)",
        ],
        1830: [
            "The Narrative of Arthur Gordon Pym of Nantucket",
            "Oliver Twist",
            "Sartor Resartus: The Life and Opinions of Herr Teufelsdröckh",
            "Crotchet Castle",
            "Paul Clifford — Complete",
            "The doctor, &c., vol. 2 (of 7)",
        ],
        1840: [
            "Wuthering Heights",
            "The Count of Monte Cristo",
            "Jane Eyre: An Autobiography",
            "A Christmas Carol",
            "Vanity Fair",
            "Agnes Grey",
        ],
        1850: [
            "Uncle Tom's Cabin",
            "Walden, and On The Duty Of Civil Disobedience",
            "Madame Bovary",
            "Moby Dick; Or, The Whale",
            "The Scarlet Letter",
            "Leaves of Grass",
        ],
        1860: [
            "Alice's Adventures in Wonderland",
            "Little Women",
            "Great Expectations",
            "Drum-Taps",
            "Adam Bede",
        ],
        1870: [
            "Middlemarch",
            "Daniel Deronda",
            "The Law and the Lady",
            "The Way We Live Now",
            "The Return of the Native",
        ],
        1880: [
            "The Strange Case of Dr. Jekyll and Mr. Hyde",
            "Adventures of Huckleberry Finn",
            "Treasure Island",
            "King Solomon's Mines",
            "She",
        ],
        1890: [
            "The Time Machine",
            "The War of the Worlds",
            "The Jungle Book",
            "Dracula",
            "The Picture of Dorian Gray",
        ],
    }

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
                    book_title = f"unknown book {index + 1}"
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
    # print(f"{books_by_decade}")

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
