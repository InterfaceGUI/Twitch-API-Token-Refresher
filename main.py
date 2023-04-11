from flask import Flask
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from flask import session, redirect, request, url_for, jsonify
import requests
import json
import os

app = Flask(__name__)
CORS(app)
app.secret_key = "development"
oauth = OAuth()

host = os.environ.get('host') if os.environ.get('host') else '0.0.0.0'
port = os.environ.get('port') if os.environ.get('port') else '3000'

Twitch_ClientID = os.environ.get('ClientID')
Twitch_ClientSecret = os.environ.get('ClientSecret')
Twitch_Scope = os.environ.get('scope').split(',') if os.environ.get('scope') else ''
    
#Put your scope in request_token_params
#Twitch client id to consumer_key
#twitch client secret to consumer_secret
twitch = oauth.remote_app('twitch',
                          base_url='https://api.twitch.tv/kraken/',
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://api.twitch.tv/kraken/oauth2/token',
                          authorize_url='https://api.twitch.tv/kraken/oauth2/authorize',
                          consumer_key=Twitch_ClientID, # get at: https://www.twitch.tv/kraken/oauth2/clients/new
                          consumer_secret=Twitch_ClientSecret,
                          request_token_params={'scope': Twitch_Scope}
                          )
                          
                          
@app.route('/login')
def login():
    return twitch.authorize(callback=url_for('authorized', _external=True))

@app.route('/revok', methods=['POST'])
def revok():
    req = request.values
    revokData = {
                    "token":req['access_token'],
                    "client_id":twitch.consumer_key
                }
    resp = requests.post('https://id.twitch.tv/oauth2/revoke', data=revokData)
    return 'ok'

@app.route('/refresh', methods=['POST'])
def refreshToken():
    req = request.get_json()
    print(req)
    refreshdata = {
                    "refresh_token":req['refresh_token'],
                    "grant_type":"refresh_token",
                    "client_id":twitch.consumer_key,
                    "client_secret":twitch.consumer_secret
                  }
    resp = requests.post('https://id.twitch.tv/oauth2/token', data=refreshdata)
    if not resp.ok:
        return 'Access denied'

    print(resp.json())
    return resp.json()


@app.route('/twitch-auth-callback')
def authorized():
    resp = twitch.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    print('Twitch resp:',resp)
    headers = {
        'Authorization': f'Bearer {resp["access_token"]}',
        'Client-Id': twitch.consumer_key
    }
    me = requests.get('https://api.twitch.tv/helix/users',headers=headers).json()['data'][0]
    
    print('User status:', me)

    Html = f'<form method="POST" action="/revok">access_token : <input type="text" class="form-control" name="access_token" value="{resp["access_token"]}"><br><br> refresh_token :<input type="text" value="{resp["refresh_token"]}"><button type="submit" >Revoke</button></form>'
    return Html

if __name__ == '__main__':
    app.run(host=host, debug=True, port=port, ssl_context=('./ssl/server.crt', './ssl/server.key'))