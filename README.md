# SDS210 Individual Project: ZüriWieNeu Urban Issue Analysis

## Project Overview

This project analyses reported urban infrastructure issues in the city of Zurich using open data from the **ZüriWieNeu** reporting platform.

ZüriWieNeu allows residents to report problems in public space, such as waste at collection points, damaged streets, broken lighting, graffiti, or issues with green spaces. The dataset contains individual reports with timestamps, categories, coordinates, and descriptive text.

The goal of this project is to build a clear and reproducible data workflow that reads, cleans, structures, analyses, and visualizes the ZüriWieNeu data. The analysis combines temporal, categorical, and spatial perspectives.

The project works with the CSV file available from the City of Zurich in addition to Quartier Information and population counts. 

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

This question introduces spatial analysis by assigning individual report points to Zurich Quartier polygons and comparing reporting intensity across neighbourhoods using two normalised rates:

- reports per 1'000 residents: using population data from the City of Zurich
- reports per km^2: using the Quartier area computed from the shapefile geometry

### Research Question 4

**Are certain types of ZüriWieNeu reports concentrated in particular Zurich Quartiere in 2025, and within the dominant category, where exactly in the city do these reports cluster?**

This question analyses whether specific report categories, especially **Abfall/Sammelstelle**, are spatially concentrated in certain Quartiere. The analysis is done in two stages: 
1. A Quartier-level choropleth of the share of **Abfall/Sammelstelle** reports within each Quartier
2. A **Kerndel Density Estimation (KDE)** on the point locations of all **Abfall/Sammelstelle** reports in 2025, revealing where within the city these reports cluster independently of administrative boundaries

---

## Project Structure

SDS210_IndividualProject/

- data/
  - raw/
    - stzh.zwn_meldungen_p.csv
    - StatQuartiere_ZH/
      - Zurich Quartiere shapefile files
    - bev324od3240.csv
  - processed/
    - zueriwieneu_cleaned.csv

- notebooks/
  - 00_dataexploration.ipynb
  - 01_R1.ipynb
  - 02_R2.ipynb
  - 03_R3.ipynb
  - 04_R4.ipynb

- output/
  - saved visualizations (PNG files)

- src/
  - __init__.py
  - loading.py
  - cleaning.py
  - analysis.py
  - spatial.py

- environment.yml
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

### Population Data

For the research question 3, the project uses the Open Data Zürich dataset *Bevölkerung nach Stadtquartier* (`bev324od3240.csv`), which contains the economically resident population (ÀnzBestWir) per statistical Quartier (`QuarLang`) and year (`StichtagDatJahr`). The data is filtered specifically to the year 2025 to fit the analysis for allowing the calculation of reports per 1'000 residents in the Quartier. 

---

## Methods

The project follows a reusable data workflow.

### 1. Loading

The raw CSV file is loaded using a reusable function from `src/loading.py`.

### 2. Cleaning

The cleaning workflow is implemented in `src/cleaning.py`.

The main cleaning steps are:

1. Convert date columns to datetime format (`requested_datetime`, `agency_sent_datetime`, `updated_datetime`). 
2. Remove duplicate reports based on `service_request_id`. On the current export this finds 0 duplicates, but the step is done to ensure the correct amount of report counts. 
3. Drop the `service_code` column, but only if it is identical to `service_name`. Right now, the information in both columns is the same, so keeping both columns would be redundant. 
4. Add time-based columns:
   - `year`
   - `month`
   - `year_month`

These steps are combined in one reusable function:

`df_clean = clean_reports(df_raw)`

This ensures that the same cleaning logic is applied consistently across all notebooks.

### 3. Temporal Analysis

Temporal analysis is used for Research Questions 1 and 2 and is implemented in `src/analysis.py`.

The project calculates:

- yearly report counts (`count_reports_per_year`)
- monthly report counts (`count_reports_per_month`)
- report counts by year and category (`count_reports_by_year_and_category`)
- category shares by year (derived from the year-and-category counts in the notebook)

### 4. Spatial Analysis

Spatial analysis is used for Research Questions 3 and 4 and is implemented in `src/spatial.py`.

The report data is converted into a GeoDataFrame using the coordinate columns `e` and `n` (through `reports_to_geodataframe`). Each report is then spatially joined to a Zurich Quartier polygon (with the function `join_reports_to_quartiere`).

This allows the project to calculate:

- total reports per Quartier
- reports per 1'000 residents per Quartier (Notebook 03)
- reports per km^2 per Quartier, with the Quartier area computed from the shapefile geometry (Notebook 03)
- report categories per Quartier (Notebook 04)
- dominant categories by Quartier (Notebook 04)
- category shares within each Quartier (Notebook 04)

### Kernel Density Estimation (KDE)

In notebook 4, to identify clusters of the point data showing **Abfall/Sammelstelle** data in 2025, a KDE was done. The `bw_adjust` parameter allows to control the bandwidth, to ensure that there is a balance between local clusters and city-wide pattern. In this analysis, the value of `0.5` was chosen after comparing results from three different bandwidths (`0.3`, `0.5`, `1`). 

---

## Main Findings

### Reporting Volume Over Time

