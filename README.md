#### TODO: make nicer

## Installation guide:
- clone repo
- set up venv
- install `requirements.txt`
- run `python3 manage.py runserver`
- run `python3 manage.py runserver`

## Possible problems:
- check perms for the forlder specified in `settings.py` as MEDIA_ROOT
- if on windows 🤮, change this folder

## Docs are your friend:
- most everything is [Django Admin](https://docs.djangoproject.com/en/5.1/ref/contrib/admin/)
- the missing "volume equalisation" should be done as a [Command](https://docs.djangoproject.com/en/5.1/howto/custom-management-commands/) and triggered with some button (like the one in AudioSetsAdmin class)

## Notes:
- this is pretty ugly and some good practices were not followed but everything works and most of it is easily fixable, gl
