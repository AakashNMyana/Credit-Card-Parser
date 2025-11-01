import pdfplumber
import re
import pandas as pd

BANK_PATTERNS = {
    'HDFC': {
        'identifier': 'HDFC Bank',
        'patterns': {
            'Cardholder Name': re.compile(r"MR\s+([A-Z\s]+)"),
            'Card Number (Last 4 Digits)': re.compile(r"XXXX XXXX XXXX (\d{4})"),
            'Statement Date': re.compile(r"Statement Date\s*:\s*(\d{2}/\d{2}/\d{4})"),
            'Payment Due Date': re.compile(r"Payment Due Date\s*:\s*(\d{2}/\d{2}/\d{4})"),
            'Total Amount Due': re.compile(r"Total Amount Due\s*Rs\.\s*([\d,]+\.\d{2})")
        }
    },
    'ICICI': {
        'identifier': 'ICICI Bank',
        'patterns': {
            'Cardholder Name': re.compile(r"Name\s*:\s*([A-Z\s\.]+)"),
            'Card Number (Last 4 Digits)': re.compile(r"Card Number\s*:\s*XXXX XXXX XXXX (\d{4})"),
            'Statement Date': re.compile(r"Statement Date\s*:\s*(\d{2}-\w{3}-\d{4})"),
            'Payment Due Date': re.compile(r"Payment Due Date\s*:\s*(\d{2}-\w{3}-\d{4})"),
            'Total Amount Due': re.compile(r"Total Amount Due\s*:\s*₹\s*([\d,]+\.\d{2})")
        }
    },
    'SBI': {
        'identifier': 'SBI Card',
        'patterns': {
            'Cardholder Name': re.compile(r"MR\.\s+([A-Z\s]+)"),
            'Card Number (Last 4 Digits)': re.compile(r"CARD NO\.\s*:\s*XXXX XXXX XXXX (\d{4})"),
            'Statement Date': re.compile(r"Statement Date\s*:\s*(\d{2} \w{3} \d{4})"),
            'Payment Due Date': re.compile(r"Payment Due Date\s*:\s*(\d{2} \w{3} \d{4})"),
            'Total Amount Due': re.compile(r"Total Amount Due\s+([\d,]+\.\d{2})")
        }
    },
    'AXIS': {
        'identifier': 'Axis Bank',
        'patterns': {
            'Cardholder Name': re.compile(r"MR\.\s+([A-Z\s]+)"),
            'Card Number (Last 4 Digits)': re.compile(r"Card Number\s+XXXX XXXX XXXX (\d{4})"),
            'Statement Date': re.compile(r"Statement Date\s+(\d{2}-\d{2}-\d{4})"),
            'Payment Due Date': re.compile(r"Payment due date\s+(\d{2}-\d{2}-\d{4})"),
            'Total Amount Due': re.compile(r"TOTAL AMOUNT DUE\s+Rs\.\s+([\d,]+\.\d{2})")
        }
    },
    'KOTAK': {
        'identifier': 'Kotak',
        'patterns': {
            'Cardholder Name': re.compile(r"Dear\s+([A-Z\s]+),"),
            'Card Number (Last 4 Digits)': re.compile(r"CREDIT CARD NO\.\s+XXXX XXXX XXXX (\d{4})"),
            'Statement Date': re.compile(r"STATEMENT DATE\s+(\d{2}/\d{2}/\d{4})"),
            'Payment Due Date': re.compile(r"PAYMENT DUE DATE\s+(\d{2}/\d{2}/\d{4})"),
            'Total Amount Due': re.compile(r"TOTAL AMOUNT DUE\s+₹([\d,]+\.\d{2})")
        }
    }
}

def parse_statement(statement_path):
    try:
        with pdfplumber.open(statement_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() or ""

        # Step 1: Identify the bank
        detected_bank = None
        for bank, config in BANK_PATTERNS.items():
            if config['identifier'] in full_text:
                detected_bank = bank
                break
        
        if not detected_bank:
            print(f"Error: Could not determine the bank for '{statement_path}'.")
            return None

        # Step 2: Use the patterns for the identified bank
        patterns = BANK_PATTERNS[detected_bank]['patterns']
        extracted_data = {'Issuer': BANK_PATTERNS[detected_bank]['identifier']}

        for key, pattern in patterns.items():
            match = pattern.search(full_text)
            if not match:
                print(f"Error: Could not find '{key}' in '{statement_path}' for {detected_bank} bank.")
                return None # Stop if any single pattern fails
            
            extracted_data[key] = match.group(1).strip()
            
        return pd.DataFrame([extracted_data])

    except Exception as e:
        print(f"An unexpected error occurred while parsing '{statement_path}': {e}")
        return None