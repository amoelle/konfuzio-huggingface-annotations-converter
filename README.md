# konfuzio-huggingface-annotations-converter

Description: This application serves two primary purposes:

1. Load data from a specified Konfuzio project and store it in a structured, more general format (tabular, HuggingFace, ...).
2. Visually draw bounding boxes on images to verify the transformed OCR data and annotations.

## Usage

1. **Configuration**: 

   Before starting the application, set your desired parameters in the `config.json` file.
   - `project_number`: The project number from Konfuzio.
   - `document_types`: A list containing the types of documents you want to load. This can be any combination of "train", "test", "no_status", and "preparation".

2. **Start the Application**:

Run the `main.py` script. You will be presented with a menu of options:

Choose an option:

1. Load and Store Data from Konfuzio
2. Draw Visualized Data
3. Exit

- Choose `1` to load and store data based on the parameters set in `config.json`.
- Choose `2` to draw visualized data. You will be prompted to provide the `project_id`, `document_id`, and `page_number`. The application will then attempt to draw bounding boxes for the specified file if it exists.
- Choose `3` to exit the application.

3. **Data Visualization**:

When choosing to draw visualized data, ensure you provide the correct `project_id`, `document_id`, and `page_number`. The application will check for the existence of the corresponding file and draw bounding boxes if the file exists.

## Requirements

Ensure you have all the required packages installed using:

pip install -r requirements.txt

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Setup
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the main script using `python main.py`.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## Directory Structure

konfuzio-huggingface-annotations-converter/
│
├── annotations_converter/
│   ├── main.py
│   └── utils.py
│
├── data/
│   └── ... ( data files)
│
├── tests/
│   └── ... (any test scripts)
│
├── requirements.txt
└── README.md
