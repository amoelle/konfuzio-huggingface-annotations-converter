import os
import json
from utils import (process_all_documents, save_to_json, load_from_json, draw_boxes)


def draw_boxes_from_config():
    """
    Draw bounding boxes based on the configuration provided by the user.
    """
    
    project_id = input("Please enter the project ID: ")
    document_id = input("Please enter the document ID: ")
    page_number = input("Please enter the page number: ")
    
    file_path = f"data_{project_id}/documents/{document_id}/page_{page_number}.png"
    
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist. Please ensure you've entered the correct details.")
        return
    
    # Load the corresponding dataframe
    json_data = load_from_json(f'konfuzio_converted_project_{project_id}_dataset.json')
    
    doc_key = f"document_{document_id}"
    if doc_key not in json_data:
        print(f"Error: Document ID {document_id} data not found in stored datasets.")
        return
    
    dataframe_page = json_data[doc_key]['pages'][int(page_number) - 1]
    df = pd.DataFrame(dataframe_page)
    
    # Draw boxes on the image
    image = draw_boxes(file_path, df, 'bbox')  # or 'merged_bbboxes' or 'merged_bbboxes_by_line' based on your requirement
    image.show()

    return


def main():
    while True:
        print("\nChoose an option:")
        print("1. Load and Store Data from Konfuzio")
        print("2. Draw Visualized Data")
        print("3. Exit")
        choice = input("> ")

        if choice == "1":
            # Load configuration
            with open('config.json', 'r') as file:
                config = json.load(file)
            project_id = config["project_id"]
            document_types = config["document_types"]

            allowed_types = ["train", "test", "no_status", "preparation"]

            # Check for invalid document types
            invalid_types = [doc_type for doc_type in document_types if doc_type not in allowed_types]
        
            if invalid_types:
                print(f"Error: Invalid document types {invalid_types} found in config.json. Allowed types are {allowed_types}.")
                exit(1)

            project = Project(id_=project_id, update=True, strict_data_validation=False)

            # Call the process_and_store_documents function to handle further steps
            process_and_store_documents(project_number, document_types)

            print(f"Processing project {project_number} with document types {document_types}...")

        elif choice == "2":
            project_id = input("Enter Project ID: ")
            document_id = input("Enter Document ID: ")
            page_number = input("Enter Page Number: ")

            # Construct the expected file path based on user input
            file_path = os.path.join('../', f'data_{project_id}', 'documents', f'{document_id}', f'page_{page_number}.png')

            if os.path.exists(file_path):
                print(f"Drawing boxes for file {file_path}...")
                # Assuming you have a dataframe corresponding to this file. 
                # You might want to adjust how you fetch this dataframe.
                df = ... 
                draw_boxes(file_path, df, 'bbox')
            else:
                print(f"File {file_path} not found!")

        elif choice == "3":
            print("Exiting the application.")
            break

        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
