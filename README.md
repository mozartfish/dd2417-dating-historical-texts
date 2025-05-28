# dd2417-dating-historical-texts

Goal : Can you automatically detect what decade or even what year a certain document has been written? To make the task more interesting, explicit mentions of
years should be removed from the texts. Språkbanken has a lot of historical Swedish text data, and you can find English texts from various points in time at Project Gutenberg.

Dataset :
Project Gutenberg : 
extract snippets from several novels/documents (200-500 characters per sample, multiple samples per document)
Cleaning : punctuation/lowercase/remove explicit years
Tokenize sentences / words
Label each document → Year or decade

Data representation
Hybrid : word embeddings (pretrained Glove) + character-level embeddings

Model architecture
Averaged embeddings vs. RNN/GRU/LSTM (last hidden state or max pooling)
Fully-connected layer + softmax 
transformer??

Training
Cross-entropy loss
Adam optimizer
Use a validation set ?

Metrics : Confusion matrix 

## Models 

1. DistillBert (transformer architecture)
2. BIGRU (Assignment 4) - avoid LSTMs at all costs
3. Logistic Regression (Assignment 2)
4. N-gram modeling (Assignment 2)

## Books 

### 1700

1. The Battle of the Books, and other Short Pieces
2. The Way of the World
3. A Tale of a Tub
4. An Essay Towards a New Theory of Vision
5. The Tatler, Volume 1

### 1710

1. The Spectator, Volume 1
2. An Essay on Criticism
3. The Rape of the Lock, and Other Poems
4. The Journal to Stella
5. Three Dialogues Between Hylas and Philonous in Opposition to Sceptics and Atheists

### 1720

1. Robinson Crusoe
2. Gulliver's Travels
3. The Beggar's Opera
4. The Fable of the Bees; Or, Private Vices, Public Benefits

### 1730

1. A Discourse Concerning Ridicule and Irony in Writing (1729)
2. A Letter to Dion
3. An Essay on Man; Moral Essays and Satires
4. A Treatise of Human Nature

### 1740

1. History of Tom Jones, a Foundling
2. Clarissa Harlowe; or the history of a young lady — Volume 1
3. Joseph Andrews, Vol. 1
4. The Fortunate Foundlings
5. Pamela, or Virtue Rewarded

### 1750

1. The Adventures of Peregrine Pickle
2. Preface to a Dictionary of the English Language
3. Amelia — Volume 1
4. The History of Sir Charles Grandison, Volume 4 (of 7)
5. The History of Miss Betsy Thoughtless

### 1760

1. The Castle of Otranto
2. A Sentimental Journey Through France and Italy
3. The Vicar of Wakefield
4. The Life and Opinions of Tristram Shandy, Gentleman
5. The History of England in Three Volumes, Vol. I., Part B.

### 1770

1. She Stoops to Conquer; Or, The Mistakes of a Night: A Comedy
2. The School for Scandal
3. The Expedition of Humphry Clinker
4. Evelina, Or, the History of a Young Lady's Entrance into the World
5. The Rivals: A Comedy

### 1780

1. History of the Decline and Fall of the Roman Empire — Volume 5
2. Songs of Innocence and of Experience
3. The Journal of a Tour to the Hebrides with Samuel Johnson, LL.D.
4. Emmeline, the Orphan of the Castle
5. The Task, and Other Poems

### 1790

1. The Monk: A Romance
2. The Mysteries of Udolpho
3. A Vindication of the Rights of Woman
4. A Sicilian Romance

### 1800

1. Sense and Sensibility
2. The Sorrows of Young Werther
3. Castle Rackrent
4. St. Leon: A Tale of the Sixteenth Century
5. Fundamental Principles of the Metaphysic of Morals
6. Thalaba the Destroyer

### 1810

1. Mansfield Park
2. Pride and Prejudice
3. The Life of Horatio, Lord Nelson
4. Rob Roy — Complete
5. Roderick, the last of the Goths

### 1820

1. The Last of the Mohicans; A narrative of 1757
2. The Pioneers; Or, The Sources of the Susquehanna
3. Woodstock; or, the Cavalier
4. History of the Peninsular War, Volume 1 (of 6)
5. Adonais
6. Anne of Geierstein; Or, The Maiden of the Mist. Volume 2 (of 2)

### 1830

1. The Narrative of Arthur Gordon Pym of Nantucket
2. Oliver Twist
3. Sartor Resartus: The Life and Opinions of Herr Teufelsdröckh
4. Crotchet Castle
5. Paul Clifford — Complete
6. The doctor, &c., vol. 2 (of 7)

### 1840

1. Wuthering Heights
2. The Count of Monte Crist
3. Jane Eyre: An Autobiography
4. A Christmas Carol
5. Vanity Fair
6. Agnes Grey

### 1850

1. Uncle Tom's Cabin
2. Walden, and On The Duty Of Civil Disobedience
3. Madame Bovary
4. Moby Dick; Or, The Whale
5. The Scarlet Letter
6. Leaves of Grass

### 1860

1. Alice's Adventures in Wonderland
2. Little Women
3. Great Expectations
4. Drum-Taps
5. Adam Bede

### 1870

1. Middlemarch
2. Daniel Deronda
3. The Law and the Lady
4. The Way We Live Now
5. The Return of the Native

### 1880

1. The Strange Case of Dr. Jekyll and Mr. Hyde
2. Adventures of Huckleberry Finn
3. Treasure Island
4. King Solomon's Mines
5. She

### 1890

1. The Time Machine
2. The War of the Worlds
3. The Jungle Book
4. Dracula
5. The Picture of Dorian Gray
