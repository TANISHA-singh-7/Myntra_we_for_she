# Myntra_we_for_she
# TAO: Try Any Outfit

<h1 align="center">TAO: Try Any Outfit</h1>

*Team:* SheInnovates

## Overview

TAO (Try Any Outfit) is an innovative application that allows users to virtually try on different outfits using images of their own bodies. By leveraging advanced face and pose detection algorithms, TAO ensures that the chosen outfits are displayed accurately and realistically on the user's image.

## Features

- *Clothing Image Upload:* Users can upload images of clothing items they wish to try on.
- *Pose Image Upload:* Users can upload their pose images, ensuring the outfit fits correctly.
- *Face Detection:* Utilizes the MTCNN face detection algorithm to ensure the face is correctly identified and positioned.
- *Category Selection:* Users can choose between different clothing categories (upper cloth, lower cloth, full body, dresses).
- *Denoise Steps:* Allows users to adjust the denoising steps for better image quality.
- *Task Management:* Manages user tasks, providing feedback on task status and history of past attempts.

## How to Use

1. *Upload Images:* Start by uploading a clothing image and a pose image.
2. *Select Category:* Choose the category of clothing from the dropdown menu.
3. *Adjust Settings:* Adjust the denoise steps if necessary and provide a caption for the outfit.
4. *Run the Task:* Click the "Run" button to start processing.
5. *View Results:* The resulting image will be displayed along with runtime information.

## Installation

To run TAO locally, follow these steps:

1. *Clone the Repository:*
    bash
    git clone https://github.com/your-repo/tao-try-any-outfit.git
    cd tao-try-any-outfit
    

2. *Install Dependencies:*
    bash
    pip install -r requirements.txt
    

3. *Run the Application:*
    bash
    python app.py
    

4. *Access the Application:*
    Open your web browser and navigate to http://localhost:7860.

## Dependencies

- MTCNN
- gradio
- utils (custom utility functions)
- Other Python dependencies as listed in requirements.txt

## Code Explanation

### Main Components

- *Image Upload:* Allows users to upload images for the cloth and pose.
- *Face Detection:* Uses MTCNN to detect faces in the uploaded pose image.
- *Result Generation:* Generates the result by combining the cloth image with the pose image.
- *Task Management:* Handles the creation and management of user tasks, including error handling and task status updates.

### Key Functions

- onUpload: Handles image upload actions.
- onClick: Processes the images, runs face detection, and manages task creation.
- onLoad: Loads the history of user tasks and displays them.

## Examples

The application includes example images for both clothing and poses to help users get started quickly.

## Troubleshooting

If you encounter any issues while using TAO, please check the following:

- Ensure that the uploaded images are clear and meet the required specifications.
- Make sure the face is visible and not too large in the pose image.
- If the server is under maintenance, try again later.

## Contributions

We welcome contributions from the community. If you would like to contribute to TAO, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.

---

We hope you enjoy using TAO! If you have any questions or feedback, feel free to reach out to us.

---

By SheInnovates