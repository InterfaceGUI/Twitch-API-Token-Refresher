# Twtich-API-Token-Refresher
This is a Python program based on the Flask architecture for refreshing the Twitch API tokens.

## install & Setup

## How to use

* Go to `/login`endpoint to Get `Access Token` and `Refresh Token`

* Refresh the token using the `/refresh` endpoint:
<details> <summary>Refresh Token</summary>

```javascript
  await fetch('https://0.0.0.0:3000/refresh',{
      method: "POST", headers: {'Origin':'*','content-type': 'application/json'},
      body:JSON.stringify({"refresh_token": 'RefreshToken'})
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    console.log(myJson);
  });

```
</details>

## Example for the streamelement widget
<details> <summary>Validate and refresh the token</summary>

```javascript
window.addEventListener('onWidgetLoad', async function (obj) {
    await TwitchAPI_validate()
});
```

```javascript
const twitchOAuthToken = "{{Twitch_access_token}}"
const TwitchRefreshToken = "{{Twitch_refresh_token}}"

async function TwitchAPI_validate(){
    
    //Test the access token. If the token expires, twitch will return 401.
    const response = await fetch('https://id.twitch.tv/oauth2/validate',{
        method: "GET",
        headers: {
            Authorization: `Bearer ${twitchOAuthToken}`
        }
    })
    
    if ( response.status == 401){
        console.log('invalid access token')
        console.log('Getting new token...')
        
        const newtoken = await fetch('https://0.0.0.0:3000/refresh',{
            method: "POST", headers: {'Origin':'*','content-type': 'application/json'},
            body:JSON.stringify({"refresh_token":TwitchRefreshToken})
        })

        if ( newtoken.status != 200){return false}
        
      	let respData = await newtoken.json();
        console.log(respData);
        
        //Update widget Field
        SE_API.setField('Twitch_access_token', respData['access_token']);
    }
    return true
}
```
</details>

<details> <summary>Use the twitch api</summary>

```javascript
await fetch('https://api.twitch.tv/helix/users',{
    method: "GET",
    headers: {
        Authorization: `Bearer ${twitchOAuthToken}`,
        'Client-Id': '---Client id here---'
    }
})
.then((response) => {
    return response.json()
})
.catch((error) => {
    console.log(`Error: ${error}`);
})
```
</details>

<details> <summary>fields.json</summary>

```json
{
    "Twitch_access_token": {
        "type": "text",
        "label": "Twitch Access Token",
        "value": "",
        "group": "Twitch Settings"
    },
    "Twitch_refresh_token": {
        "type": "text",
        "label": "Twitch Refresh Token",
        "value": "",
        "group": "Twitch Settings"
    }
}
```
</details>
