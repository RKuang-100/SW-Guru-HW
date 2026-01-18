#!/usr/bin/env python3 -B
"""Word frequency counter - refactored version following SE heuristics"""

# Q3: What Mechanism vs Policy issues did I find?
# AQ3: Found hardcoded stopwords, punctuation, top_n value, and formatting stuff all mixed into the code.
#      Fixed by moving ALL of that into this CONFIG dict at the top. Now if you want different stopwords
#      or want to show top 20 instead of 10, just change the config - no need to dig through code.
CONFIG = {
    'stopwords': ["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
                  "of", "is", "was", "are", "were", "be", "been", "with"],
    'punctuation': '.,!?;:"()[]',
    'top_n': 10,
    'bar_char': '*',
    'word_width': 15,
    'count_width': 3
}


# Q1: What Separation of Concerns issues did I find?
# AQ1: The original code mixed everything together - reading files, processing data, and printing
#      all in one function. Fixed by splitting into model functions (below) that only work with data,
#      and presentation functions (further down) that only handle printing. No mixing!

def read_text_file(filename):
    """Reads text from a file - pure I/O function"""
    with open(filename) as f:
        return f.read()


def clean_word(word, punctuation):
    """Removes punctuation from a single word"""
    return word.strip(punctuation)


def normalize_text(text):
    """Converts text to lowercase and splits into words"""
    return text.lower().split()


def filter_stopwords(words, stopwords):
    """Removes stopwords from word list"""
    return [word for word in words if word and word not in stopwords]


def count_word_frequencies(words):
    """Counts how many times each word appears"""
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts


def sort_words_by_frequency(counts):
    """Sorts words by frequency, highest first"""
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def get_top_words(sorted_words, top_n):
    """Gets the top N most frequent words"""
    return sorted_words[:top_n]


def clean_all_words(words, punctuation):
    """Cleans all words and removes empty ones"""
    cleaned_words = []
    for word in words:
        cleaned = clean_word(word, punctuation)
        if cleaned:
            cleaned_words.append(cleaned)
    return cleaned_words


def build_result_dict(counts, top_words):
    """Builds the result dictionary with counts and stats"""
    return {
        'counts': counts,
        'top_words': top_words,
        'total_words': sum(counts.values()),
        'unique_words': len(counts)
    }


# Q2: What Single Responsibility Principle issues did I find?
# AQ2: The original count_words() function was doing way too much - reading, cleaning, counting,
#      sorting, filtering, formatting, printing... everything! Fixed by breaking it into small
#      functions where each one does exactly ONE job:
#      - read_text_file: just reads a file
#      - clean_word: just strips punctuation from one word
#      - clean_all_words: just cleans a list of words
#      - normalize_text: just lowercases and splits
#      - filter_stopwords: just removes stopwords
#      - count_word_frequencies: just counts occurrences
#      - sort_words_by_frequency: just sorts
#      - get_top_words: just slices the top N
#      - build_result_dict: just builds the result structure

def process_text(text, config):
    """Main processing pipeline - orchestrates all the model functions"""
    words = normalize_text(text)
    cleaned_words = clean_all_words(words, config['punctuation'])
    filtered_words = filter_stopwords(cleaned_words, config['stopwords'])
    counts = count_word_frequencies(filtered_words)
    sorted_words = sort_words_by_frequency(counts)
    top_words = get_top_words(sorted_words, config['top_n'])
    return build_result_dict(counts, top_words)


# Q1 continued: Here are the presentation functions - all the printing stuff separated out
# AQ1: All the print statements got moved here. Now if you want to change how things look,
#      you only touch these functions. The data processing functions above don't care about
#      formatting at all.

def format_bar(count, bar_char):
    """Creates a bar visualization for word count"""
    return bar_char * count


def format_word_line(index, word, count, bar, word_width, count_width):
    """Formats a single line of word output"""
    return f"{index:2}. {word:{word_width}} {count:{count_width}} {bar}"


def print_header(filename):
    """Prints the header section"""
    print(f"\n{'='*50}")
    print(f"WORD FREQUENCY ANALYSIS - {filename}")
    print(f"{'='*50}\n")


def print_summary(result):
    """Prints the summary statistics"""
    print(f"Total words (after removing stopwords): {result['total_words']}")
    print(f"Unique words: {result['unique_words']}\n")


def print_top_words(result, config):
    """Prints the top N words with formatting"""
    print(f"Top {config['top_n']} most frequent words:\n")
    
    for i, (word, count) in enumerate(result['top_words'], 1):
        bar = format_bar(count, config['bar_char'])
        line = format_word_line(i, word, count, bar, 
                               config['word_width'], config['count_width'])
        print(line)
    
    print()


def print_results(result, filename, config):
    """Main presentation function - orchestrates all printing"""
    print_header(filename)
    print_summary(result)
    print_top_words(result, config)


# Q4: Any small Function problems?
# AQ4: Yeah, the original function was like 40 lines doing everything. Fixed by making
#      each function super short (like 2-10 lines max) and giving them clear names.
#      Now you can read any function in 5 seconds and know exactly what it does.
#      Much easier to test individual pieces too.

def count_words(file="essay.txt", config=None):
    """Main entry point - orchestrates model and presentation"""
    if config is None:
        config = CONFIG
    
    # Q1: Here's where we tie it all together - model first, then presentation
    # AQ1: Notice how we do all the data processing first (read + process_text),
    #      then pass the results to print_results. Clean separation - no mixing!
    text = read_text_file(file)
    result = process_text(text, config)
    print_results(result, file, config)


if __name__ == "__main__":
    count_words("essay.txt")
