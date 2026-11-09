# SpaceX Falcon 9 Landing Outcome Analysis

**Python · SQL · scikit-learn · Plotly Dash · Folium**

An end-to-end data science capstone exploring SpaceX Falcon 9 launch records and classifying first-stage landing outcomes. This work was completed as part of the **IBM Data Science Professional Certificate (Coursera)**.

## Project at a glance

- **Question:** How do launch characteristics relate to Falcon 9 first-stage landing outcomes, and how well can standard classifiers distinguish successful from unsuccessful landings?
- **Methods:** API/CSV data exploration, SQL queries, exploratory visualizations, interactive mapping/dashboarding, and supervised classification.
- **Classifiers:** Logistic regression, support vector machine (SVM), decision tree, and k-nearest neighbors (KNN), with `GridSearchCV` tuning.
- **Evaluation:** 80/20 train/test split (`random_state=2`) in the classification notebook; the resulting test set contains **18 launches**.

## Classification results

These numbers are **saved notebook outputs**, not independently rerun benchmarks.

| Classifier | Saved test accuracy | Correct / 18 |
| --- | ---: | ---: |
| Logistic regression | **83.3%** | 15 |
| Support vector machine | **83.3%** | 15 |
| K-nearest neighbors | **83.3%** | 15 |
| Decision tree | 66.7% | 12 |

Three classifiers tied on the test set; the notebook selects logistic regression as the displayed best model because of the tie-breaking order in its comparison code. The model-tuning cross-validation results are different from the held-out test accuracies.

> **Interpretation caution:** With only 18 test observations, the accuracy estimates are sensitive to individual predictions. The notebook scales the full feature matrix **before** the train/test split, which can leak test-set information into preprocessing. The decision-tree grid also contains an unsupported `max_features='auto'` setting on some scikit-learn versions, producing failed fits. Treat these results as educational and preliminary, **not** validated production performance.

## Analysis workflow

1. **Data collection and preparation:** Explore the IBM-hosted SpaceX API snapshot and course CSV datasets; inspect launch records and attributes.
2. **SQL exploration:** Use SQLite to group launches by launch site, compare payload masses, and count successful landings.
3. **EDA:** Visualize launch site, orbit, payload mass, flight number, and landing outcomes.
4. **Geospatial exploration:** Use Folium to mark launch sites and landing outcomes.
5. **Interactive dashboard:** Use Plotly Dash to filter launch sites and payload ranges and inspect landing outcome plots.
6. **Classification:** Compare four scikit-learn models using hyperparameter searches, confusion matrices, and test accuracy.

The repository represents several related course exercises. The notebooks do not form a single fully automated pipeline, and some rely on IBM-hosted source data or legacy course code.

## Repository guide

| File | Purpose |
| --- | --- |
| [`spacex_data.ipynb`](spacex_data.ipynb) | SpaceX launch API snapshot and Wikipedia scraping exploration |
| [`spacex_sql.ipynb`](spacex_sql.ipynb) | SQL queries on launch records |
| [`spacex_visual.ipynb`](spacex_visual.ipynb) | EDA plots and an additional logistic regression example |
| [`spacex_folium.ipynb`](spacex_folium.ipynb) | Interactive launch-site maps |
| [`spacex_dash.py`](spacex_dash.py) | Interactive Dash dashboard |
| [`spacex_classfication.ipynb`](spacex_classfication.ipynb) | Four-model classification and evaluation (filename retained as uploaded) |

**Note:** The additional logistic regression example in `spacex_visual.ipynb` shows a **72%** test accuracy with a different feature set/split. It is not directly comparable to the classification notebook's 83.3% results.

## How to explore

1. Clone or download the repository and install Python 3 with Jupyter Notebook or JupyterLab.
2. Install relevant packages for the notebooks:

   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn requests beautifulsoup4 folium plotly dash jupyter ipython-sql prettytable
   ```

3. Open notebooks individually and run cells in order. Some download CSV files from **IBM Skills Network** and require internet access.
4. For the dashboard, run `python spacex_dash.py` in the repository folder, then open the local address printed by Dash. The dashboard downloads a course CSV on startup.
5. If a notebook fails due to a changed website, removed course URL, library version, or missing CSV, inspect its data-loading cell. The Wikipedia scraping exercise currently has a saved **empty DataFrame** output, so that portion should not be treated as a working scraper.

## Limitations and next steps

- Refit preprocessing **inside a scikit-learn Pipeline** after splitting, and tune hyperparameters on training folds only.
- Remove invalid decision-tree options; report precision/recall and uncertainty, in addition to accuracy.
- Freeze dependency versions, provide stable source data or downloads, and make the notebooks run sequentially from a fresh environment.
- Add a screenshot of the dashboard and export representative figures once verified.

## Attribution

Created by **Jihoon Lim** as an **IBM Data Science / Coursera capstone and associated exercises**. Course-provided datasets and assignment structure are attributed to IBM Skills Network. Results above are taken from the committed notebook outputs.
