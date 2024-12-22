# Custom eWeLink REST API Manager for Create Webhooks Scenes
## Using DEV standard licence and official eWeLink API

### Steps to run:
0. Create an account on https://dev.ewelink.cc/ and request for a standard free licence, then create an API (to gain appid & app secret). On `Redirect URL` field paste `http://localhost:8000/ewelink/1/use_code`.
1. Install python 3.10
2. Install `django` & `django rest framework`:
```bash
pip install django djangorestframework
```
3. Go to `REST_API` directory:
```bash
cd .\REST_API\
```
4. Create & run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create superuser:
```bash
python manage.py createsuperuser
```
6. Run server locally:
```bash
python manage.py runserver
```
7. Go to `localhost:8000/admin/` . Login using your superuser account. Create a new `Configuration` object using created API on step 0.
8. Go to `localhost:8000/ewelink/id_of_your_configuration_object/authorize_app/` & login using your main eWeLink account (for eWeLink mobile app) to get an accessToken.
9. Go to `https://web.ewelink.cc/` & login using your main eWeLink account (for eWeLink mobile app). Identify your devices that you want to use in your scenes.
10. Go to `localhost:8000/admin/` . Login using your superuser account. Add your `Device` objects using id from `https://web.ewelink.cc/`.
11. Create a new scene using json payload (**advanced**: `localhost:8000/ewelink/id_of_your_configuration_object/scene_create/`) or html form (**recommended**: `localhost:8000/ewelink/id_of_your_configuration_object/scene_create_by_form/`).
12. Have fun using webhooks, for example using StreamDeck ;)

### Endpoints in app:
- `<int:pk>/authorize_app/` : Get accessToken & refreshToken
    * `<int:pk>` - id of your `Configuration` object
- `<int:pk>/use_code/` : Automated endpoint to gather access code from eWeLink API to get accessToken
- `<int:pk>/refresh_tokens/` : Refresh tokens :)
- `<int:pk>/device/` : Shows list of devices & statuses (JSON view)
- `<int:pk>/device/<str:name>/` : Show detail of device & status (JSON view)
    * `<str:name>` : Device name
- `<int:pk>/scene/` : Show list of scenes (JSON view)
- `<int:pk>/scene/<str:name>/` : Show detail of scene (JSON view)
    * `<str:name>` : Scene name
- `<int:pk>/scene_create/` : Create scene using JSON payload (**advanced**)
- `<int:pk>/scene_create_by_form/` : Create scene using HTML form (**recommended**)
- `<int:pk>/scene/<str:name>/edit/` : Edit scene using HTML form
- `<int:pk>/scene/<str:name>/activate` : Activate scene (webhook for StreamDeck or other useful things :)

### Usefull links:
- https://coolkit-technologies.github.io/eWeLink-API/#/en/APICenterV2
- https://coolkit-technologies.github.io/eWeLink-API/#/en/OAuth2.0?id=code-examples-and-test-cases
- https://dev.ewelink.cc/#/console
- https://web.ewelink.cc/#/ota

### Created by:
- Adrian Albrecht ( me :) )