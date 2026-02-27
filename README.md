# The Trade Registry
**The Trade Registry** is a professional financial dashboard designed for
performance analysis and real-time market tracking. Built with a robust
backend and a modern, responsive interface, it allows traders to manage their
portfolios with ease and precision.
---
## Key Features
### 1. Advanced Financial Dashboard
- **Live Price Tracking:**
Real-time ticker prices with automatic updates to reflect current market
conditions.
- **Relational-Live Synthesis:**
Implementation of a hybrid data layer that merges PostgreSQL-stored trades with real-time price volatility
- **Global News Feed:**
A dedicated market news section with relative time logic to keep you informed of the latest trends.
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
- **Streamlined Access Architecture**
An intuitive navigation framework designed to centralize user profile management and technical support modules.
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
- **Docker Secrets:**
Production deployments use Docker Secrets for heightened security. Sensitive data (Django secret key, API keys, database credentials, email credentials) are stored in `.secrets/` directory and mounted as Docker secrets, never exposed in environment variables or docker-compose files.
Secrets are referenced in docker-compose via `secrets:` section and accessed at `/run/secrets/` inside containers.
Example:
```bash
# Create secret files
mkdir -p .secrets/
echo "your-secret-key" > .secrets/django_secret_key.txt
echo "api-key-value" > .secrets/finnhub_api_key.txt

# Secrets are ignored (added to .gitignore and .dockerignore)
# Docker automatically mounts them in containers
```
- **Production Grade:**
Deployed on Oracle Cloud using **Gunicorn** as the WSGI server for reliable
performance.

### Honeypot & Attack Detection
- **Honeypot Endpoint:**
A decoy admin panel at `/admin/` captures unauthorized access attempts.
- **Automatic IP Blacklisting:**
IPs with 3+ failed login attempts are automatically blacklisted and subsequently blocked.
- **Comprehensive Logging:**
All attempts are logged with IP, username, user-agent, and timestamps for security auditing.
- **Admin Dashboard:**
View and manage all blacklisted IPs via Django admin interface.
- **CLI Management:**
Use the `honeypot_blacklist` management command to manage the blacklist:
```bash
# List all blacklisted IPs
python manage.py honeypot_blacklist --list

# Manually add an IP
python manage.py honeypot_blacklist --add 1.2.3.4 --reason "Brute force detected"

# Remove an IP from blacklist
python manage.py honeypot_blacklist --remove 1.2.3.4

# Clear entire blacklist
python manage.py honeypot_blacklist --clear
```

### Admin Panel Security
- **Configurable URL Path:**
The Django admin panel URL is selected by developer via the `ADMIN_URL_PATH` environment variable to prevent discovery at the standard `/admin/` path.
---
### Bulk Ticker Ingestion Utility

The **Trade Registry** features a custom management command designed to seed or update the database with a large volume of tickers efficiently. It leverages Django's `bulk_create` method to minimize database transactions and optimize performance.

#### 1. CSV File Requirements
To ensure the data is mapped correctly to the **PostgreSQL** schema, your source file must be a standard CSV with the following exact headers:

| Column | Description | Example |
| :--- | :--- | :--- |
| `symbol` | The stock ticker symbol (must match Yahoo Finance format) | `AAPL`, `GGAL.BA`, `MELI` |
| `name` | The full legal name of the company | `Apple Inc.`, `MercadoLibre Inc.` |

> **Important:** The file must be saved with **UTF-8** encoding to properly handle special characters in international company names.

#### 2. Usage
You can trigger the ingestion process by passing the file path as a positional argument to the management command.

**Local Environment:**
```bash
python manage.py seed_tickers path/to/your/tickers_list.csv
```
The script will iterate through the CSV, prepare the objects, and perform a bulk insertion. Any existing symbols will be skipped or updated depending on your specific command configuration to prevent integrity errors.
## You can access deployed version following this link
[traderegistry.tech](traderegistry.tech)
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
