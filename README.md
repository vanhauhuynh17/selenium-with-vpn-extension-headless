# Pricing worker: A powerful worker to scrape stock data

## 1. What is pricing-worker?
- pricing-worker is a stock crawler written by Python.
- It is designed with the hope to crawl main information including:
    + pricing information of stocks
    + company information connected with each stock or ETF - a type of index fund
    + statistical idicators
    + stock news

## 2. Quick start
Note: there is not too much difference between `python` and `python3` in our repo because we can use both to successfully run our app.

### Folder structure:
This repo is followed by a structure: https://github.com/yngvem/python-project-structure

### 2.1. Requirements
- [Python](https://www.python.org/downloads/) (required)
- Editor: [Visual Studio](https://visualstudio.microsoft.com/) (optional)
    + Extensions
        + Python (ID: ms-python.python)
        + Pylance (ID: ms-python.vscode-pylance)


### 2.2. How to run the app
Step 1. Install virtual env ([Ref](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/))

    python3 -m pip install --user virtualenv

Step 2. Create a virtual env and activate it ([Ref](https://docs.python.org/3/library/venv.html))

    python3 -m venv env
    source env/bin/activate

Step 3. Install python packages from the package requirement file

    pip install -r requirements.txt

Step 4. Export the google credential (used for GCS namely firebase, firestore)

    export GOOGLE_APPLICATION_CREDENTIALS=resources/credential.dev.json

Step 5. Run the main app

    python3 main.py

### 2.3. How to add new stock codes
It requires perseverance, grit and patience to add new stock codes. Keep calm and let's do it

Step 1. Add new stock codes in `top_stock.csv`. This file will include all stocks supported in Anfin app

Step 2. Update new stock information such as **subsector, industrialName** into `resources/crawled_company.csv` - data are crawled from [SSI page](https://iboard.ssi.com.vn/bang-gia/vn30). If not, `crawl_indicators` function in `stock_indicator_crawler.py` does not work properly. How to update `resources/crawled_company.csv`? Add function `save_crawled_company_csv` at the bottom of `run_company_info_crawler`. It looks look:

    def run_company_info_crawler():
    df = load_profiles_from_ssi()
    df = detect_domains(df)
    df = normalize_company_profiles(df)
    df = detect_colors(df)
    save_crawled_company_csv(df)

Step 3: (Use [color-detector](https://github.com/anfin21/color-detector) repo) Add relevant stock codes under `stock_logo` folder - logo images will be resized and reshaped first such as adding a circle around the image, then detect background colors and colors of these stock image for Mobile app.

### 2.4. Build the docker container (use for testing when you wanna deploy to the google cloud)
Step 1: Build an image

    docker build -t pricing-worker .

Step 2: Run the container from this image in the background

    docker run -d --name=pricing-worker pricing-worker

Step 3: View logs of container

    docker logs pricing-worker


## 3.1. Documents
- Using PlantUML extension in Visual studio
- Visual diagram extension resource
    - Homepage: https://marketplace.visualstudio.com/items?itemName=jebbs.plantuml
    - Sequence diagram page: https://plantuml.com/sequence-diagram
- Installing and using PlantUML
    ```
        brew install --cask temurin
        brew install graphviz
    ```
    In Mac, click to the file and press option + D

## 3. Sequence diagrams
- Using [Mermaid JS](https://mermaid-js.github.io/)

- Extensions:
    + Markdown Preview Mermaid Support (ID: bierner.markdown-mermaid)
    + Mermaid Markdown Syntax Highlighting (ID: bpruitt-goddard.mermaid-markdown-syntax-highlighting)

- Diagrams

    + Crawling realtime pricing
    ```mermaid
        sequenceDiagram
        pricing-worker ->> ssi-web : get pricing data for stock
        ssi-web -->> pricing-worker: return `stockRealimes` data
        pricing-worker ->> firestore: add pricing data to `live_stock_prices document`
        firestore -->> pricing-worker: return result

        pricing-worker ->> ssi-web : get detailed data of index such as VNINDEX for stock
        ssi-web -->> pricing-worker: return `IndexDetail` data
        pricing-worker ->> firestore: add detailed data of index to `live_stock_prices document`
        firestore -->> pricing-worker: return result
    ```

    + Crawling company's information
    ```mermaid
        sequenceDiagram
        pricing-worker ->> ssi-web: scrape company's information for each stock code
        ssi-web -->> pricing-worker: return `companyProfile` data

        pricing-worker ->> ssi-web: get share holders information for each company
        ssi-web --> pricing-worker: return `shareholders` data

        pricing-worker ->> pricing-worker: `calculate share_holders` and `compay_share_holders` data
        pricing-worker ->> pricing-worker: detect the company website
        pricing-worker ->> pricing-worker: detect colors and background colors of company's logos, resharp company's logos

        pricing-worker ->> google-storage: update company's logo
        google-storage -->> pricing-worker: return result

        pricing-worker ->> firestore: save detailed data of index to `companies document`
        firestore -->> pricing-worker: return result
    ```

    + Create company's groups
    ```mermaid
        sequenceDiagram
        pricing-worker ->> google-storage: update the local group icon file
        google-storage --> pricing-worker: return result

        pricing-worker ->> pricing-worker: convert the thumnail/background image from png to jpg
        pricing-worker ->> google-storage: update the local thumnail icon file
        google-storage --> pricing-worker: return result

        pricing-worker ->> firestore: update the group data of index to `company_groups document`
        firestore -->> pricing-worker: return result
    ```

    + Update company's groups
    ```mermaid
        sequenceDiagram
        pricing-worker ->> file-storage: load all stock information from `crawled_stocks.csv`
        file-storage --> pricing-worker: return all stock information

        pricing-worker ->> ssi-web: get stock list belonging to vn30
        ssi-web -->> pricing-worker: return corresponding data
        pricing-worker ->> ssi-web: get current prices of stock list
        ssi-web -->> pricing-worker: return corresponding data
        pricing-worker ->> ssi-web: get super sectors of stock list
        ssi-web -->> pricing-worker: return corresponding data
        pricing-worker ->> ssi-web: get stock list of etf
        ssi-web -->> pricing-worker: return corresponding data
        pricing-worker ->> pricing-worker: calculate new groups `top_market_cap`, `top_revenue_growth`


        pricing-worker ->> pricing-worker: match / classify stock groups for each stock
        pricing-worker ->> pricing-worker: calculate `sharesoutstanding` value for each stock

        pricing-worker ->> firestore: update group list for each stock to `companies document`
        firestore -->> pricing-worker: return result
    ```

    + Crawling interval prices
    ```mermaid
        sequenceDiagram
        pricing-worker ->> ssi-web: get interval prices of stocks at interval (5 seconds, minute and 1 day)
        ssi-web -->> pricing-worker: return corresponding data
        pricing-worker ->> mysql: add all prices data at inteval
        mysql -->> pricing-worker: return corresponding data
        pricing-worker ->> firestore: add all prices data at interval
        mysql -->> pricing-worker: return corresponding data
    ```

    + Crawling and calculating the statistical indicator
    ```mermaid
        sequenceDiagram
        pricing-worker ->> file-storage: load `all` stock information from `crawled_company.csv`
        file-storage --> pricing-worker: return all stock information

        pricing-worker ->> pricing-worker: self calculate statistical indicators such as revenue, revenue_growth, profit_margin
        pricing-worker ->> pricing-worker: calculate ranks of some statistical indicators

        pricing-worker ->> file-storage: save all data to `crawled_stocks.csv`
        file-storage -->> pricing-worker: return result

        pricing-worker ->> file-storage: get all data from `crawled_stocks.csv`
        file-storage -->> pricing-worker: return data

        pricing-worker ->> firestore: only update statistical indicators
        firestore -->> pricing-worker: return result
    ```

## 4. Folder structure
    .
    ├── common/          # Tools and utilities
    ├── env/             # Virtual env folder
    ├── stock_logo/      # Stock logo images (Use color-detector repo instead)
    └── resources/       # Resource files such as csv files, credential files, config files and images
    ├── pricing/         # Place for storing price API from SSI
    ├── pubsub/          # sending notification by google pub/sub
    ├── stock_groups/    # containing icon and background images for company groups
    └── README.md

## 5. Resource description
- you are maybe confused about many csv files, let's get more clarify them:
    + `crawled_company.csv`: csv file are crawled from ssi webpage (we crawl data and then save file). (function: `save_crawled_company_csv`)
    + `crawled_stocks.csv`: stock data taken from `crawled_company.csv`, then calculate statistical indicators and save.
    + `top_stock.csv`: list of stock code which Anfin supports for viewing, purchasing
    + `anfin_stock.csv`: list of stock code which are used for news crawling