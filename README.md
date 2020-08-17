# Youtube Upload script

## Install

- Download and install Python3 - https://www.python.org/downloads/
- Install pipenv - `pip3 install --user pipenv`
- Install all dependencies - `pipenv install`
- Get `client_secrets.json` from Google Developer Console - https://developers.google.com/identity/protocols/oauth2/
- Run the script - see below

## How to use

Run the script with a combination of arguments that suits your case best, e.g.:

```
    python upload_video.py --file="example.mpg" \
                       --title="To be done" \
                       --description="another-lesson" \
                       --keywords="schools-for-fools" \
                       --category="schools-for-fools" \
                       --privacyStatus="unlisted"
```
