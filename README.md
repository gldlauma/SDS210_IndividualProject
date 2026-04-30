# SDS210 Individual Project: ZüriWieNeu Urban Issue Analysis

## Project Overview

This project analyses reported urban infrastructure issues in the city of Zurich using open data from the **ZüriWieNeu** reporting platform.

ZüriWieNeu allows residents to report problems in public space, such as waste at collection points, damaged streets, broken lighting, graffiti, or issues with green spaces. The dataset contains individual reports with timestamps, categories, coordinates, and descriptive text.

The goal of this project is to build a clear and reproducible data workflow that reads, cleans, structures, analyses, and visualizes the ZüriWieNeu data. The analysis combines temporal, categorical, and spatial perspectives.

The project first works with a downloaded CSV file. The code is structured so that it could later be extended to use the ZüriWieNeu Open311 API.

---

## Research Questions

The project is organized around four research questions.

### Research Question 1

**How has the number of ZüriWieNeu reports changed over time?**

This question analyses yearly and monthly reporting trends between 2013 and 2025.

### Research Question 2

**How has the composition of ZüriWieNeu report categories changed over time?**

This question examines how different report categories developed over time, using both absolute counts and relative category shares.

### Research Question 3

**Which Zurich Quartiere had the highest number of ZüriWieNeu reports in 2025?**

This question introduces spatial analysis by assigning individual report points to Zurich Quartier polygons and mapping report counts by neighbourhood.

### Research Question 4

**Are certain types of ZüriWieNeu reports concentrated in particular Zurich Quartiere in 2025?**

This question analyses whether specific report categories, especially **Abfall/Sammelstelle**, are spatially concentrated in certain Quartiere.

---

## Project Structure

SDS210_IndividualProject/

- data/
  - raw/
    - ZüriWieNeu raw CSV file
    - StatQuartiere_ZH/
      - Zurich Quartiere shapefile files
  - processed/
    - zueriwieneu_cleaned.csv

- notebooks/
  - 00_dataexploration.ipynb
  - 01_R1.ipynb
  - 02_R2.ipynb
  - 03_R3.ipynb
  - 04_R4.ipynb

- output/
  - figures/
    - saved visualizations

- src/
  - __init__.py
  - loading.py
  - cleaning.py
  - analysis.py
  - spatial.py

- requirements.txt
- README.md

---

## Data

### ZüriWieNeu Report Data

The main dataset contains reports submitted through the ZüriWieNeu platform.

Important columns include:

- `service_request_id`: unique report identifier
- `requested_datetime`: date and time when the report was submitted
- `updated_datetime`: date and time when the report was last updated
- `e` and `n`: Swiss coordinate values in EPSG:2056
- `service_name`: report category
- `status`: report status
- `title`, `detail`, and `description`: textual report information
- `interface_used`: information about how the report was submitted

The analysis focuses mainly on reports from **2013 to 2025**. Reports from 2026 are present in the dataset but are excluded from full-year comparisons because 2026 is not yet a complete calendar year.

### Spatial Data

The spatial analysis uses Zurich Quartier boundaries from a shapefile. These polygons are used to assign each report point to a Quartier using a spatial join.

The spatial data uses the coordinate reference system:

**EPSG:2056 — CH1903+ / LV95**

This matches the coordinate columns `e` and `n` in the ZüriWieNeu dataset.

---

## Methods

The project follows a reusable data workflow.

### 1. Loading

The raw CSV file is loaded using a reusable function from `src/loading.py`.

### 2. Cleaning

The cleaning workflow is implemented in `src/cleaning.py`.

The main cleaning steps are:

1. Convert date columns to datetime format.
2. Remove duplicate reports based on `service_request_id`.
3. Add time-based columns:
   - `year`
   - `month`
   - `year_month`

These steps are combined in one reusable function:

`df_clean = clean_reports(df_raw)`

