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