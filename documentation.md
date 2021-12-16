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
#### (Optional) Method: `PUT`
###### (Optional) Supply `desired_id`: Desired shortened URL
#### returns: json with the shortened URL

---

### `/my_urls`
#### Method: `GET` 
#### returns: json with all the URLs the user has created.

---

### `/generate_token`
#### Method: `POST` 
###### Supply `username`: Username
###### Supply `password`: Password
###### Supply `otp`: Generated TOTP 6-digit code
#### returns: json with a newly generated token.

---

### `/generate_account`
#### Method: `POST` 
###### Supply `username`: Username
###### Supply `password`: Password
###### Supply `email`: Email to associate with the account
#### returns: json with a newly generated token and a TOTP seed to use for future code generation.

---

### `/destroy_token`
#### Method: `GET` 
#### returns: json with a success message
