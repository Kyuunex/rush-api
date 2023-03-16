# rush-api
rush-api is a URL shortener, made in Flask.  

### Features:
1. Account registration
2. TOTP one time password security, when generating tokens. 
    + Automatically enabled for all accounts for absolute security.
    + In the future, I will add option to enable the requirement for each time the API request is sent.
3. Custom URL generation for premium accounts 
    + Must be set manually for each account in the database.
    + Your external billing system should call `/update_account_premium` endpoint to do so.
4. Visitor number tracking
5. URL validation
6. Auto deletion after 30 days of URLs after creation or last visit 
    + **Async task to clean up old URLs is not implemented yet!**
7. Domain blacklist

### A quick example:
###### Create a redirect url:
```bash
curl http://127.0.0.1:8080/create_redirect -X POST -d "url=https://youtu.be/FTQbiNvZqaY"
```
```json
{"shortened_url": "http://127.0.0.1:8080/u/8IgjK1T"}
```
###### List your created redirect urls:
```bash
curl http://127.0.0.1:8080/my_urls --header "Authorization: tF9y4lcvaY80FkqxIsL1fE7cnCslfeVe"
```
```json
[
  {
    "author_id": 1, 
    "creation_timestamp": 1639675025, 
    "delete_after": null, 
    "id": "your-custom-id", 
    "last_visit": 1639675025, 
    "premium": 1, 
    "url": "https://youtu.be/FTQbiNvZqaY", 
    "visits": 0
  }
]
```

### [Installation Instructions](https://github.com/Kyuunex/rush-api/blob/main/installation.md)
### [Endpoint Documentation](https://github.com/Kyuunex/rush-api/blob/main/documentation.md)
