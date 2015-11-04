# FSND Project 3 - Item Catalog
_Originally forked from [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)._

# Vagrant Initialization

The included _Vagrantfile_ will take care of provisioning the virtual machine. Simply run:

`````
>vagrant up
`````

# Running the Application

Starting the app is simple, but requires a preparatory step.

## Connect via SSH
Once the Vagrant machine is up and running, connect via SSH.

`````
>vagrant ssh
`````

## Initialize the database
Run the _database.py_ initialization script to create the proper PostgreSQL
database schema.

`````
>cd /vagrant/catalog
>python database.py
`````
You can validate the schema by inspecting the 'catalog' database created by
the script.

## Start the Web application
From the project's directory, launch the main Flask web app.

`````
>cd /vagrant/catalog
>python catalog.py
`````

# Using the Application

The application supports OAuth2 via Google. You will need a Google Account for authenticating with the Catalog application.

## Load the app in your Browser
Navigate to [localhost:5000](http://localhost:5000) in your browser.

# References

I consulted a few online resources to help complete the project.

*Python*:
* Decorator Examples for Securing Methods : [Python Decorator Library](https://wiki.python.org/moin/PythonDecoratorLibrary#Access_control)
* StackOverflow : [How to make a python decorator function in Flask with arguments (for authorization)](http://stackoverflow.com/questions/13896650/how-to-make-a-python-decorator-function-in-flask-with-arguments-for-authorizati)

*HTTP File Uploads*:
* [jquery uploads](http://stackoverflow.com/questions/166221/how-can-i-upload-files-asynchronously)
* [uploading with flask](http://flask.pocoo.org/docs/0.10/patterns/fileuploads/)
