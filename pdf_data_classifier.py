import configparser
from pdfminer.high_level import extract_pages
from pdfminer.layout import (
    LTTextBox, LTTextLine, LTImage, LTCurve, LTLine, LTChar
)
import json

def extract_data_from_pdf(pdf_path):
    """
    Extract and return whole PDF data from the given path which will be further used for classification.
    :param pdf_path: path where PDF file exists.
    :return: Content that's in PDF file.
    """
    try:
        return extract_pages(pdf_path)

    except Exception as error:
        print(f"Error: {error}")



def parse_pdf_data(pdf_data):
    """
    This function will parse the data in PDF to find properties Font size, Font Name, Font Style of the text, which will
    be used in classification.
    :param pdf_data: A generator object containing all the content of the given PDF file.
    :return: A dictionary containing all the properties of elements like Font size, Font Name, Font Style of the text in
    PDF.
    """
    try:
        table_and_graph_elements_coordinates_list = []
        image_elements_coordinates_list = []
        text_list = []
        for page_layout in pdf_data:

            for element in page_layout:
                text_properties_dict = {}
                if isinstance(element, LTTextBox):
                    text = element.get_text().replace('\n', '')
                    text_properties_dict["text"] = text
                    for text_line in element:
                        if isinstance(text_line, LTTextLine):
                            for char in text_line:
                                if isinstance(char, LTChar):
                                    text_properties_dict["fontsize"] = int(char.size)
                                    break
                    text_list.append(text_properties_dict)

                # TODO: Parse the co-ordinates that are given in the below code's output to check which text belongs to Images, Tables or Graphs in future improvements.

                # The below code is used for detection of non-text elements like Graphs, Images, Tables, etc.
                elif isinstance(element, LTCurve) or isinstance(element, LTLine):
                    # Element is a graphical element (line or curve or tables)
                    table_and_graph_elements_coordinates_list.append(str(element))
                elif isinstance(element, LTImage):
                    # Element is an image
                    image_elements_coordinates_list.append(str(element))

        return text_list, table_and_graph_elements_coordinates_list, image_elements_coordinates_list

    except Exception as error:
        print(f"Error: {error}")

def classify_text(font_size, title_found):
    """
    Used to determine whether the input text is Title, Paragraph, heading, etc.
    How this classification works: It determines on the basis of Font size.
        Header: A header usually comes before a Title and usually is on top of a PDF.
        Title: A PDF will generally have only one Title and its Font size will be the highest.
        Heading: To Determine a heading, usually headings have the second-highest font size.
        Normal Text/Paragraph: The third highest are usually subheadings or normal text. Subheadings usually are also
                                highlighted in Bold, but since we are not considering font style, we cannot determine
                                subheadings. Hence, we will go with normal text.
    :param sorted_font_size: List containing unique font sizes of all texts in descending order.
    :return: Type of text
    """

    title_size = sorted_font_size[0]
    heading_size = sorted_font_size[1]
    normal_text_size = sorted_font_size[2]

    if font_size == title_size:
        return "Title"

    if not title_found:
        return "Header"

    if font_size == heading_size and title_found:
        return "Heading"

    if font_size == normal_text_size and title_found:
        return "Normal_text"

    if font_size < normal_text_size and title_found:
        return "Unknown-element"


def create_elements_json(text_list):
    """
    Create elements json and store it in a file.
    :param text_list: List containing all text properties.
    """
    try:
        elements_dict = dict()
        elements_dict["elements"] = []
        title_found = False
        for text_data in text_list:
            elements_data = dict()
            print(f"font size: {text_data['fontsize']}")
            text_type = classify_text(text_data["fontsize"], title_found)
            print(f"texttype: {text_type}")
            if text_type == "Title":
                print("coming here")
                title_found = True
            elements_data["type"] = text_type
            elements_data["text"] = text_data["text"]
            elements_dict["elements"].append(elements_data)
        with open("elements.json", 'w') as json_file:
            json.dump(elements_dict, json_file, indent=4)

        print("JSON file created")

    except Exception as error:
        print(f"Error: {error}")


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        pdf_path = config.get('FILEPATH', 'pdf_path')
        pdf_data = extract_data_from_pdf(pdf_path)
        text_list, table_and_graph_elements_coordinates_list, image_elements_coordinates_list = parse_pdf_data(pdf_data)
        textset = set()
        for textdict in text_list:
            textset.add(textdict['fontsize'])
        sorted_font_size = sorted(textset, reverse=True)
        create_elements_json(text_list)

    except Exception as error:
        print(f"Error: {error}")


