# Publishing Instructions for PyPI

This document describes the process of publishing the `dialog-yaml` library to PyPI.

## Pre-publishing checklist

Before publishing, make sure that:

1. You have updated the version in `pyproject.toml`
2. All changes are committed to Git
3. You have tested the library locally

## Requirements

Install the necessary tools for publishing:

```bash
pip install build twine
```

Or using uv:

```bash
uv pip install build twine
```

## Publishing Process

### 1. Creating a distribution

You can create a distribution using the Make command:

```bash
make build
```

Or directly with Python:

```bash
rm -rf dist/ build/ *.egg-info  # cleaning up previous builds
python -m build
```

As a result, files will be created in the `dist/` directory:

- `dialog-yaml-{version}.tar.gz` - source archive
- `dialog-yaml-{version}-py3-none-any.whl` - wheel file

### 2. Checking the distribution

Before uploading to PyPI, you can check the created distribution:

```bash
python -m twine check dist/*
```

### 3. Publishing to TestPyPI (recommended)

To test the publishing process, use TestPyPI:

```bash
make upload-testpypi
```

Or directly:

```bash
python -m twine upload --repository testpypi dist/*
```

This will require you to configure your credentials in the `~/.pypirc` file.

### 4. Publishing to PyPI

After successful testing, upload the package to PyPI:

```bash
make upload-pypi
```

Or directly:

```bash
python -m twine upload dist/*
```

## .pypirc configuration

Create a `~/.pypirc` file with the following content:

```pypirc
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your_pypi_token_here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your_testpypi_token_here
```

For security, it is recommended to use tokens instead of a username and password.

## Using PyPI tokens

1. Log in to your PyPI account
2. Go to "Account settings" → "API tokens"
3. Create a new token
4. Use the token as the password in the `.pypirc` file

## Cleanup

To clean up build files, use:

```bash
make clean
```

## Recommendations

- Always test publishing to TestPyPI before publishing to the main PyPI
- Increment the version number with each new release according to semantic versioning
- Check that all files are included in the package using MANIFEST.in
