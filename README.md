
# Performance Measures of Database Types and Transformation Methods - Measuring Local ETL Performance
## Hello and Welcome!

## Overview

This project aims to evaluate the performance of various database systems and data transformation tools in a local Extract, Transform, Load (ETL) environment. By comparing MySQL and MongoDB for data storage, alongside Python's Pandas and NVIDIA's RAPIDS for data transformation, we seek to identify optimal combinations that minimize resource usage and maximize efficiency.

![](https://github.com/7446Nguyen/Database_FileManagement_Project1/blob/master/scripts/images/ETLsoftware.png)

## Repository Structure

- **Reports and Findings/**: Contains IEEE-formatted project proposals and final reports detailing methodologies, experiments, and conclusions.
- **data/**: Includes raw datasets and performance metrics collected during testing phases.
- **scripts/**: Houses all scripts used for data extraction, transformation, loading, and performance benchmarking.

## Key Objectives

1. **Database Performance**: Assess the efficiency of relational (MySQL) versus non-relational (MongoDB) databases during data extraction and loading phases.
2. **Transformation Tools Comparison**: Evaluate the speed and resource consumption of data transformations using CPU-based Python Pandas versus GPU-accelerated NVIDIA RAPIDS.
3. **Optimal ETL Strategy**: Determine the best combination of database and transformation tool for various data scenarios to inform best practices in ETL processes.

## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/7446Nguyen/ETL-Performance-Comparative-Analysis.git
   cd ETL-Performance-Comparative-Analysis
   ```
2. **Set Up Environment**:
   - Ensure you have Python installed.
   - Install necessary packages using `pip` or `conda` as specified in the `scripts/requirements.txt` file.
   - For GPU acceleration tests, ensure you have a compatible NVIDIA GPU and have installed the appropriate CUDA toolkit.
3. **Run Scripts**:
   - Navigate to the `scripts/` directory and execute the desired ETL scripts to perform data transformations and collect performance metrics.

## Data Sources

The datasets used in this project are located in the `data/` directory. These datasets are utilized to benchmark the performance of different ETL strategies.

## Authors

- **Jeff Nguyen**

## Acknowledgments

Special thanks to the open-source community and contributors of MySQL, MongoDB, Pandas, and NVIDIA RAPIDS for providing the tools necessary for this analysis.
