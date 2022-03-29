# wordpress-social
Share your Wordpress articles on Social Media.

[![Continuous Integration](https://github.com/aveek22/wordpress-social/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/aveek22/wordpress-social/actions/workflows/continuous-integration.yml) [![Setup Terraform](https://github.com/aveek22/wordpress-social/actions/workflows/setup-terraform.yml/badge.svg)](https://github.com/aveek22/wordpress-social/actions/workflows/setup-terraform.yml)

## Install libraries for AWS Lambda Layer

Use the following command from the root direcotry to install specific modules into a directory.

```bash
pip install -r app/lambda_layers/requirements.layers.txt -t app/lambda_layers/packa
ges/python --upgrade
```

Run the following command to create a ZIP for Lambda Layers.

```bash
cd app/lambda_layers/packages
zip -r python.zip python
```

## Installation
Download or clone the repository from GitHub.
```bash
git clone https://github.com/aveek22/wordpress-social.git
cd wordpress-social
```

Create the python virtual environment
```bash
python -m venv .venv
```

Install Poetry
```bash
pip install --upgrade pip
pip install poetry
```

Install dependencies
```bash
poetry install
```

To add new packages to the module, consider using poetry
```bash
poetry add <packages>
```