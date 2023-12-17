### README.md for BCI Experiment (EEG Data Analysis) 

#### Project Overview

This repository contains a BCI (Brain-Computer Interface) experiment project focusing on EEG (Electroencephalogram) data analysis. It includes datasets from the BCI Competition 2008 - Graz data set B, scripts for data preprocessing and analysis, Jupyter notebooks for model training, and utility scripts.

#### Repository Structure

- `dataset/`: EEG data files in GDF format from BCI Competition (e.g., `B0101T.gdf`, `B0105E.gdf`, etc.)
- `models/`: Jupyter notebooks (`svm.ipynb`) and HTML outputs (`svm.html`) for SVM model training and analysis.
- `utils/`: Utility scripts like `get_csv_from_gdf.py` for data conversion.
- `docs/`: Documentation including `desc_2b.pdf` describing the EEG dataset.
- Other directories: `archived`, `requirements.txt`, and a Python virtual environment directory `venv-bci-experiment-1`.

#### Setup Instructions

1. **Clone the Repository:**
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set Up a Python Virtual Environment:**
   ```
   python -m venv venv-bci-experiment-1
   source venv-bci-experiment-1/bin/activate  # On Windows: `venv-bci-experiment-1\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Running the Notebooks:**
   ```
   jupyter notebook
   ```
   Navigate to `models/` to access and run the Jupyter notebooks.

#### Usage

- Convert GDF files to CSV using `utils/get_csv_from_gdf.py` for preprocessing.
- Analyze EEG data and train models using the notebooks in the `models/` directory.

#### Contributing

Feel free to contribute to this project by submitting issues or pull requests. For detailed dataset information, refer to `docs/desc_2b.pdf`.