The number of ZüriWieNeu reports increased strongly between 2013 and 2025. After a decline between 2013 and 2015, reporting activity began to rise again from 2016 onward. The increase became especially strong after 2018. There were 3'724 reports in 2018 and 11'588 reports in 2025. 

The highest full-year report count occurred in 2025, with **11,588 reports**.

### Category Development Over Time

Over the time of the ZüriWieNeu platform, there have been changes in the categories to report to, with 6 categories initially available and additional four being added over time. The most common report category across the full period was **Abfall/Sammelstelle**.

Other important categories included:

- `Signalisation/Lichtsignal`
- `Strasse/Trottoir/Platz`
- `Grünflächen/Spielplätze`
- `Beleuchtung/Uhren`

The 100% stacked bar chart showed that the increase in reports was not only a general rise in total volume, but also involved changes in the relative compostion of reported issues types. 

### Spatial Distribution in 2025

In 2025, reporting activity was unevenly distributed across Zurich Quartiere and the two normalisations gave overlapping but different pictures.

**Reports per 1'000 residents:** The map is highly polarised on the Quartiere City and Hochschulen, with both being non-residential areas. A small residential population pushes these two Quartiere, as there are many reports documented. 

**Reports per km^2:** A more gradual pattern can be identified, with a clear peak around Langstrase and high values in Lindenhof, Rathaus and City. 

In both choropleth maps, it becomes visible how there is a concentration of reports in the centre of the City of Zurich and a decrease towards the periphery of the City. There are disagreements in the two approaches, shown in more detail for *Langstrasse*. Langstrasse ranks fourth on the per-resident map, but first on the per-km^2 map. When choosing an approach, the resident one is less reliable, as not only residents of the Quartier can upload reports. 

### Category Concentration in 2025

The category `Abfall/Sammelstelle` dominated the strongest Quartier-category combinations in 2025. It was the most common category in **32 out of 34 Quartiere** and the other two Quartiere were dominated by `Signalisation/Lichtsignal`. 

The highest local shares of `Abfall/Sammelstelle` reports were found in Quartiere such as:

- Langstrasse
- Werd
- Sihlfeld
- Hard
- Alt-Wiedikon

The Kernel Density Estimation on the point location of all 2025 Abfall/Sammelstelle reports add a finer view to the choropleth map highlighting specific clusters in the City. 

---

## Visualizations

The project includes the following visualizations, all saved to the `outputs/` folder:

- `R1_YearlyReport_BarChart.png` — yearly bar chart of report counts (2014–2025)
- `R1_MonthlyNumbers.png` — monthly time-series plot of report counts
- `R2_StackedBar_Categories.png` — stacked bar chart of report categories by year
- `R2_ShareCategories_Stacked.png` — 100% stacked bar chart of category shares by year
- `R3_Choropleth_ReportsPer1000.png` — choropleth of reports per 1,000 residents by Quartier in 2025
- `R3_Choropleth_ReportsPerKm2.png` — choropleth of reports per km² by Quartier in 2025
- `R4_Share_LargestReport_ByQuartier.png` — choropleth of the share of Abfall/Sammelstelle reports by Quartier in 2025
- `R4_KDE_Abfall_2025.png` — Kernel Density Estimation heatmap of Abfall/Sammelstelle report points in 2025
- `R4_KDE_Abfall_Bandwidth.png` — side-by-side KDE comparison for three bandwidth values (sensitivity check)

---

## Requirements

This project uses Python and Jupyter notebooks.

The conda environment is defined in `environment.yml` (environment name: `sds-env`).

To create and activate the environment, run:

```bash
conda env create -f environment.yml
conda activate sds-env
```

Main libraries used:

- `pandas` for data loading, cleaning, and tabular analysis
- `geopandas` for spatial data processing
- `matplotlib` for static visualizations and maps
- `seaborn`for kernel density estimation and visualisation
- `jupyter` / `notebook` for running the notebooks

---

## How to Run the Project

1. Clone or download the project folder.

2. Create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate sds-env
```

3. Place the following files in `data/raw/` with these exact names:

| File | Description |
|----------------------------|-----------------------------------------------------------------|
| `stzh.zwn_meldungen_p.csv` | ZüriWieNeu report data (Open Data Zürich)                       |
| `bev324od3240.csv`         | Population by Quartier (Open Data Zürich, dataset bev324od3240) |
| `StatQuartiere_ZH/`        | Folder containing the Zurich Quartiere shapefiles               |

The filenames are hardcoded in the notebooks and must match exactly (including case).

4. Run the notebooks in the following order:

- `00_dataexploration.ipynb`
- `01_R1.ipynb`
- `02_R2.ipynb`
- `03_R3.ipynb`
- `04_R4.ipynb`

The first notebook prepares and explores the data. The following notebooks each answer one research question.

Note: Always select `sds-env` as Kernel for execution of the notebooks.
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

This is particularly relevant for the per-resident rate in Research Question 03, where Quartiere with very small residential population but high daytime activity appear as extreme outliers. With the approach of Quartier area or the clustering of point data, this issue of residential population is reduced, but still describe a reporting behaviour rather than the underlying urban issues directly in the City of Zurich. 