# FIR - Dishvision 2.0

FIR - Food Image Recognition (Dishvision 2.0)

Main Objective:
Develop a web application for local food image recognition and nutritional intake estimation to assist patients in managing their diet.

Objectives:
Develop a system for users to log food images and nutritional intake.
Create a simple GUI for image input for local food analysis.
Train and test food recognition models, including customization for local cuisine in Singapore.
Integrate existing databases for mapping food to weight and retrieving nutritional information.
Deploy the system on a python-based web platform.
Conduct testing to ensure accuracy and usability.
Finalize documentation & Project Submittables.


Academic Supervisor: 
Daniel Wang Zhengkui

Industry Supervisor: 
Zhengyi Kwan

Team Members:
Tan Jing Yuan, 
Ong Sheng Long, 
Fu Shaoyu, 
Ng Zi Hwee, 
Low Yi San

# Instructions for Setting Up and Running DishVision 2.0

## 1. Prerequisites

### System Requirements
- **Python**: Version 3.10 or higher installed.
- **Internet Connection**: Required for downloading necessary files and libraries.
- **GPU Drivers and CUDA Toolkit**: Ensure GPU drivers and the CUDA toolkit (if applicable) are properly installed for optimal performance.

### Required Files
Download the following model files and place them in the respective directories:

1. **Mass Estimation Model**  
   [Mass Estimation Model Download Link](https://sitsingaporetechedu-my.sharepoint.com/:u:/g/personal/2201241_sit_singaporetech_edu_sg/EZIv4oteiFlIkpGsnXDtpggBZh7vsYWklx3zKmndFKcmUQ?e=QidY64)  
   **Location**: `FIR/experiment/37c9ed248cc58c1dae423f304c095d48a9f8150e.ckpt`

2. **Food Recognition Model**  
   [Food Recognition Model Download Link](https://sitsingaporetechedu-my.sharepoint.com/:u:/g/personal/2201241_sit_singaporetech_edu_sg/EcTVU-9t5Q5FpHpgDuI0HokBNd7F3OWoXdAbQXF_hftmOg?e=o8DbxW)  
   **Location**: `FIR/output_minicpmv2`  
   *This directory should contain multiple files such as:*
   - `model-00001-of-00003.safetensors`
   - `model-00002-of-00003.safetensors`
   - `model-00003-of-00003.safetensors`
   - Other configuration files.

3. **Apple's Depth Estimation Model**  
   [Depth Estimation Model Download Link](https://drive.google.com/drive/folders/1QVXTHZPzSIIN3FO5czClRvls7WjNolpy?usp=sharing)  
   **Location**: `FIR/checkpoints/depth_pro.pt`

---

## 2. Setting Up the Environment

### Step 1: Navigate to the Project Directory
Open a terminal or command prompt and change the current directory to the main project folder:

cd path_to_project_directory

---

### Step 2: Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:

#### 1. Create Virtual Environment:

python -m venv venv

#### 2. Activate Virtual Environment:
- **On Windows**:
venv\Scripts\activate

- **On macOS/Linux**:
source venv/bin/activate

---

### Step 3: Install Required Libraries
Use the `requirements.txt` file to install all necessary dependencies:

pip install -r requirements.txt


---

## 3. Running the Application

### Step 1: Launch the Web Application
Within the active virtual environment, execute the following command to start the Streamlit server:

streamlit run app.py

### Step 2: Wait for Model and Backend Initialization
The application will load the pre-trained models (Mass Estimation and Food Recognition) and initialize the knowledge graph backend. This may take a few moments depending on your system's resources.

### Step 3: Verify Successful Launch
Once the application has fully loaded, it will display a login screen in your default web browser. If the login screen appears without errors, DishVision 2.0 is ready to use.

### Test Account:
- **Email**: test@gmail.com  
- **Password**: 123456789  

---

## 4. Troubleshooting

### Potential Version Error:
If you encounter the error: IndexError: index is out of bounds for dimension with size 0

This indicates that your `transformers` library version is incompatible. Use the following command to install the correct version:

pip install transformers==4.36.0

### CUDA Version Issues:
The CUDA version used for the project was **CUDA 12.1**. Upgrading or downgrading to this version might solve CUDA-related errors.

---

This guide provides the necessary instructions for setting up, running, and troubleshooting DishVision 2.0. For additional help, refer to the documentation in the project repository or contact the development team.


















