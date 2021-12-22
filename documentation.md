# Documentation

## Authorization
Authorization is done by supplying your token in the `Authorization` header.  
To generate a token, use the `/generate_token` endpoint.  
To destroy a token, use the `/destroy_token` endpoint.  
To generate an account, use the `/generate_account` endpoint.

## Endpoints

### `/u/<url_id>`
#### Method: `GET`
###### Supply `url_id`: URL's unique identifier
#### returns: A redirect to that URL

---

### `/create_redirect/<desired_id>`
#### Method: `POST` 
###### Supply `url`: URL to redirect to
###### Supply `delete_after`: Positive value = POSIX timestamp when to delete the redirect. `0` value = Never. Negative value = How long after the last visit to delete the redirect.
#### (Optional) Method: `PUT`
###### (Optional) Supply `desired_id`: Desired shortened URL
#### returns: json with the shortened URL

###### Example:
```bash
curl http://127.0.0.1:8080/create_redirect -X POST -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
```json
{
  "shortened_url": "https://127.0.0.1:8080/u/EnqYNGo"
}
```

###### Example 2:
```bash
curl http://127.0.0.1:8080/create_redirect/custom -X POST -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
{
  "shortened_url": "https://127.0.0.1:8080/u/custom"
}
```

---

### `/my_urls`
#### Method: `GET` 
#### returns: json with all the URLs the user has created.

###### Example:
```bash
curl http://127.0.0.1:8080/my_urls --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
[
  {
    "author_id": 1, 
    "creation_timestamp": 1639675025, 
    "delete_after": null, 
    "id": "custom", 
    "last_visit": 1639675025, 
    "premium": 1, 
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
    "visits": 0
  }
]
```

---

### `/generate_token`
#### Method: `POST` 
###### Supply `username`: Username
###### Supply `password`: Password
###### Supply `otp`: Generated TOTP 6-digit code
#### returns: json with a newly generated token.
Example:
```bash
curl http://127.0.0.1:8080/generate_token -X POST -d "username=root&password=1111&otp=350076"
```
```json
{
  "token": "2otsFxH90puYlGvfWL0kqeacTxpvc3QE"
}
```

---

### `/generate_account`
##### Unless you set `allow_registration` in config, you need to supply a token of an administrator/billing account to use this endpoint. This is not required to generate the first account in the database.
#### Method: `POST` 
###### Supply `username`: Username
###### Supply `password`: Password
###### Supply `email`: Email to associate with the account
#### returns: json with a TOTP seed to use for code generation.

###### Example:
```bash
curl http://127.0.0.1:8080/generate_account -X POST -d "username=root&password=1111&email=test"
```
```json
{
  "user_id": 1,
  "totp_seed": "5F62QCOJR3FPQHQXTXLJRTYUGX3QAZCM"
}
```

---

### `/destroy_token`
#### Method: `GET` 
#### returns: json with a success message

###### Example:
```bash
curl http://127.0.0.1:8080/destroy_token --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
{
  "success": "This token has been destroyed!"
}
```

---

### `/update_account_premium`
##### Administrator/Billing system use only
#### Method: `POST` 
###### Supply `user_id`: Account ID
###### Supply `premium`: 1 or 0
#### returns: A success message

###### Example:
```bash
curl http://127.0.0.1:8080/update_account_premium -X POST -d "user_id=5&premium=1" --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
{
  "success": "Account updated"
}
```
