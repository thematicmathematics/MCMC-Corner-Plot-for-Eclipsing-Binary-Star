# MCMC Corner Plot Visualization Tool for Eclipsing Binary
This tool is developed to provide a comprehensive statistical and visual analysis of MCMC posterior distributions for eclipsing binary star systems. It uniquely combines multiple confidence levels with robust outlier rejection, delivering publication-quality figures that highlight both parameter correlations and global optimization results.

## Key Features
* **Multi-Layered Contours:** Displays 68% (1-$\sigma$), 90% (1.64-$\sigma$), and 99% (2.57-$\sigma$) confidence levels in a single plot with distinct colors.
* **Statistical Precision:** Calculates asymmetric error bars based on the percentiles (e.g  16th, 50th, and 84th for 1-$\sigma$).
* **Robust Data Cleaning:** Implements a 5-$\sigma$ clipping method based on the **Median Absolute Deviation (MAD)** to remove outliers safely.
* **Publication Ready:** Generates high-resolution `.png` and vector-based `.eps` files suitable for academic journals.
* **Reference Comparison:** Allows overlaying "Best Fit" values (e.g., from differential correction methods like WD) against MCMC results.

## Requirements
To run this script, you will need:
* Python 3.x
* `pandas`, `numpy`, `matplotlib`, `corner`, `openpyxl`

You can install the dependencies via pip: 
```bash
pip install pandas numpy matplotlib corner openpyxl
```
## Data Format
The script expects an Excel file (`.xlsx`) containing three separate sheets. Each sheet should contain the MCMC chain samples corresponding to the desired confidence interval:

* **err68:** Samples for the 1-$\sigma$ distribution (covers 16th to 84th percentiles).
* **err90:** Samples for the 90% distribution (covers 5th to 95th percentiles).
* **err99:** Samples for the 99% distribution (covers 0.5th to 99.5th percentiles).

> **Note:** Ensure that each sheet has identical column names corresponding to the parameters defined in the `params` list within the script.

## How to Use
1.  **Place Data:** Move your Excel data file into the same directory as the script.
2.  **Configure Script:** Open the script and update the following variables to match your specific star system:
    * `EXCEL_FILE`: The name of your data file.
    * `params`: List of parameter names as they appear in your Excel columns.
    * `outDSP`: Update this dictionary with your "Best Fit" (e.g., MC or WD output) values.
3.  **Refine Cleaning:** If your parameter space is significantly different, adjust the hard-coded limits and the $\sigma$ clipping value in the `load_and_clean` function.
4.  **Run:** Execute the script using the following command:

```bash
python cornerplot.py
 ``` 
S. Ceren Çalışkan Astrophysics MSc Student Çanakkale Onsekiz Mart University
If you use this tool in your research, please cite it as follows:

Çalışkan, S. C. (2026). MCMC Corner Plot Visualization Tool for Eclipsing Binary. GitHub Repository.
