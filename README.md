# Credit-Card-Parser
An intelligent Python parser to extract key data from multi-bank credit card statements using a single, universal engine.

## 1. Objective
This project is an advanced Python-based PDF parser designed to extract 5 key data points from the credit card statements of 5 major Indian credit card issuers. It features a single, intelligent parsing engine that automatically identifies the bank and applies the correct extraction logic, demonstrating a robust and scalable software design.

---

## 2. Scope & Features

### Supported Credit Card Issuers
The universal parser can process statements from:
1.  **HDFC Bank**
2.  **ICICI Bank**
3.  **SBI Card**
4.  **Axis Bank**
5.  **Kotak Mahindra Bank**

### Extracted Data Points
The following 5 data points are consistently extracted from each statement:
1.  **Cardholder Name**
2.  **Card Number (Last 4 Digits)**
3.  **Statement Date**
4.  **Payment Due Date**
5.  **Total Amount Due**

---

## 3. Technical Implementation & Architecture

This project was refactored from a multi-file approach to a more efficient and centralized single-parser architecture. This design significantly improves maintainability and scalability.

### Core Technologies
*   **Language:** Python 3
*   **Libraries:**
    *   `pdfplumber`: For extracting raw text from PDF files.
    *   `pandas`: For organizing the final extracted data into a clean, readable DataFrame.
    *   `re` (Regular Expressions): The core engine for finding and isolating specific data points.

### Advanced Architecture: The Universal Parser
Instead of separate scripts for each bank, the project now uses a single, intelligent module (`parsers/universal_parser.py`) with the following key features:

1.  **Centralized Pattern Configuration:** All regular expressions for all banks are stored in a single, easy-to-manage dictionary (`BANK_PATTERNS`). This makes it trivial to update a pattern or add support for a new bank without touching the core logic.

2.  **Content-Based Bank Detection:** The parser reads the text content of each PDF to find an identifying keyword (e.g., "HDFC Bank", "SBI Card"). This is a major improvement over the initial design, as it **no longer relies on PDF filenames**, making the system more robust and user-friendly.

3.  **Unified Parsing Logic:** A single function (`parse_statement`) handles the entire workflow:
    *   Opens and reads the PDF.
    *   Identifies the bank.
    *   Selects the correct set of regex patterns from the central configuration.
    *   Extracts, cleans, and structures the data.
    *   Returns a standardized pandas DataFrame.

This elegant design ensures that the system is not only functional but also clean, efficient, and easy to extend in the future.

---

## 4. How to Run the Project

### Prerequisites
- Python 3.6+
- pip (Python package installer)

### Step 1: Set Up the Environment
Clone the repository and install the required dependencies from the `requirements.txt` file.
```bash
# Navigate to your project directory
cd credit-card-parser

# Install libraries
pip install -r requirements.txt
```

### Step 2: Add PDF Statements
Place any number of credit card statement PDFs from the supported banks into the `statements/` directory. The filenames do not need to contain the bank's name.

### Step 3: Execute the Parser
Run the main script from the project's root directory.
```bash
python main.py
```
The script will automatically process each PDF, identify the bank, extract the data, and print a final, consolidated table to the console.

---

## 5. Conclusion
This solution successfully meets all assignment objectives by creating a functional, well-structured, and advanced PDF parser. By refactoring to a universal parsing engine with auto-detection capabilities, the project demonstrates a strong understanding of software design principles, resulting in a system that is robust, maintainable, and highly scalable.
