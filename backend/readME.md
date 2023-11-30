# Backend Documentation #

## Main Tools Used ##
- SQLAlchemy:
    - Purpose: 
        - Simplifies database interactions by providing a high-level
        - Pythonic interface to relational databases
        - Has object-relational mapping, SQL expression language, and database abstraction
    - [Documentation Link](https://docs.sqlalchemy.org/en/20/orm/)
- FastAPI
    - Purpose: 
        - API implementation - used to build high-performance web APIs with Python, 
        - Offers automatic documentation and validation
        - Development through a declarative, type-annotated approach.
    - [Documentation Link](https://fastapi.tiangolo.com/)
- Pydantic 
    - Purpose
        - Used for data validation and parsing in Python (fastapi uses this)
        - Flexible way to define data models w/ type hints and enables detailed documentation
    - [Documentation Link](https://docs.pydantic.dev/latest/)
- MySQL 
    - Purpose: Relational database for information storage
    - [Documentation Link](https://dev.mysql.com/doc/)
    
## Local Environment Setup Instructions: ##

### Two Options ##
1. Using conda environment with .yml file

 - Install Conda Environment from their [official website](https://www.anaconda.com/products/distribution) 
 - Inside capstoneproject/backend, run: `conda env create -f environment.yml`
 - Activate the environment: `conda activate my_env` (replace my_env with name of your environment)
 - To deactivate, run `conda deactivate`
 - Remember to always activate your environment before you start your work!
 - To install anything new into your environment, first try `conda install` *before* `pip install` but remember to 
 update your requirements.txt with any new dependencies for docker purposes.
 - **[Conda Cheat Sheet](https://conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)**
 - [Conda Documentation](https://conda.io/projects/conda/en/latest/user-guide/index.html)



2. Pip Install
 - In your local environment (whether in a python virtual environment , etc.) inside capstoneproject/backend, run: `pip install -r requirements.txt`
 - Always ensure to add any new dependencies into requirements.txt


## Backend Design Overview ##

