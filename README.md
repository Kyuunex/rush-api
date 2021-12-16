# rush-api
rush-api is a URL shortener, made in Flask.  

### Features:
1. Account registration
2. TOTP one time password security, when generating tokens. 
    + Automatically enabled for all accounts
3. Custom URL generation for premium accounts 
    + Must be set manually for each account in the database.
    + Normally you would use your external billing system to do so.
4. Visitor number tracking
5. URL validation
6. Auto deletion after 30 days of URLs after creation or last visit 
    + **feature not fully implemented!**

### [Installation Instructions](https://github.com/Kyuunex/rush-api/blob/main/installation.md)
### [Endpoint Documentation](https://github.com/Kyuunex/rush-api/blob/main/documentation.md)
