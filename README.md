
# About:
Backend Flask application for the CareerSync recommendation system

Used for the actual recommendation system through the Recommender class and supplies the front end for some more information 
for the user.


## How do I build and run this?

### Step 1:
Extract the job-description-final.rar to 
```job-description-final.csv``` 
in the current directory

### Step 2:
activate the Virtual Environement through this command:

```bash
.\venv\Scripts\activate 
```

### Step 3:
Download and install the dependencies:

```bash
pip install requirements.txt
```
### Step 4:
run the application

```bash
flask --app .\skillsApi.py --debug run
```

That's it for the flask part check the React and Spring part.
