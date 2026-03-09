# Report Draft: Sections 2, 3, and 4 (KNN)

Use the content below in your 4–5 page technical report. Adjust wording to match your full document.

---

## Section 2: Data Description

We use the **Diabetes 130-US Hospitals for Years 1999–2008** dataset (Strack et al., 2014). The dataset contains **101,766** encounter-level records from 130 US hospitals over 1999–2008, with **47–50** features describing patient demographics, admission and discharge information, diagnoses, medications, and lab usage. The introductory paper by Strack et al. (2014) motivates the prediction of hospital readmission within 30 days and beyond.

The target variable is **readmitted**, which takes three values: **NO** (no readmission within 130 days), **&lt;30** (readmission within 30 days), and **&gt;30** (readmission between 31 and 130 days). Missing values are indicated by the symbol **"?"** in the raw data (e.g., in *weight*, *payer_code*, *medical_specialty*, and in some diagnosis fields). We replace these with missing-value placeholders and handle them in preprocessing (see Section 4). Identifiers (*encounter_id*, *patient_nbr*) are excluded from modeling. After preprocessing and optional removal or imputation of missing values, we apply feature scaling so that all numeric and encoded features are on a comparable scale for the classifiers.

---

## Section 3: Classifiers (KNN portion)

**K-Nearest Neighbors (KNN)** is a non-parametric, instance-based classifier: for a test point, it finds the *k* training examples nearest in feature space and assigns the majority class among those neighbors (or a distance-weighted vote). No explicit model is learned; prediction depends on the chosen distance metric (we use Euclidean distance) and the hyperparameter *k*.

We implement KNN using **scikit-learn** (`KNeighborsClassifier`). The **hyperparameter** we tune is the number of neighbors **k**. We investigate the following **k** values: **1, 3, 5, 7, 9, 11, 15, 21, 25, 31**. Model selection is performed by training on the training set and evaluating **validation accuracy** for each *k*; the *k* with the highest validation accuracy is selected, and the final performance is reported on the held-out test set.

---

## Section 4: Experimental Setup

**Data partitioning.** We use a **three-way holdout** split: **60%** of the data for **training**, **20%** for **validation** (hyperparameter selection), and **20%** for **testing** (final evaluation). Splits are **stratified** by the target (*readmitted*) so that class proportions are preserved in each subset. The same partition and random seed are used for all experiments to ensure reproducibility.

**Preprocessing.** Missing values marked as "?" in the raw data are first converted to missing (e.g., `NaN`). We then apply **imputation** (e.g., median for numeric features, most frequent for categorical) or optionally **removal** of instances/features with excessive missingness. Categorical features are **one-hot encoded**; **feature scaling** (e.g., standardization via zero mean and unit variance) is applied to all numeric and encoded features so that distance-based methods such as KNN are not dominated by any single feature.

**Metrics.** We report **accuracy** (fraction of correct predictions) on the validation set for model selection and on the test set for final evaluation. **Classification error** is 1 − accuracy. Additional metrics (e.g., per-class precision/recall, confusion matrix) can be reported for the chosen model on the test set.

**Software.** Preprocessing and modeling are implemented in **Python** using **pandas** and **scikit-learn**. The experimental pipeline is designed for **reproducibility** and **systematic evaluation** rather than maximizing accuracy alone.

---

## Reference

Strack, B., DeShazo, J. P., Gennings, C., Olmo, J. L., Ventura, S., Cios, K. J., & Clore, J. N. (2014). Impact of HbA1c measurement on hospital readmission rates: analysis of 70,000 clinical database patient records. *BioMed Research International*, 2014.
