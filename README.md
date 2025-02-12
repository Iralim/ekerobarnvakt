# Migration of Ekerobarnvakt.se to Flask  

The original website, [ekerobarnvakt.se](https://www.ekerobarnvakt.se), was built on WordPress.  
I migrated it to Flask and deployed it on [ekerobarnvakt.onrender.com](https://ekerobarnvakt.onrender.com),  
maintaining the same design while enhancing functionality.  

## Current Tasks  
- ✅ Set up an email **info@ekerobarnvakt.se** for the domain  
- 🔒 Configure security settings  
- 🔄 Transfer the domain to Namecheap and update DNS settings to use `ekerobarnvakt.se`  
  while hosting requests on the serverless Flask backend at  
  [ekerobarnvakt.onrender.com](https://ekerobarnvakt.onrender.com)  

## Migration Process  
To recreate the original site, I used **BeautifulSoup** to scrape each HTML page  
and parsed all static file links for adaptation to Flask.  
