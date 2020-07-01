# RBG Intranet

[![Build Status](https://travis-ci.org/redbuttegarden/intranet.svg?branch=master)](https://travis-ci.org/redbuttegarden/intranet)

An intranet site for Red Butte Garden staff and RBG IT documentation.

# Getting Started

To run these containers locally, you'll need to on a Mac or customize the docker-compose.yml files to match your own
environment. Assuming you are on a mac, you can follow this guide to get started:

1. Change into the directory you want to run the code out of and clone the respository:
    
    a. `cd ~`
    
    b. `git clone https://github.com/redbuttegarden/intranet`
    
2. Install dependencies:

    a. [Docker](https://github.com/redbuttegarden/intranet)
    
3. Create the environment files that docker-compose.yml is expecting to find. The `web` container looks for 
`/Users/$USER/intranet_web.env` and the `db` container looks for `/Users/$USER/intranet_db.env`. If you're not on a Mac,
you'd need to change those paths in the docker-compose.yml file to make things work.

    a. An example `/Users/$USER/intranet_web.env` file would look like this:
    
    ```ini
    # These environment variables tell Django how to connect to the database container
    PG_PASSWORD=example_password
    PG_USER=intranet_user
    PG_DB=intranet_db
   
    # This environment variable is used by django to keep the site secure: https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key
    SECRET_KEY=jkfkjsajksdfjklfdjklfds
   
    # This setting defines which settings file Django uses to run the site
    DJANGO_SETTINGS_MODULE=intranet.settings.dev
    ```
   
   b. An example `/Users/$USER/intranet_db.env` file would look like this:
   
   ```ini
    # These environment variables tell the Postgres container how to contruct the database
    # Additional info about that process can be found on the Postgres docker hub page: https://hub.docker.com/_/postgres/
    POSTGRES_PASSWORD=example_password
    POSTGRES_USER=intranet_user
    POSTGRES_DB=intranet_db
    ```
   
   c. Note that the database values between these two files needs to match. So for example, if PG_PASSWORD is set to 
   "myp455word" in `intranet_web.env`, POSTGRES_PASSWORD would also need to be set to "myp455word" in `intranet_db.env`.
   
4. Change into the top-level intranet directory (the one that contains the `docker-compose.yml` files) and start the 
containers. This will download and build the images so it will take a moment the first time you run it:

    a. `cd ~/intranet`
    
    b. `docker compose up`
    
5. At this point, the database will be created for you and django should start up a development server. You should see a
warning in the output that looks something like this:

    ```bash
    web    | You have 109 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, blog, box, contenttypes, custom_user, home, postgres_search, sessions, taggit, wagtailadmin, wagtailcore, wagtaildocs, wagtailembeds, wagtailforms, wagtailimages, wagtailredirects, wagtailsearch, wagtailusers.
    web    | Run 'python manage.py migrate' to apply them.
    ```
   
    This means we need to apply Django migrations to the database.
    
6. To apply django database migrations, we need to connect to the docker container that's running Django. We have a few 
options to do that so I'll describe two common methods.
    
    For both methods, we need to open up a second terminal and change into the intranet directory. Leave the first
    window with `docker-compose up` running.
    
    `cd ~/intranet`
    
    a. For the first method, we can use a single command: `docker-compose run web python /code/manage.py migrate`
    
    b. The second method is slightly more complex but also more flexible. First, use the `docker container ls` command
    to list the running docker containers. Here's some example output showing just the web and db containers:
    ```bash
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
    f054315eedbd        intranet_web        "python /code/manage…"   19 minutes ago      Up 19 minutes       0.0.0.0:8000->8000/tcp   web
    257d47885fce        postgres:11         "docker-entrypoint.s…"   19 minutes ago      Up 19 minutes       5432/tcp                 db
    ```
    We want to connect to the `intranet_web` container so copy it's container ID (in this example it's `f054315eedbd`).
    
    Now we can start an interactive bash shell in that container by specifying the ID as follows:
    
    `docker exec -it f054315eedbd /bin/bash`
    
    At this point, you should now be inside the container. We need to change to the directory with our code so we can
    use the Django management commands. For this project, our code was copied into the `/code` directory of the 
    container. From there we can run the same django command as in the first method above:
    
    `cd /code`
    
    `python manage.py migrate`
    
7. At this point, your basic Django web app should be running and available. Point your browser to `http://0.0.0.0:8000`
and make sure you're not getting any errors. You should see a message like "Welcome to your new Wagtail site!"

8. Now we need to load the intranet pages into the database. We'll need to do this in several steps so it will be 
easiest to do that by connecting to the web container with a bash shell. Follow the steps described in 6.b. until you're
in the `/code` directory of the web container.

    a. From here, we can start a Django shell so we can interact with the Django objects stored in the database. We need to
    delete the Wagtail welcome page before we can load the other pages.
    
    `python manage.py shell`
    
    This will drop you into a python interpreter using our Django environment. Now we can search for and delete the 
    wagtail welcome page.
    
    ```python
    >>> from wagtail.core.models import Page
    >>> welcome_page = Page.objects.get(title="Welcome to your new Wagtail site!")
    >>> welcome_page.delete()
    >>> exit()
    ```
    
    After running `exit()`, you'll be back to your bash shell in the web container. We're now free to load the database
    fixture files that contain our intranet pages. This fixture file is located at 
    `intranet/blog/fixtures/blog_test_fixtures.json`. We load it with another Django management command:
    
    `python manage.py loaddata blog/fixtures/blog_test_fixtures.json`
    
    It should hopefully report back that it successfully installed the fixtures:
    
    `> Installed 117 object(s) from 1 fixture(s)`
   
9. Now if you go back to your browser and refresh the page, things should look a bit more interesting. The intranet
homepage should now be visible and the staff info page at `http://0.0.0.0:8000/staff-info/` should include a few
test posts.

10. We're almost there! The fixture file doesn't include any user objects so we need to make one before we can login. 
Once again, start a bash shell in the web container or use the one you already have if it's still open.

    From the `/code` directory run the following command and follow the prompts to create a django admin user:
    
    `python manage.py createsuperuser`
    
    It should report that the superuser was created successfully
    
11. You're now free to login at `http://0.0.0.0:8000/admin/` using your new superuser's credentials!