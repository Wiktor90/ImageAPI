# Image Api

## About project
It is simple API to serve images files in common formats: **PNG, JPG, JPEG, GIF**.
Api is able to resize your image (if proper width/height parameter were passed) 
or just store image, in filestorage with its original dimensions. 
Project as well persists images in DB.


## Run Project:

### Note
_Make sure you have **Docker** and **Docker Compose** installed on your system before setup process._
_Make sure you have **git** installed to be able to clone a repo._

1. Clone repository from GitHub:
   - ```git clone https://github.com/Wiktor90/ImageAPI.git```
2. Go to main project directory `cd app`
3. Start containers `docker-compose up`
4. After this you can check `docker-compose ps` that both containers are up and running:
   - `app_db_1`
   - `app_web_1`
4. Then you have to migrate migrations into DB:
   - go into app container `docker exec -it app_web_1 bash`
   - add migrations: `python manage.py migrate`
5. If you want to use Django Admin panel please create superuser:
    - from app container: `python manage.py createsuperuser --email admin@example.com --username admin`
    - go to http://localhost:8000/admin/ in your browser and pass your credentials

## Sending API request
App is browsable, so you can use built in DRF HTML to test API endpoints 
in your browse. You can also use another tool like Postman etc.

Detailed endpoints documentation is accessible in the link below. 
You can check it just after making projest up and running on your localhost:

http://localhost:8000/swagger/

http://localhost:8000/redoc/

## File storage
All file which are sent via POST request are stored in the `media/` directory.
After upload the path to image will be automatically 
generated as `media/images/{filename}`

#### *comments*
Inside the media file in the repo, there is a _placeholder.txt_. It is only because of
that I had to create media folder from GitHub UI (because media dir was 
in my .gitignore and didn't upload).
Sorry for that quick fix but there is no impact on storage.