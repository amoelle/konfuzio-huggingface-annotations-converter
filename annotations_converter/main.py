import os
import json
import pandas as pd
from utils import (process_all_documents, save_to_json, load_from_json, draw_boxes)


def draw_boxes_from_user_input():
    """
    Draw bounding boxes based on the configuration provided by the user.
    """
    
    project_id = input("Please enter the project ID: ")
    document_id = input("Please enter the document ID: ")
    page_number = input("Please enter the page number: ")

    # Prompt the user for the type of bounding box2
    bbox_type = input("Choose the type of bounding box to draw ( bbox / merged_bbboxes / merged_bbboxes_by_line ): ")
    while bbox_type not in ['bbox', 'merged_bbboxes', 'merged_bbboxes_by_line']:
        print("Invalid choice. Please select a valid bounding box type.")
        bbox_type = input("Choose the type of bounding box to draw ( bbox / merged_bbboxes / merged_bbboxes_by_line ): ")
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Move one directory up from the script's directory
    parent_dir = os.path.dirname(script_dir)

    konfuzio_document_dir = f"data_{project_id}/documents/{document_id}/"
   
 
    # Path to stored data
    data_dir = "data"
    file_name = f"project_{project_id}_docs.json"
    # Construct the file path relative to the script's directory
    dir_path = os.path.join(parent_dir, data_dir) 
    file_path = os.path.join(dir_path, file_name) 

    # Load the corresponding dataframe
    print(f"Trying to load {file_path} ...")
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist. Please ensure you've entered the correct details.")
        return
    json_data = load_from_json(file_path)

    doc_key = f"{document_id}"
    if doc_key not in json_data:
        print(f"Error: Document ID {document_id} not found in stored datasets.")
        return
    
    while len(json_data[doc_key]['pages']) < int(page_number):
        page_number = input("Specified page number out of range. Please enter a page number smaller or equal {}:".format(len(json_data[doc_key]['pages'])))
        
    image_name = f"page_{page_number}.png"
    # Construct the file path relative to the script's directory
    image_path = os.path.join(parent_dir, konfuzio_document_dir, image_name) 
    if not os.path.exists(image_path):
        print(f"Error: Image {file_path} does not exist. Please ensure it was saved before.")
        return
    
    image_short_path = os.path.join(konfuzio_document_dir, image_name) 
    dataframe_page = json_data[doc_key]['pages'][int(page_number) - 1]
    df = pd.DataFrame(dataframe_page)
    print(df.head())

    # Draw boxes on the image
    image = draw_boxes(image_path, image_short_path, df, bbox_type)  # or 'merged_bbboxes' or 'merged_bbboxes_by_line' based on your requirement
    #image.show()
    image_save_path = os.path.join(parent_dir, data_dir, "output.png")
    image.save(image_save_path)

    return
1
def process_documents_from_config(config):
    """
    Handle processing of documents based on the provided configuration.
    """
    
    # Extract configuration details
    project_id = config["project_id"]
    document_types = config["document_types"]
    allowed_types = ["train", "test", "no_status", "preparation"]
    max_nr_docs_per_type = config['max_nr_docs_per_type']

    # Check for invalid document types
    invalid_types = [doc_type for doc_type in document_types if doc_type not in allowed_types]

    if invalid_types:
        print(f"Error: Invalid document types {invalid_types} found in config.json. Allowed types are {allowed_types}.")
        exit(1)
    
    print(f"Processing project {project_id} with document types {document_types}...")
    # Process the documents
    tabular_document_datasets_dict = process_all_documents(project_id, document_types, max_nr_docs_per_type)
    
    #document_types_string = "_".join(document_types)
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Move one directory up from the script's directory
    parent_dir = os.path.dirname(script_dir)
    data_dir = "data"
    file_name = f"project_{project_id}_docs.json"
    # Construct the file path relative to the script's directory
    dir_path = os.path.join(parent_dir, data_dir) 
    file_path = os.path.join(dir_path, file_name) 

    if not os.path.exists(dir_path):
        print(f"Error: Directory {dir_path} does not exist. Please ensure you've entered the correct details.")
    else:
        print(f"Saving {file_path} ...")
        # Store the processed data
        save_to_json(tabular_document_datasets_dict, file_path)

    return

def main():
     
    while True:
        print("\nChoose an option:")
        print("1. Load and Store Data from Konfuzio")
        print("2. Draw Visualized Data")
        print("3. Exit")
        choice = input("> ")
    
        if choice == "1":

            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(script_dir, f"./config.json") 

            # Load configuration
            with open(file_path, 'r') as file:
                config = json.load(file)

            # Call the process_documents_from_config function
            process_documents_from_config(config)
            break
        
        elif choice == "2":
            
            draw_boxes_from_user_input()
            break

        elif choice == "3":
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please select again.")


if __name__ == "__main__":
    
    main()
