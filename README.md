# Item Catalog
--------------

    * This is an application that provides a list of items within a variety of categories as well as
    provide a user registration and authentication system. Registered users will have the ability to post, edit
    and delete their own items.

    * Used technologies: Flask, SQLAlchemy, Facebook, Google+ Authentication


# Prerequisites
---------------
1. Install Vagrant and VirtualBox

2. Clone the `fullstack-nanodegree-vm repository`

3. Clone https://github.com/orangegirl85/udacity_p3_catalog_item repository
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

3. Setup database:

`python database_setup.py`

4. Populate database

`python lotsofitems.py`

5. Run app

`python application.py`



# Resources
----------
1. Full Stack Foundations - Udacity course

2. Authentication and Authorization: OAuth - Udacity course



# Extras
----------
1. Project Structure
```
/catalog
    .gitignore
    Readme.md
    database_setup.py
    lotsofitems.py
    application.py

```

