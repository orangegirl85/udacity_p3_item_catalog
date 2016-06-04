# Item Catalog
--------------

    * This is an application that provides a list of items within a variety of categories as well as
    provide a user registration and authentication system. Registered users will have the ability to post, edit
    and delete their own categories and items.

    * Used technologies: Flask, SQLAlchemy, Facebook, Google+ Authentication


# Prerequisites
---------------
1. Install Vagrant and VirtualBox

2. Clone the `fullstack-nanodegree-vm repository`

3. Clone https://github.com/orangegirl85/udacity_p3_item_catalog repository
   into fullstack/vagrant/catalog


# Run App for Mac users
-----------------------
1. Launch the Vagrant VM
```
    vagrant up
    vagrant ssh
```

2. Navigate to catalog folder:

`cd /vagrant/catalog`

3. Run app in order to set database:

`python run.py`

4. Populate database

`python lotsofitems.py`

5. Run app again

`python run.py`

6. Go to: http://localhost:8000

7. Api endpoint: http://localhost:8000/catalog.json



# Resources
----------
1. Full Stack Foundations - Udacity course

2. Authentication and Authorization: OAuth - Udacity course

3. How To Structure Large Flask Applications - https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

4. Bootstrap starter template http://getbootstrap.com/examples/starter-template/ - used for header


# Extras
----------
1. Project Structure
```
/catalog
    /app
        /auth
            __init__.py
            controllers.py
            models.py
        /catalog
            __init__.py
            api.py
            controllers.py
            models.py
        /items
            __init__.py
            controllers.py
            models.py
        /static
            styles.css
        /templates
            /auth
                login.html
            /catalog
                catalog.html
                deletecategory.html
                editcategory.html
                newcategory.html
            /items
                deleteitem.html
                edititem.html
                item.html
                items.html
                newitem.html
            403.html
            404.html
            header.html
            main.html
        __init__.py
    /config
        __init__.py
        client_secret_facebook.json
        client_secret_google.json
    .gitignore
    lotsofitems.py
    README.md
    run.py

```

2. Built a structured application inspired by digitalocean tutorial.

3. Added protection against CSRF requests.