# Machine Learning

Machine learning projects, model training, and deployment.

## Structure

- `models/` - Trained models (excluded from git)
- `training/` - Training scripts and pipelines
- `inference/` - Inference and serving code
- `experiments/` - ML experiments (MLflow tracking)
- `pipelines/` - End-to-end ML pipelines

## Setup

```bash
pip install scikit-learn tensorflow pytorch mlflow
```

## Best Practices

- Track experiments with MLflow
- Version datasets and models
- Document model performance metrics
- Use configuration files for hyperparameters