This ensures that the same cleaning logic is applied consistently across all notebooks.

### 3. Temporal Analysis

Temporal analysis is used for Research Questions 1 and 2.

The project calculates:

- yearly report counts
- monthly report counts
- report counts by year and category
- category shares by year

### 4. Spatial Analysis

Spatial analysis is used for Research Questions 3 and 4.

The report data is converted into a GeoDataFrame using the coordinate columns `e` and `n`. Each report is then spatially joined to a Zurich Quartier polygon.

This allows the project to calculate:

- total reports per Quartier
- report categories per Quartier
- dominant categories by Quartier
- category shares within each Quartier

---

## Main Findings

### Reporting Volume Over Time

The number of ZüriWieNeu reports increased strongly between 2013 and 2025. After a decline between 2013 and 2015, reporting activity began to rise again from 2016 onward. The increase became especially strong after 2018.

The highest full-year report count occurred in 2025, with **11,588 reports**.

### Category Development Over Time

The most common report category across the full period was **Abfall/Sammelstelle**.

Other important categories included:

- `Signalisation/Lichtsignal`
- `Strasse/Trottoir/Platz`
- `Grünflächen/Spielplätze`
- `Beleuchtung/Uhren`

The category analysis showed that the increase in reports was not only a general rise in total volume, but also involved changes in the composition of reported issue types.

### Spatial Distribution in 2025

In 2025, reporting activity was unevenly distributed across Zurich Quartiere.

The Quartiere with the highest number of reports were:

1. Langstrasse
2. Sihlfeld
3. Altstetten
4. Wipkingen
5. Unterstrass

Langstrasse had the highest number of reports, with **1,200 reports** in 2025.

### Category Concentration in 2025

The category **Abfall/Sammelstelle** dominated the strongest Quartier-category combinations in 2025.

It was the most common category in **32 out of 34 Quartiere**.

The highest local shares of `Abfall/Sammelstelle` reports were found in Quartiere such as:

- Langstrasse
- Werd
- Sihlfeld
- Hard
- Alt-Wiedikon

This suggests that waste and collection-point issues were especially important in the reporting patterns of these neighbourhoods.

---

## Visualizations

The project includes several visualizations:

- yearly bar chart of report counts
- monthly time-series plot
- stacked bar chart of report categories by year
- 100% stacked bar chart of category shares
- choropleth map of reports by Quartier in 2025
- choropleth map of `Abfall/Sammelstelle` share by Quartier

Saved visualizations are stored in:

`output/figures/`

---

## Requirements

This project uses Python and Jupyter notebooks.

The required Python packages are listed in `requirements.txt`.

To install the required packages, run:

`pip install -r requirements.txt`

Main libraries used:

- `pandas` for data loading, cleaning, and tabular analysis
- `geopandas` for spatial data processing
- `shapely` for geometry operations
- `matplotlib` for static visualizations and maps
- `jupyter` / `notebook` for running the notebooks

---

## How to Run the Project

1. Clone or download the project folder.

2. Install the required packages:

`pip install -r requirements.txt`

3. Place the raw ZüriWieNeu CSV file in:

`data/raw/`

4. Place the Zurich Quartiere shapefile folder in:

`data/raw/StatQuartiere_ZH/`

5. Run the notebooks in the following order:

- `00_dataexploration.ipynb`
- `01_R1.ipynb`
- `02_R2.ipynb`
- `03_R3.ipynb`
- `04_R4.ipynb`

The first notebook prepares and explores the data. The following notebooks each answer one research question.

---

## Notes on Interpretation

The ZüriWieNeu dataset represents reported urban issues. Therefore, the results should be interpreted as patterns of reporting activity, not as direct measurements of infrastructure quality.

A high number of reports in a Quartier may reflect actual infrastructure problems, but it may also be influenced by:

- population density
- visitor activity
- centrality
- land use
- nightlife or commercial activity
- awareness of the reporting platform