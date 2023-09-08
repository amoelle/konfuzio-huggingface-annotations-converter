import os
import pandas as pd
import konfuzio_sdk
from konfuzio_sdk.data import Project
from konfuzio_sdk.tokenizer.regex import WhitespaceTokenizer as KWT
from nltk.tokenize import word_tokenize, NLTKWordTokenizer
from nltk.tokenize import WhitespaceTokenizer as WT
from PIL import Image, ImageDraw, ImageFont


def get_word_bboxes(document):

    raw_document = deepcopy(document)  # get Document with no Annotations
    tokenizer = KWT()
    tk_document = tokenizer(raw_document)
    tk_document.get_images(update=True)

    return tk_document


def process_all_documents(documents):
    """
    Process all documents and organize the results in a structured dictionary.

    Parameters:
    - documents: List of documents to be processed.

    Returns:
    - tabular_document_datasets_dict: A dictionary where the key is the document's name and 
      the value is another dictionary containing 'pages' and 'document_text'.
    """
    
    tabular_document_datasets_dict = {}

    for document in documents:
        # Get dataframes from the document
        no_label_annotations_df, label_annotations_df = get_dataframes_from_doc(document)
        
        # Transfer annotations and merge bounding boxes
        full_df = transfer_annotations(no_label_annotations_df, label_annotations_df)
        full_df = merge_bounding_boxes(full_df)
        
        # Split up full_df into chunks corresponding to the pages
        pages_list = []
        for _, group in full_df.groupby('file_name'):
            pages_list.append(group)
        
        # Store the data in the main dictionary
        tabular_document_datasets_dict[document.name] = {
            'pages': pages_list,
            'document_text': document.text
        }

    return tabular_document_datasets_dict


def process_word_bboxes_document(document):
    
    dataset_column_dictionary = {
        'annotation_id': [],
        'page_index': [],
        'line_number': [],
        'offset_string': [],
        'offset_string_original': [],
        'top': [],
        'bottom': [],
        'x0': [],
        'y0': [],
        'x1': [],
        'y1': [],
        'start_offset': [],
        'end_offset': [],
        'file_name': [],
        'file_path': []
    }

    annotations = document.get_annotations()
    file_paths_array = []
    for idx, _ in enumerate(annotations):
        nr_bboxes_in_annotations = len(annotations[idx].bboxes)

        annotation_id = annotations[idx].id_

        for bnr in range(nr_bboxes_in_annotations):

            bbox = annotations[idx].bboxes[bnr]
            line_number = bbox['line_number']

            page = document.pages()[bbox['page_index']]
            up_factor_x = page.get_image().width / page.width  # image > page, thus up_factor_x > 1
            up_factor_y = page.get_image().height / page.height # image > page, thus up_factor_y > 1

            page_index = bbox['page_index'] + 1
            top = bbox['top']
            bottom = bbox['bottom']
            x0 = bbox['x0'] * up_factor_x
            y0 = bbox['top'] * up_factor_y
            x1 = bbox['x1'] * up_factor_x
            y1 = bbox['bottom'] * up_factor_y
            start_offset = bbox['start_offset']
            end_offset = bbox['end_offset']
            offset_string = bbox['offset_string']
            file_name = "page_" + str(page_index) + ".png"
            file_path =  os.getcwd() + '/' + 'data_' + str(project_id) + '/documents/' + str(annotations[idx].document.copy_of_id) + "/" + file_name
            file_paths_array.append(file_path)

            dataset_column_dictionary['page_index'].append(page_index)
            dataset_column_dictionary['annotation_id'].append(annotation_id)
            dataset_column_dictionary['start_offset'].append(start_offset)
            dataset_column_dictionary['end_offset'].append(end_offset)
            dataset_column_dictionary['offset_string'].append(offset_string)
            dataset_column_dictionary['offset_string_original'].append(offset_string)
            dataset_column_dictionary['top'].append(top)
            dataset_column_dictionary['bottom'].append(bottom)
            dataset_column_dictionary['x0'].append(x0)
            dataset_column_dictionary['y0'].append(y0)
            dataset_column_dictionary['x1'].append(x1)
            dataset_column_dictionary['y1'].append(y1)
            dataset_column_dictionary['line_number'].append(line_number)
            dataset_column_dictionary['file_name'].append(file_name)
            if os.path.exists(file_path):
                dataset_column_dictionary['file_path'].append(file_path)
            else:
                dataset_column_dictionary['file_path'].append("NA")

    return dataset_column_dictionary, file_paths_array


