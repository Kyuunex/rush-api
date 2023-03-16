# rush-api
rush-api is a URL shortener, made in Flask.  

### Features:
1. Account registration
2. TOTP one time password security, when generating tokens. 
    + Automatically enabled for all accounts
    + In the future, I will add option to enable the requirement for each time the API request is sent.
3. Custom URL generation for premium accounts 
    + Must be set manually for each account in the database.
    + Normally you would use your external billing system to do so.
4. Visitor number tracking
5. URL validation
6. Auto deletion after 30 days of URLs after creation or last visit 
    + **Async task to sift through last visits is not implemented yet!**
7. Domain blacklist

###### A quick example:
```bash
curl http://127.0.0.1:8080/create_redirect -X POST -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
```json
{
  "shortened_url": "https://127.0.0.1:8080/u/EnqYNGo"
}
```


### [Installation Instructions](https://github.com/Kyuunex/rush-api/blob/main/installation.md)
### [Endpoint Documentation](https://github.com/Kyuunex/rush-api/blob/main/documentation.md)
