def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

               
                cleaned_lines = [
                    line.strip()
                    for line in lines[1:]
                    if line.strip()
                ]

                
                if 50 <= len(cleaned_lines) <= 100:
                    return cleaned_lines
                else:
                    print(f"Warning: Read {len(cleaned_lines)} records using {encoding}")

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []
