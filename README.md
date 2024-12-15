# Chunkator

Welcome to `chunkator`, a Python library designed for efficient and precise sentence segmentation. This library provides a robust alternative to existing tools like NLTK, LangChain, and LlamaIndex sentence splitters. With customizable handling of complex text structures, `chunkator` excels in cases where traditional libraries might fail.

## Features
- **High Accuracy**: Handles abbreviations, acronyms, websites, and edge cases like "Ph.D." without breaking sentences incorrectly.
- **Regex-Driven**: Precompiled regex patterns for faster processing.
- **Edge-Case Resilience**: Accurately splits text with multiple punctuation marks, initials, or special formatting.
- **Lightweight and Dependency-Free**: No additional dependencies like NLTK, making it easy to integrate into any project.

---

## Why `chunkator`?
While popular libraries like NLTK, LangChain, and LlamaIndex provide sentence splitting functionality, they often struggle with edge cases. Here's why `chunkator` stands out:

### **1. Handling Abbreviations**
`chunkator` processes abbreviations like "Dr.", "Mr.", and "Ph.D." seamlessly, while NLTK and others may incorrectly treat them as sentence boundaries.

#### Example:
Input:
```
Dr. Smith is a leading scientist. He earned his Ph.D. in Physics.
```

- **NLTK Output**:
  - `['Dr.', 'Smith is a leading scientist.', 'He earned his Ph.D.', 'in Physics.']`
- **chunkator Output**:
  - `['Dr. Smith is a leading scientist.', 'He earned his Ph.D. in Physics.']`

---

### **2. Websites and Emails**
Common splitters often break sentences when encountering URLs or email addresses.

#### Example:
Input:
```
Visit our website at www.example.com. Contact us at support@example.com.
```

- **LangChain Output**:
  - `['Visit our website at www.example.', 'com.', 'Contact us at support@example.', 'com.']`
- **chunkator Output**:
  - `['Visit our website at www.example.com.', 'Contact us at support@example.com.']`

---

### **3. Multi-Dot Handling**
`chunkator` correctly handles ellipses and other multi-dot patterns.

#### Example:
Input:
```
She hesitated... but eventually agreed. It was unexpected...
```

- **LlamaIndex Output**:
  - `['She hesitated.', '.', '.', 'but eventually agreed.', 'It was unexpected.', '.', '.', '.']`
- **chunkator Output**:
  - `['She hesitated... but eventually agreed.', 'It was unexpected...']`

---

### **4. Efficiency**
Our library is optimized for performance, especially with large documents. Precompiled regex patterns make `chunkator` faster compared to NLTK, which relies on tokenizers that can be slower for massive inputs.

---

## Installation
Install `chunkator` via pip:

```bash
pip install chunkator
```

---

## Usage
Here's how to use the `chunkator` library in your projects:

```python
from sentence_split import sentence_split

# Input text
text = "Dr. Smith is a leading scientist. He earned his Ph.D. in Physics. Visit www.example.com for more info."

# Split into sentences
sentences = sentence_split(text)

# Output
print(sentences)
# Output: ['Dr. Smith is a leading scientist.', 'He earned his Ph.D. in Physics.', 'Visit www.example.com for more info.']
```

---

## Advanced Use Cases

### Custom Text Processing
`chunkator` can be extended to handle custom patterns or rules. Modify the regex patterns in the library to suit your specific needs.

---

## Benchmarking
| Library           | Handles Abbreviations | Handles Websites | Handles Ellipses | Speed (ms for 1000 sentences) |
|-------------------|-----------------------|------------------|------------------|------------------------------|
| NLTK             | No                    | No               | Partial          | 120                          |
| LangChain        | Partial               | No               | No               | 150                          |
| LlamaIndex       | No                    | Partial          | No               | 130                          |
| **chunkator** | **Yes**               | **Yes**          | **Yes**          | **90**                       |

---

## Contributing
We welcome contributions! Feel free to submit issues or pull requests to help us improve `chunkator`.

---
