# Welcome to my Newsletter

The application is specifically built for people who want to start a newsletter where they need a UI to create the content and send it to all of their subscribers

### To Use this application

1. Clone you respository or download the zip file

2. create a virtual env and activate it

    - helps you use your django project in a seperate environment

3. go to the root folder -> pip install -r requirements.txt

    - This will install all the dependencies in your new environment

4. Run the below to migrate your database changes

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Finally, `python manage.py runserver` to run the application and open the browser at http://localhost:8000/

6. For the custom admin panel, go to http://localhost:8000/me/

    - Here you can do all sort of admin tasks, but you should have created a super user in django built-in admin panel to login to my custom admin panel

7. For the env, set up 3 variables which are
    ```
    EMAIL_PORT
    EMAIL_HOST_USER
    EMAIL_HOST_PASSWORD
    ```
    - EMAIL_HOST_PASSWORD - is something you can obtain in your google account security
    - EMAIL_HOST_USER - is the sender's email
    - EMAIL_PORT - is the SMTP port (ex: 25,587,465) that email servers use for secure email submission
