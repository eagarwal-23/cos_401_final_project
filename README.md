# COS 401 Final Project
## Authors: Eesha Agarwal, Kaleb Areda, Addele Hargenrader, Hyunsung Yun

## Directory Structure

app.py implements the frontend interface for each of our metrics, which are
implemented separately in emotions.py, lexical.py, semantic.py, and syntactic.py.

Each of the backend metrics can be run separately by supplying two arguments,
one for the original (in French) and one for the translation.

data/ contains the poems that were used for analysis. FEEL.csv and nrc.txt are
databases that we used to do implement the metrics.

## Running the Backend Driver

translators.py drives all four backends while also generating machine translations.
Need two arguments to run translators.py: the first is the poem to translate,
and the second is a translation for comparison.

`python translators.py poem1.txt poem1_en.txt`

## Running the Frontend Web App

After setting your working directory to the this directory's location, follow the following commands in your terminal to launch the frontend web app in your browser:

- pip install flash
- pip install -r requirements.txt
- python app.py

The last command will generate a prompt in terminal that will say something like "Running on http://127.0.0.1:5000". Copy the printed link into your browser to open the Frontend web app.


