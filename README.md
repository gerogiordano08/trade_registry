# The Trade Registry
**The Trade Registry** is a professional financial dashboard designed for
performance analysis and real-time market tracking. Built with a robust
backend and a modern, responsive interface, it allows traders to manage their
portfolios with ease and precision.
---
## Key Features
### 1. Advanced Financial Dashboard
- **Dual-Column Layout:**
A high-density information interface featuring a 12-unit grid system for
optimal data visualization.
- **Live Price Tracking:**
Real-time ticker prices with automatic updates to reflect current market
conditions.
- **Global News Feed:**
A dedicated market news section with relative time logic (e.g., *"5 minutes
ago"*) to keep you informed of the latest trends.
---
### 2. Trade Management & Metrics
- **Comprehensive Lifecycle:**
Support for registering, tracking (*Ongoing*), and finalizing (*Ended*)
trades.
- **Dynamic Profit Tracking:**
Real-time calculation of realized and unrealized gains based on live market
data.
- **Interactive UI:**
**"Profit Toggle"** functionality allowing users to switch between absolute
currency values and percentage performance with a single click.
---
### 3. Professional User Interface
- **Modern Navigation:**
A sleek, dark-themed navbar with user profile management and intuitive
dropdowns.
- **Interactive Help Center:**
A dedicated support section featuring Bootstrap accordions for FAQs and
direct technical contact.
- **Responsive Design:**
Fully optimized for mobile and desktop views using Bootstrap 5.
---
## Technical Stack
- **Backend:** Django (Python 3.12)
- **Frontend:** HTML5, CSS3 (Lato Typography), Bootstrap 5
- **Database:** PostgreSQL
- **Caching:** Redis
- **DevOps:** Docker (Multi-stage builds)
---
## RESTful API
Implementation of RESTful API that receives tickers and information from outside services and offers it to an endpoint.
## Redis
Use of redis to cache ticker information, reducing unnecesary API requests.
---
## Background Tasks & Automation
The system relies on **Django Management Commands** and **System Cron** to
maintain data freshness and system health:

- **Price Updates:**
```bash
python manage.py run_get_prices
```
Runs every minute to fetch and update the latest ticker values in the
database.
- **News Scraping:**
```bash
python manage.py run_scraper
```
Executes periodically to populate the market news feed with the latest
relevant articles.
- **Data Cleanup:**
```bash
python manage.py run_news_cleaner
```
Uses `timedelta` logic to automatically purge news articles older than 7
days, optimizing database storage and performance.

---
## Data Model & Architecture
The system is built on a relational schema designed for scalability:
- **Ticker:**
The core entity storing market symbols, names, and the most recent prices
fetched via API.
- **Trade:**
Linked to *Tickers*, storing specific transaction data such as buy/sell
prices, quantity, and dates.
Calculates live metrics by comparing entry prices with current ticker values.
- **News:**
Stores scraped articles associated with specific tickers, including
timestamps and summaries.
---
## Infrastructure & Security
- **Containerization:**
Professional multi-stage Docker builds to ensure a lightweight and secure
production environment.
- **Environment Safety:**
Secret management via environment variables to keep sensitive credentials
(like DB passwords and API keys) out of the codebase.
- **Production Grade:**
Deployed on Oracle Cloud using **Gunicorn** as the WSGI server for reliable
performance.
---
## You can access deployed version following this link
TBD
## Local Setup
The project is fully containerized with Docker to ensure a consistent
environment.
### 1 Clone the repository
```bash
git clone https://github.com/gerogiordano08/trade_registry.git
cd trade_registry
```
### 2 Configure Environment Variables
Copy the example file and fill in your credentials:
```bash
cp .env.example .env
```
### 3 Build and Run with Docker Compose
```bash
docker-compose up --build
```
The application will be available at:
```
http://localhost:8000
```
---
## Author
Developed by **Gerónimo Giordano**
