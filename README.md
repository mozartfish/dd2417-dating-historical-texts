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
