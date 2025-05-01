# Data Pipeline Project

This project implements a modern data stack using Airflow, dbt, Jupyter, and Superset for data orchestration, transformation, analysis, and visualization.

## 🚀 Stack Components

- **Apache Airflow**: Workflow orchestration
- **dbt**: Data transformation
- **Jupyter**: Interactive data analysis
- **Apache Superset**: Data visualization and exploration
- **Docker**: Containerization and local development
- **Make**: Build automation and setup

## 📋 Prerequisites

- Docker and Docker Compose
- Make
- Python 3.x
- Git

## 🔧 Setup

1. Clone the repository:
```bash
git clone git@gitlab.com:lappis-unb/gest-odadosipea/app-lappis-ipea.git
cd app-lappis-ipea
```

2. Run the setup using Make:
```bash
make setup
```

This will:
- Create necessary virtual environments
- Install dependencies
- Set up pre-commit hooks
- Configure development environment

## 🏃‍♂️ Running Locally

Start all services using Docker Compose:

```bash
docker-compose up -d
```

Access the different components:
- Airflow: http://localhost:8080
- Jupyter: http://localhost:8888
- Superset: http://localhost:8088

## 💻 Development

### Code Quality

This project uses several tools to maintain code quality:
- Pre-commit hooks
- Linting configurations
- Automated testing

Run linting checks:
```bash
make lint
```

Run tests:
```bash
make test
```

### Project Structure

```
.
├── airflow/
│   ├── dags/
│   └── plugins/
├── dbt/
│   └── models/
├── jupyter/
│   └── notebooks/
├── superset/
│   └── dashboards/
├── docker-compose.yml
├── Makefile
└── README.md
```

### Makefile Commands

- `make setup`: Initial project setup
- `make lint`: Run linting checks
- `make tests`: Run test suite
- `make clean`: Clean up generated files
- `make build`: Build Docker images

## 🔐 Git Workflow

This project requires signed commits. To set up GPG signing:

1. Generate a GPG key:
```bash
gpg --full-generate-key
```

2. Configure Git to use GPG signing:
```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
```

3. Add your GPG key to your GitLab account

## 📚 Documentation

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Superset Documentation](https://superset.apache.org/docs/intro)

## 🤝 Contributing

1. Create a new branch for your feature
2. Make changes and ensure all tests pass
3. Submit a merge request
