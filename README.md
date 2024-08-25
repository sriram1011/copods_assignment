# PDF Text Extraction and Classification

This project is a Python-based tool that extracts and classifies text data from PDF files. The tool uses the `pdfminer.six` library to parse PDF content and classifies the extracted text into categories like titles, headings, and paragraphs based on font size.

## Installation

To use this project, you'll need to have Python installed on your system. Then, you can install the required packages using `pip`:

pip install pdfminer.six


## Usage

**Clone the repository:**

    git clone https://github.com/your-username/your-repository.git
    cd your-repository

## Configuration

The tool uses a configuration file (`config.ini`) to specify the path to the PDF file. Below is an example of the configuration file:

[FILEPATH]
pdf_path = /path/to/your/pdf_file.pdf


## Functions

### `extract_data_from_pdf(pdf_path)`

- **Description:** Extracts content from the specified PDF file.
- **Parameters:** 
  - `pdf_path` (str): The path to the PDF file.
- **Returns:** A generator object containing the PDF content.

### `parse_pdf_data(pdf_data)`

- **Description:** Parses the extracted PDF data to find text properties like font size, font name, and font style.
- **Parameters:** 
  - `pdf_data` (generator): The generator object containing the PDF content.
- **Returns:** 
  - A list of dictionaries containing text properties.
  - Lists of graphical elements like images, tables, and graphs.

### `classify_text(font_size, title_found)`

- **Description:** Classifies the text into categories based on font size.
- **Parameters:** 
  - `font_size` (int): The size of the font.
  - `title_found` (bool): A flag indicating whether the title has been found.
- **Returns:** A string indicating the type of text (Title, Heading, Normal_text, etc.).

### `create_elements_json(text_list)`

- **Description:** Creates a JSON file (`elements.json`) from the parsed text data.
- **Parameters:** 
  - `text_list` (list): A list of dictionaries containing text properties.

## Example Output

The script generates a JSON file (`elements.json`) containing the extracted and classified text data. Below is an example of what the JSON file might look like:

```json
{
    "elements": [
        {
            "type": "Title",
            "text": "Document Title"
        },
        {
            "type": "Heading",
            "text": "Introduction"
        },
        {
            "type": "Normal_text",
            "text": "This is a sample paragraph."
        }
    ]
}
```
