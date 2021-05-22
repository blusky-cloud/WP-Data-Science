# WP-Data-Science
Created by Whitman Spitzer 5/17/2021

This is a repository for code relating to the analysis of Federal Spending Data using Python.

### Data
Currently, in the data/testing folder, there is a .txt file with the output of the test request we made.
In the `first_contact.py` script, you can change the name of the file name variable `data_file_name` to be whatever you want, it will save as a new .txt file the next time you run the script (with whatever specific request you make). In the `save_json_to_file` function, there is a call to `open(data_file_name, 'w')`, this will save the data in a `.txt` file in whatever folder you have the Python script stored. If you copy this repository (we'll walk through it later) you can change that to save the file in the `data` folder, under `testing` the way it's shown here.

### Python Code
Code is currently stored in the source/live folder, the script right now is called `first_contact.py`

### Dependencies
Thus far, development has been in PyCharm, in virtual environments. We already installed these on your computer, but it's a good idea to document the process for when you need to do it again. The dependencies thus far can be installed with the following command line (terminal) arguments:
```bash
pip install requests && pip install requests-toolbelt && pip install pandas && pip install beautifulsoup4
```
