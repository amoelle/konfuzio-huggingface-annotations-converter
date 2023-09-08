import os
import pandas as pd
import konfuzio_sdk
from konfuzio_sdk.data import Project
from konfuzio_sdk.tokenizer.regex import WhitespaceTokenizer as KWT
from nltk.tokenize import word_tokenize, NLTKWordTokenizer
from nltk.tokenize import WhitespaceTokenizer as WT
from PIL import Image, ImageDraw, ImageFont
from copy import deepcopy
import json


def get_word_bboxes(document):

    raw_document = deepcopy(document)  # get Document with no Annotations
    tokenizer = KWT()
    tk_document = tokenizer(raw_document)
    tk_document.get_images(update=True)

    return tk_document


def process_annotated_document(document):
    dataset_column_dictionary = {
        'annotation_id': [],
        'page_index': [],
        'line_number': [],
        'top': [],
        'bottom': [],
        'x0': [],
        'y0': [],
        'x1': [],
        'y1': [],
        'label': [],
        'label_set': [],
        'start_offset': [],
        'end_offset': [],
        'offset_string': [],
        'file_name': [],
        'file_path': [],
    }

    annotations = document.get_annotations()
    file_paths_array = []
    for idx, _ in enumerate(annotations):
        
        if annotations[idx].is_correct != True:
            continue
        
        nr_bboxes_in_annotations = len(annotations[idx].bboxes)

        annotation_id = annotations[idx].id_

        for bnr in range(nr_bboxes_in_annotations):

            bbox = annotations[idx].bboxes[bnr]

            page = document.pages()[bbox['page_index']]
            line_number = bbox['line_number']
            up_factor_x = page.get_image().width / page.width  # image > page, thus up_factor_x > 1
            up_factor_y = page.get_image().height / page.height # image > page, thus up_factor_y > 1

            page_index = bbox['page_index'] + 1
            top = bbox['top']
            bottom = bbox['bottom']

            x0 = bbox['x0'] * up_factor_x
            y0 = bbox['top'] * up_factor_y
            x1 = bbox['x1'] * up_factor_x
            y1 = bbox['bottom'] * up_factor_y

            label = annotations[idx].label.name_clean
            label_set = annotations[idx].label_set.name_clean
    
            start_offset = bbox['start_offset']
            end_offset = bbox['end_offset']
            offset_string = bbox['offset_string']
            file_name = "page_" + str(page_index) + ".png"

            project_id = document.project.id_

            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            parent_dir = os.path.dirname(script_dir)
            document_id = str(annotations[idx].document.copy_of_id)
            konfuzio_document_dir = f"data_{project_id}/documents/{document_id}/"
            full_file_path = os.path.join(parent_dir, konfuzio_document_dir, file_name) 
            file_path = os.path.join(konfuzio_document_dir, file_name) 
            file_paths_array.append(file_path)

            dataset_column_dictionary['annotation_id'].append(annotation_id)
            dataset_column_dictionary['page_index'].append(page_index)
            dataset_column_dictionary['line_number'].append(line_number)

            dataset_column_dictionary['top'].append(top)
            dataset_column_dictionary['bottom'].append(bottom)
            dataset_column_dictionary['x0'].append(x0)
            dataset_column_dictionary['y0'].append(y0)
            dataset_column_dictionary['x1'].append(x1)
            dataset_column_dictionary['y1'].append(y1)


            dataset_column_dictionary['label'].append(label)
            dataset_column_dictionary['label_set'].append(label_set)
            dataset_column_dictionary['start_offset'].append(start_offset)
            dataset_column_dictionary['end_offset'].append(end_offset)
            dataset_column_dictionary['offset_string'].append(offset_string)
            dataset_column_dictionary['file_name'].append(file_name)
            dataset_column_dictionary['file_path'].append(file_path)

            # if os.path.exists(file_path):
            #     dataset_column_dictionary['file_path'].append(file_path)
            # else:
            #     dataset_column_dictionary['file_path'].append("NA")

    return dataset_column_dictionary, file_paths_array


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
        'file_path': [],
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

            project_id = document.project.id_

            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            parent_dir = os.path.dirname(script_dir)
            document_id = str(annotations[idx].document.copy_of_id)
            konfuzio_document_dir = f"data_{project_id}/documents/{document_id}/"
            full_file_path = os.path.join(parent_dir, konfuzio_document_dir, file_name) 
            file_path = os.path.join(konfuzio_document_dir, file_name)
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
            dataset_column_dictionary['file_path'].append(file_path)
            
            # if os.path.exists(file_path):
            #     dataset_column_dictionary['file_path'].append(file_path)
            # else:
            #     dataset_column_dictionary['file_path'].append("NA")

    return dataset_column_dictionary, file_paths_array



