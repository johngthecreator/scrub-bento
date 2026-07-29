# Spacy CSV Service

BentoML microservice that uses a custom spaCy NER model to extract brand names from offer text in CSV files and filter results against a known list of consumer brands.

## How it works

1. Accepts one or more CSV files via the `/upload` endpoint
2. Concatenates all CSVs into a single DataFrame
3. Runs the spaCy NER model on the `offer` column to detect `BRAND` entities
4. Appends the detected brand to the `normalized_offer` field
5. Filters records to only include offers from a known brand list
6. Returns a JSON array of matching offer metadata

## Expected CSV format

| Column | Description |
|---|---|
| `offer` | Offer text (used for NER brand extraction) |
| `normalized_offer` | Normalized offer text (gets appended with detected brand) |
| `offer_url` | URL for the offer |
| `offer_type` | Type of offer |
| `brand` | Brand name (filtered against known brands) |
| `category` | Product category |
| `expires_date` | Expiration date |
| `source` | Data source |

## Prerequisites

- Python 3.12+
- [BentoML](https://docs.bentoml.com/)

## Getting started

### Install dependencies

```bash
pip install bentoml spacy pandas python-dotenv
```

### Run the service locally

```bash
bentoml serve service:SpacyCSVService
```

The service will be available at `http://localhost:3000`.

### Test with a CSV

```bash
curl -X POST http://localhost:3000/upload \
  -F "csv_files=@your_data.csv"
```

### Build as a container

```bash
bentoml build
bentoml containerize SpacyCSVService:latest
```

## Model

The spaCy model is stored in `./model-best/` and was trained to detect `BRAND` entities. It has an F1 score of ~87.4%.
