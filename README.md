This tool is currently deployed on the streamlit community cloud and can be accessed via ...
```
https://kit-grade-analyzer.streamlit.app
```

# About the Project
Cohort analysis and comparison of final graduates grades at KIT.  
Uses and aggregates / analyzes the final KIT grades published at the 
[KIT ECTS Ranking Chart](https://www.sle.kit.edu/nachstudium/ects-einstufungstabellen.php).

# Example Preview
![](assets/readme/ui_example.png)

# Installation

1. Clone the repository by running the following command in your terminal:

   ```
   git clone https://github.com/negralessio/kit-grade-analyzer.git
   ```


2. Navigate to the project root directory by running the following command in your terminal:

   ```
   cd kit-grade-analyzer
   ```

3. Create a virtual environment and activate it (Python Version 3.11).
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages by running the following command in your terminal:

   ```
   pip install -r requirements.txt
   ```

5. (Optional). Install pre-commit to help adhering to code styles and mitigating minor issues
   ```
   pre-commit install
   ```

# How To Run:
1. Run GUI, while in root dir, via:

   ```
   streamlit run gui/app.py
   ```

2. Simply add one or more URL into the corresponding text field.
