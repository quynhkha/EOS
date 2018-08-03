# EOS - Image processing on Web 
This project allows user to process rock crystal image on web. The main technology used are OpenCV, Django and JQuery.

## Getting Started

These instructions will guide you to launch the EOS web app using docker-compose. This will skip the messy setup for development stage. However, you should modify accordingly to launch the web app for production.

### Prerequisites
```
docker (newest version preferred)
docker-compose (newest version preferred)
```

### Build and run the docker image for the web app.

Go to /EOS/EOSWebApp

Run this command in your terminal:

``` docker-compose run web python manage.py migrate --noinput ```

After docker-compose download dependencies and build the image, run this command to launch the web app:

``` docker-compose up -d --build ```

If you encounter "userland proxy Error" (Especially for Windows user), you can try restart Docker and run the above command again.

Now you can launch the web app by navigating to ``` http://localhost:8000 ```

### Code development

After any modification in the code, you should run the migration command once again.

### Notice

For production, you should modify the file /EOS/EOSWebApp/EOSWebApp/settings.py to only allow certain IP ranges.
For more information, look up for docker and docker-compose documentation.
