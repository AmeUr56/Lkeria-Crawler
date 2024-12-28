# Lkeria Crawler
This project is a Scrapy-based web crawler designed to scrape data from the Lkeria website. It includes three separate spiders to target different sections of the site:
- **Announces**: Location (Rentals) and Vente (Sales).
- **Experts**: Architects, Notaries, Geometers, and Real Estate Developers.
- **Agencies**: Real Estate Agencies and Property Administrators.

## Lkeria Website
is a  Algerian platform dedicated to real estate and professional services. It provides resources for property listings (rentals and sales), expert services (architects, notaries, geometers, and real estate developers), and agencies (real estate agencies and property administrators).


## Features

### Announces Spider:
Scrapes details of rental and sale listings, including:

- Title
- URL
- Agence
- Property type
- Area
- Pieces
- Reference
- Phone Numbers
- Price
- Location
- Description

### Experts Spider:
Scrapes information about experts in various fields, including:

- Type of expert (Architect, Notary, Geometer, etc.)
- Name and title
- Wilaya (region)
- Contact information (phone, mobile, address)
- Description
- Profile URL

### Agencies Spider:
Scrapes real estate agencies and property administrators, capturing:

- Agency name
- Type of service
- Contact information (phone, email, address)
- Description
- Profile URL
- Registre
- Aggrement
- Website

## Installation
- Clone the repository:

```
git clone https://github.com/YourUsername/Lkeria-Crawler.git
```
- Navigate to the project directory:
```
cd Lkeria-Crawler
```
- Install the required dependencies:
```
pip install -r requirements.txt
```

- Running the Crawlers

Run the desired Scrapy spider for the specific section:

- Announces Spider:
```
scrapy crawl announces_spider -o announces.json
```
- Experts Spider:
```
scrapy crawl experts_spiders -o experts.json
```
- Agencies Spider:
```
scrapy crawl agencies_spider -o agencies.json
```

- Output:
- 
The data will be saved in the format specified by the -o flag (e.g., JSON, CSV, etc.).

Note:
This spider and similar projects are intended for learning purposes only. Please ensure you comply with the website’s terms of service and robots.txt when using the spider.

License
This project is licensed under the MIT License.