# Documentation

## Authorization
Authorization is done by supplying your token in the `Authorization` header.  
To generate a token, use the `/generate_token` endpoint.  
To destroy a token, use the `/destroy_token` endpoint.  
To generate an account, use the `/generate_account` endpoint.

## Endpoints

### Redirect a URL
#### `GET` `/u/<url_id>`
- `url_id`: URL's unique identifier
- returns: A redirect to that URL

---

### Create a shortened URL
#### `POST`/`PUT` `/create_redirect/<desired_id>`
- `url`: URL to redirect to
- `delete_after`: Configure automatic deletion (Optional) 
  - Positive value = POSIX timestamp when to delete the redirect. 
  - `0` value = Never. 
  - Negative value = How many seconds after the last visit to delete the redirect.
- `desired_id`: Desired shortened URL
- returns: json with the shortened URL

```bash
curl http://127.0.0.1:8080/create_redirect -X POST -d "url=https://youtu.be/FTQbiNvZqaY"
```
```json
{
  "shortened_url": "https://127.0.0.1:8080/u/8IgjK1T"
}
```

```bash
curl http://127.0.0.1:8080/create_redirect/custom -X POST -d "url=https://youtu.be/FTQbiNvZqaY" --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
{
  "shortened_url": "https://127.0.0.1:8080/u/custom"
}
```

---

### Get a list of your previously created URLs
#### `GET` `/my_urls`
- returns: json with all the URLs the user has created.

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
    "url": "https://youtu.be/FTQbiNvZqaY", 
    "visits": 0
  }
]
```

---

### Generate an authorization token
#### `POST` `/generate_token`
- `username`: Username
- `password`: Password
- `otp`: Generated TOTP 6-digit code
- returns: json with a newly generated token.

```bash
curl http://127.0.0.1:8080/generate_token -X POST -d "username=root&password=1111&otp=350076"
```
```json
{
  "token": "2otsFxH90puYlGvfWL0kqeacTxpvc3QE"
}
```

---

### Create an account
#### `POST` `/generate_account`
Unless you set `allow_registration` in config, you need to supply a token of an administrator/billing account to use this endpoint. 
This is not required to generate the first account in the database.
- `username`: Username
- `password`: Password
- `email`: Email to associate with the account
- returns: json with a TOTP seed to use for code generation.

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

### Force expire an authorization token
#### `GET` `/destroy_token`
- returns: json with a success message

```bash
curl http://127.0.0.1:8080/destroy_token --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
{
  "success": "This token has been destroyed!"
}
```

---

### Update account premium status
#### `POST` `/update_account_premium`
Administrator/Billing system use only
- `user_id`: Account ID
- `premium`: 1 or 0
- returns: A success message

```bash
curl http://127.0.0.1:8080/update_account_premium -X POST -d "user_id=5&premium=1" --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
{
  "success": "Account updated"
}
```