def get_dataframes_from_doc(document: konfuzio_sdk.data.Document) -> konfuzio_sdk.data.Document:
    
    doc_with_word_level_bboxes = get_word_bboxes(document)
    word_boxes_dataset_column_dictionary, _ = process_word_bboxes_document(doc_with_word_level_bboxes)
    no_label_annotations_df = pd.DataFrame(word_boxes_dataset_column_dictionary)

    dataset_column_dictionary, _ = process_annotated_document(document)
    label_annotations_df = pd.DataFrame(dataset_column_dictionary)

    return no_label_annotations_df, label_annotations_df



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



def merge_bounding_boxes(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Merge bounding boxes based on 'annotation_id' and 'annotation_id' + 'line_number'.
    
    Parameters:
    - dataframe: DataFrame containing the 'bbox', 'annotation_id', and 'line_number' columns
    
    Returns:
    - DataFrame with the added 'merged_bbboxes' and 'merged_bbboxes_by_line' columns
    """
    
    # --- First Round: Merge based on annotation_id only ---
    
    def merge_bboxes(group):
        """
        Merge bounding boxes for a group of rows.
        """
        # Ensure that the 'bbox' column contains strings
        bboxes_str = group['bbox'].astype(str)
        
        # Extract bounding boxes from the 'bbox' column
        bboxes = bboxes_str.str.strip("[]").str.split(",", expand=True).astype(float)
        
        # Compute the merged bounding box
        merged_bbox = [
            int(bboxes[0].min()),  # x0
            int(bboxes[1].min()),  # y0
            int(bboxes[2].max()),  # x1
            int(bboxes[3].max())   # y1
        ]
        
        return merged_bbox
    
    # Group by 'annotation_id' and apply the merge_bboxes function
    merged_bboxes_dict = dataframe.groupby('annotation_id').apply(merge_bboxes).to_dict()

    # Map the merged bounding boxes to the original dataframe using 'annotation_id' as the key
    dataframe['merged_bbboxes'] = dataframe['annotation_id'].map(merged_bboxes_dict)
    
    # For rows without a related annotation, copy the bounding box from 'bbox'
    dataframe['merged_bbboxes'].fillna(dataframe['bbox'], inplace=True)
    
    # --- Second Round: Merge based on annotation_id and line_number ---
    
    # Group by 'annotation_id' and 'line_number' and apply the merge_bboxes function
    key = dataframe['annotation_id'].astype(str) + "_" + dataframe['line_number'].astype(str)
    merged_bboxes_by_line_dict = dataframe.groupby(['annotation_id', 'line_number']).apply(merge_bboxes).to_dict()

    # Convert multi-index dict keys to concatenated string keys with underscore separator
    merged_bboxes_by_line_dict = {str(k[0]) + "_" + str(k[1]): v for k, v in merged_bboxes_by_line_dict.items()}

    # Map the merged bounding boxes to a new column in the dataframe using the unique key
    dataframe['merged_bbboxes_by_line'] = key.map(merged_bboxes_by_line_dict)
    
    # For rows without a merged bounding box based on both annotation_id and line_number, copy the bounding box from 'bbox'
    dataframe['merged_bbboxes_by_line'].fillna(dataframe['bbox'], inplace=True)
    
    return dataframe



def process_all_documents(project_id, document_types, max_nr_docs_per_type):
    """
    Process all documents and organize the results in a structured dictionary.

    Parameters:
    - documents: List of documents to be processed.

    Returns:
    - tabular_document_datasets_dict: A dictionary where the key is the document's name and 
      the value is another dictionary containing 'pages' and 'document_text'.
    """
    
    project = Project(id_=project_id, update=True, strict_data_validation=False)

    document_types_dict = {
        'train': project.documents,
        'test': project.test_documents,
        'no_status': project.no_status_documents,
        'preparation': project.preparation_documents
        }
    
    documents = []
    for doc_type in document_types:
        documents.extend(document_types_dict[doc_type][:max_nr_docs_per_type])

    tabular_document_datasets_dict = {}

    for document in documents:
        print("Processing document {} ...".format(document.name))
        
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
        tabular_document_datasets_dict[document.id_] = {
            'project_id': project_id,
            'document_name': document.name,
            'document_status': document.status,
            'document_text': document.text,
            'pages': pages_list,
        }

    return tabular_document_datasets_dict



def draw_boxes(image_path: str, image_short_path: str, dataframe: pd.DataFrame, bbox_column: str) -> Image.Image:
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

    print("image_path: ", image_path)
    print("image_short_path: ", image_short_path)
    
    dataframe = dataframe[dataframe['file_path'] == image_short_path]
    print(dataframe.head())

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
            'project_id': doc_value['project_id'],
            'document_name': doc_value['document_name'],
            'document_status': doc_value['document_status'],
            'document_text': doc_value['document_text'],
            'pages': pages_list_serializable,
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
            'project_id': doc_value['project_id'],
            'document_name': doc_value['document_name'],
            'document_status': doc_value['document_status'],
            'document_text': doc_value['document_text'],
            'pages': pages_list_df,
        }

    return dataframes_dict
