import os
import pandas as pd
from parsers import universal_parser

def main():
    statements_dir = 'statements/'
    all_data = []

    print("--- Starting Credit Card Statement Parsing (Universal Parser) ---")

    for filename in os.listdir(statements_dir):
        if filename.lower().endswith('.pdf'):
            filepath = os.path.join(statements_dir, filename)
            
            print(f"Processing '{filename}'...")
            extracted_data = universal_parser.parse_statement(filepath)
            
            if extracted_data is not None:
                all_data.append(extracted_data)
            else:
                print(f"Failed to parse '{filename}'.")


    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        column_order = [
            'Issuer', 'Cardholder Name', 'Card Number (Last 4 Digits)', 
            'Statement Date', 'Payment Due Date', 'Total Amount Due'
        ]
        final_df = final_df[column_order]
        
        print("\n\n--- Consolidated Extracted Data ---")
        print(final_df.to_string())
    else:
        print("\n--- No data was successfully extracted. ---")

if __name__ == '__main__':
    main()