# Migration of ekerobarnvakt.se to Flask  

The original website, [ekerobarnvakt.se](https://www.ekerobarnvakt.se), was built on WordPress.  
I migrated it to Flask and deployed it on [ekerobarnvakt.onrender.com](https://ekerobarnvakt.onrender.com),  
maintaining the same design while enhancing functionality.  

## Current Tasks  
- 🔄 Transfer the domain `ekerobarnvakt.se` to Namecheap and update DNS settings to point to the  
  serverless Flask backend hosted at  
  [ekerobarnvakt.onrender.com](https://ekerobarnvakt.onrender.com)  

## Migration Process  
To recreate the original site, I used **BeautifulSoup** to scrape each HTML page  
and parsed all static file links for adaptation to Flask.  

## Security Enhancements  
To ensure the security of the migrated Flask application, the following measures have been implemented:  
- **CSRF Protection**: Integrated `flask_wtf.csrf.CSRFProtect` to prevent cross-site request forgery (CSRF) attacks.  
- **Input Sanitization**: Used `markupsafe.escape()` to prevent Cross-Site Scripting (XSS) vulnerabilities.  
- **Google reCAPTCHA**: Implemented reCAPTCHA validation to block bot submissions on forms.  
- **Rate Limiting**: Configured `Flask-Limiter` to restrict excessive form submissions and prevent spam or abuse.  
- **Email Security**: Wrapped email-sending logic in a `try-except` block to handle potential issues securely.  
- **Environment Variables**: Ensured sensitive credentials (e.g., `RECAPTCHA_SECRET_KEY`) are securely stored and not exposed in logs.  
The site also benefits from **Cloudflare's security and performance features**, including DDoS protection and traffic optimization.  