def transfer_annotations(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:

    no_label_annotations_df = df1.copy()
    label_annotations_df = df2.copy()

    # Initialize the new columns 'label' and 'label_set' in df1 with default values
    no_label_annotations_df['label'] = 'NO_LABEL'
    no_label_annotations_df['label_set'] = 'NO_LABEL_SET'

    # Iterate through the rows of df1 and df2 and check for matching spans
    for index1, row1 in no_label_annotations_df.iterrows():
        for index2, row2 in label_annotations_df.iterrows():
            if row1['start_offset'] >= row2['start_offset'] and row1['end_offset'] <= row2['end_offset']:
                no_label_annotations_df.at[index1, 'label'] = row2['label']
                no_label_annotations_df.at[index1, 'label_set'] = row2['label_set']
                no_label_annotations_df.at[index1, 'annotation_id'] = row2['annotation_id']
                break  # break the inner loop once a match is found
    
    full_df = no_label_annotations_df

    full_df['bbox'] = list(map(list, zip(full_df['x0'].astype(int), full_df['y0'].astype(int), full_df['x1'].astype(int), full_df['y1'].astype(int))))

    return full_df


from PIL import Image, ImageDraw, ImageFont

def draw_boxes(image_path: str, dataframe: pd.DataFrame, bbox_column: str) -> Image.Image:
    """
    Draw bounding boxes and their labels on the image.

    Parameters:
    - image_path: Path to the image on which bounding boxes will be drawn.
    - dataframe: DataFrame containing bounding boxes and labels.
    - bbox_column: Column name in the dataframe which contains bounding boxes.
    
    Returns:
    - Modified image with bounding boxes and labels.
    """
    
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    width, height = image.size

    # Initialize drawing context and font
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    dataframe = dataframe[dataframe['file_path'] == image_path]

    for _, row in dataframe.iterrows():
        # Extract bounding box and label from the dataframe
        #print(row[bbox_column])
        #print(type(row[bbox_column]))
        #box = eval(row[bbox_column])  # Convert string representation of list to actual list
        box = row[bbox_column]
        label = row['label']
        
        # Draw the bounding box on the image
        draw.rectangle(box, outline="red", width=2)
        
        # Calculate label position (slightly above the bounding box)
        if label != 'NO_LABEL':
            label_position = (box[0], box[1] - 15)  # 15 pixels above the bounding box
            draw.text(label_position, label, font=font, fill="blue")
    
    return image


def save_to_json(data_dict, file_path):
    """
    Save the provided dictionary to a JSON file.

    Parameters:
    - data_dict: Dictionary to be saved. It contains lists of DataFrames.
    - file_path: Path to the file where the dictionary will be saved.
    """
    
    # Convert DataFrames to a serializable format (dictionary)
    serializable_dict = {}
    for doc_key, doc_value in data_dict.items():
        pages_list_serializable = [page_df.to_dict(orient='records') for page_df in doc_value['pages']]
        serializable_dict[doc_key] = {
            'pages': pages_list_serializable,
            'document_text': doc_value['document_text']
        }

    # Save the serializable dictionary to a JSON file
    with open(file_path, 'w') as file:
        json.dump(serializable_dict, file)

def load_from_json(file_path):
    """
    Load a dictionary from a JSON file and convert serialized data back to DataFrames.

    Parameters:
    - file_path: Path to the JSON file.

    Returns:
    - Dictionary with lists of DataFrames.
    """
    
    # Load the dictionary from the JSON file
    with open(file_path, 'r') as file:
        loaded_dict = json.load(file)

    # Convert serialized data back to DataFrames
    dataframes_dict = {}
    for doc_key, doc_value in loaded_dict.items():
        pages_list_df = [pd.DataFrame(page_data) for page_data in doc_value['pages']]
        dataframes_dict[doc_key] = {
            'pages': pages_list_df,
            'document_text': doc_value['document_text']
        }

    return dataframes_dict
