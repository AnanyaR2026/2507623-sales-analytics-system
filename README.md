# 2507623-sales-analytics-system
# Sales Analytics System (Python)

A modular **Sales Analytics System** built using core **Python fundamentals** to process, analyze, and enrich sales transaction data.  
The project demonstrates structured programming, data analysis, API integration, robust error handling, and professional report generation.

---

##  Project Overview

This system ingests raw sales transaction data, performs multiple layers of analysis, enriches data using an external API, and produces a comprehensive, formatted sales report.

The project is designed to reflect **real-world analytics workflows** while adhering strictly to academic assignment requirements.

---

## Key Features

- Modular and scalable Python architecture
- Clean separation of concerns (data handling, processing, API, reporting)
- Sales performance analysis across regions, products, customers, and dates
- External API integration using DummyJSON
- Graceful error handling and user-friendly console output
- Automated generation of enriched data files and analytics reports

---

## Project Structure
2507623-sales-analytics-system/
│
├── main.py
├── sales_data.py
├── report_generator.py
├── README.md
│
├── utils/
│ ├── file_handler.py
│ ├── parser.py
│ ├── validator.py
│ ├── data_processor.py
│ ├── data_based_analysis.py
│ ├── api_client.py
│ └── api_handler.py
│
├── data/
│ └── enriched_sales_data.txt
│
├── output/
│ └── sales_report.txt



---

## 🧩 Functional Breakdown

### PART 1: Data Handling & Validation

**Objective:** Read, parse, clean, and validate raw sales transaction data.

**Modules:**
- `file_handler.py` – File input/output operations
- `parser.py` – Data parsing and cleaning
- `validator.py` – Transaction validation logic

---

### PART 2: Data Processing & Analytics

#### Task 2.1 – Sales Summary  
**File:** `utils/data_processor.py`

- Total revenue calculation
- Region-wise sales analysis
- Top-selling products
- Customer purchase behavior analysis

#### Task 2.2 – Date-Based Analysis  
**File:** `utils/data_based_analysis.py`

- Daily sales trends
- Peak sales day identification

#### Task 2.3 – Product Performance  
**File:** `utils/data_based_analysis.py`

- Identification of low-performing products based on thresholds

---

### PART 3: API Integration

**API Used:** DummyJSON  
**Base URL:**  
https://dummyjson.com/products


**Purpose:**  
Enhance internal sales data with external product attributes such as category, brand, and rating.

**Modules:**
- `api_client.py` – Fetches product data from the API
- `api_handler.py` – Maps and enriches transactions with API data

**Features:**
- Error-tolerant API calls
- Safe fallback for unmatched products
- Enrichment success tracking

---

## 📄 Report Generation

**File:** `report_generator.py`

Generates a structured text report containing:

- Overall sales summary
- Region-wise performance metrics
- Top products and customers
- Daily sales trends
- Product performance insights
- API enrichment statistics







