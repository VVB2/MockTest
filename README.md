# Getting Started with this Project

## About this project

This is a `Flask and MySQL` website to help students practice `JAVA`/`Python` by giving **MockTest** i.e *MCQ* of the selected language

---

## Prerequisite

You need to have [pip](https://pypi.org/project/pip/) and [python3](https://www.python.org/downloads/) installed on your machine

---

## Project Setup

### Steps to successfully run this project

- Install all the dependencies using\
`pip install requirements.txt`

- Start the virtual environment\
    - Mac OS / Linux \
    `source mypython/bin/activate`

    - Windows \
    `mypthon\Scripts\activate`

- Start the app using \
    `python3 mocktest.py`

- Stop the virtual environement using \
    `deactivate`
    
## Project folders

- **`mocktest`**
    - **`mocktest/errors`** - contains the **functions** responsible to show error pages due to `404, 403, 500` errors 
    - **`mocktest/main`** - contains the `Home` page display function
    - **`mocktest/static`** - contains all the static assets
    - **`mocktest/templates`** - contains all the `UI` pages that will be visible to the user
    - **`mocktest/tests`** - contains the routes for the **JAVA, Python** MCQs
    - **`mocktest/users`** - contains all the files to `create, update or delete` users and the routes associated with the same
    - **`mocktest/models.py`** - contains the models for the database
    - **`mocktest/utils.py`** - to enter the data from `.json` file automatically into the database
- **`mocktest.py`** - contains the entry `.py` file to run this app
- **`requirements.txt`** - contains all the requirements that are required to successfully run this project

--- 
