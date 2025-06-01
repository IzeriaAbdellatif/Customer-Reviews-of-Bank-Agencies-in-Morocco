# Moroccan Bank Reviews Analysis

> 🏦 Advanced ETL pipeline for analyzing customer reviews of bank agencies across Morocco using Google Maps data and ML-powered sentiment analysis.

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)](https://www.postgresql.org/)

## 🎯 Project Overview

This project analyzes customer sentiment towards Moroccan banks by processing Google Maps reviews through an automated ETL pipeline, focusing on the Daraa-Tafilelt region.

### Key Features

- 🤖 Automated Google Maps review extraction
- 🔍 ML-powered multilingual sentiment analysis
- 📊 Interactive dashboards and visualizations
- 🗃️ PostgreSQL database integration
- 🔄 Automated data pipeline with Airflow

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/Bank-Reviews-Morocco.git
cd Bank-Reviews-Morocco

# Create virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```
---

## ⚙️ Airflow Installation and Initialization

This project uses Apache Airflow to orchestrate ETL tasks. Follow these steps to set up Airflow:

1. **Install Airflow**  
   - It’s recommended to use a virtual environment.  
   - Install with:
     ```bash
     pip install apache-airflow
     ```

2. **Initialize Airflow**  
   - Run the following command to initialize the Airflow metadata database:
     ```bash
     airflow db init
     ```

3. **Set Up DAGs Folder**  
   - Create a new folder named `airflow` at your desired location.
   - Inside `airflow`, create another folder named `Dags` (case-sensitive).
   - Copy the contents of your repository’s `airflow` folder into the newly created `airflow/Dags` folder.
   - Your Airflow DAGs should now be in:  
     `airflow/Dags/`

4. **Configure Airflow**  
   - (Optional) Point Airflow to your new DAGs folder by setting the `dags_folder` variable in `airflow.cfg` or via the environment variable:
     ```bash
     export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/airflow/Dags
     ```

5. **Start Airflow**  
   - Start the Airflow webserver and scheduler in separate terminals:
     ```bash
     airflow webserver
     airflow scheduler
     ```
   - Access the Airflow UI at [http://localhost:8080](http://localhost:8080).

**Note:** Make sure all your DAG Python scripts are in `airflow/Dags` for Airflow to detect and manage them.

---

## 🛠️ Technology Stack

- **Data Collection**: Google Maps API
- **Processing**: Python
- **ML/NLP**: Transformers
- **Storage**: PostgreSQL
- **Orchestration**: Apache Airflow
- **Visualization**: Looker studio

## 📊 Visualizations & Dashboard

Access our interactive dashboard: [Bank Reviews Dashboard](https://lookerstudio.google.com/reporting/a391b1ac-d8ac-4d24-8773-7ec4c162b78a)

The dashboard includes:
- Real-time sentiment analysis results
- Bank performance comparisons
- Regional distribution of reviews
- Customer satisfaction trends
- Topic analysis by bank and region
- Review volume patterns

Key visualizations include:
- Sentiment distribution by bank
- Regional satisfaction map
- Topic modeling insights
- Trend analysis over time
- Review volume by location
- Rating distributions


## 📝 License

This project is MIT licensed. See [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📫 Contact

[@IzeriaAbdellatif](https://github.com/yourusername) , [@MedTahiri](https://github.com/MedTahiri)

Project Link: [https://github.com/yourusername/Bank-Reviews-Morocco](https://github.com/yourusername/Bank-Reviews-Morocco)
