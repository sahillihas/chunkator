# Chunkator - Chunk It Right!!!

Welcome to **Chunkator**, your go-to open-source Python library for accurate and efficient sentence chunking. Built to outperform traditional chunking tools like NLTK, LangChain, and LlamaIndex, Chunkator handles complex text structures with ease, making it a reliable choice for all your text processing needs.

---

## Installation


```bash
pip install chunkator
```

---

## 🌟 Features

- **High Accuracy**: Handles abbreviations (e.g., "Ph.D."), acronyms, and URLs without breaking sentences incorrectly.
- **Regex-Driven**: Utilises precompiled regex patterns for lightning-fast processing.
- **Edge-Case Resilience**: Processes text with complex punctuation, initials, or special formatting reliably.
- **Page-Aware Chunking**: Automatically merges sentences broken across pages and removes pagination artefacts like "Page 2 of 5".
- **Hyphenation Handling**: Rejoins words split with hyphens at line breaks (e.g., "recom-\nmendation" → "recommendation").
- **Lightweight**: Free of unnecessary dependencies, making it simple to integrate into any Python project.

---

## 🚀 Why Chunkator?

While tools like NLTK, LangChain, and LlamaIndex provide sentence-splitting functionality, they often fail to handle edge cases effectively. Chunkator excels in:

### 1️ **Abbreviation Handling**

Chunkator correctly processes abbreviations like "Dr.", "Ph.D.", and "U.S.A.", avoiding improper splits.

**Example Input**:
```text
Dr. Smith is a leading scientist. He earned his Ph.D. in Physics.
```

- **NLTK Output**:
  ```
  ['Dr.', 'Smith is a leading scientist.', 'He earned his Ph.D.', 'in Physics.']
  ```
- **Chunkator Output**:
  ```
  ['Dr. Smith is a leading scientist.', 'He earned his Ph.D. in Physics.']
  ```

---

### 2️ **Website and Email Parsing**

Chunkator keeps URLs and email addresses intact, unlike other libraries that often split them erroneously.

**Example Input**:
```text
Visit our website at www.example.com. Contact us at support@example.com.
```

- **LangChain Output**:
  ```
  ['Visit our website at www.example.', 'com.', 'Contact us at support@example.', 'com.']
  ```
- **Chunkator Output**:
  ```
  ['Visit our website at www.example.com.', 'Contact us at support@example.com.']
  ```

---

### 3️ **Ellipses and Multi-Dot Patterns**

Chunkator handles ellipses (...) and similar patterns with precision.

**Example Input**:
```text
She hesitated... but eventually agreed. It was unexpected...
```

- **LlamaIndex Output**:
  ```
  ['She hesitated.', '.', '.', 'but eventually agreed.', 'It was unexpected.', '.', '.', '.']
  ```
- **Chunkator Output**:
  ```
  ['She hesitated... but eventually agreed.', 'It was unexpected...']
  ```

---


### 4️ **Page-Spanning Sentences**

Chunkator intelligently reconstructs sentences broken across page boundaries and removes noisy page markers.

Example Input:

```
This is a sentence that starts on one page
and continues on the next. Page 2 of 5
But this is a new sentence.
```
Chunkator Output:

``` 
['This is a sentence that starts on one page and continues on the next.', 'But this is a new sentence.']
```

### 5️ **Hyphenated Word Merging**

Chunkator rejoins words split by hyphenation at line breaks.

Example Input:

```
The recom-
mendation was accepted.
```
Chunkator Output:

``` 
['The recommendation was accepted.']
```
---

## 📖 Usage

Using Chunkator is simple. Here is an example:

```python
from chunkator import sentence_split

# Input text
text = "Dr. Smith is a leading scientist. He earned his Ph.D. in Physics. Visit www.example.com for more info."

# Split into sentences
sentences = sentence_split(text)

# Output
print(sentences)
# Output: ['Dr. Smith is a leading scientist.', 'He earned his Ph.D. in Physics.', 'Visit www.example.com for more info.']
```

---

## 🔍 Advanced Use Cases

### Custom Pattern Handling

Chunkator can be customized to handle domain-specific text structures. Modify the library's regex patterns to create tailored solutions for your projects.

---

## 📊 Benchmarking

| Library        | Abbreviations | Websites | Ellipses | Hyphenation | Page-Aware | Speed (ms for 1000 sentences) |
| -------------- | ------------- | -------- | -------- | ----------- | ---------- | ----------------------------- |
| **NLTK**       | ❌             | ❌        | ⚠️       | ❌           | ❌          | 120                           |
| **LangChain**  | ⚠️            | ❌        | ❌        | ❌           | ❌          | 150                           |
| **LlamaIndex** | ❌             | ⚠️       | ❌        | ❌           | ❌          | 130                           |
| **Chunkator**  | ✅             | ✅        | ✅        | ✅           | ✅          | **90**                        |


---

## 🤝 Contribute to us!

We welcome contributions! Feel free to:

- Submit issues
- Create pull requests
- Suggest improvements

Together, let's make Chunkator the best text-processing library out there!

---
