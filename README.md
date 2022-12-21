# OCP02 : Création d'un système de surveillance des prix
Projet dans le cadre de la formation OpenClassrooms - Formation développeur d'applications Python - Projet 02

Création d'un script de web scraping 

## Functions 
- Scans http://books.toscrape.com/index.html 
- Creates a .csv file per book category
- Extracts info from each book and stores it in csv file :
  - url page
  - Universal product code (upc)
  - Title
  - price including taxes
  - price excluding taxes 
  - Available stock
  - description
  - category
  - rating
  - url
- Downloads all book covers and saves them locally under their upc name


## Installing and running

### 1. Install Software requirements 
- Install Python 3.11+

### 2. Create Python project environment
1. n your terminal/IDLE position yourself in the directory where you want to create your project folder
> $ cd *//path//*
2. Create your project folder
> $ mkdir *Project_Name*
3. Create your project environment
> $ python -m venv env

### 3. Activate virtual environment
- From your project folder (this commande may change depending on your OS):
> $ ./env/Scripts/activate 

### 4. Install Pyhton packages
From your terminal or IDLE, install all packages listed in requirements.txt
> $ pip install -r requirements.txt

### 5. Run Script
From your project folder (or a different folder specifying the path) :
> $ python Script.py



## Files
### Output files
All output files will be saved in the **output folder**
- **output** 
  - **img** : folder containing all book cover images downloaded locally
  - **_category_.csv** : one file per category containing the list of books and the book info

### Temporal files
All temporal files are saved in the **tmp folder**
- **tmp**
  - **categories.csv** : lists all categories with names, codes and urls
  - **_category_code_.txt** : lists all books within a category
