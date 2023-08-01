# CONTRIBUTING to configure_dms_viz

Hello and thank you for your interest in contributing to `configure_dms_viz`! Here's how you can help.

## Getting Started:

### 1. Set Up Your Environment:

We use [`Poetry`](https://python-poetry.org/) for dependency management and packaging. If you don't have it installed, get it [here](https://python-poetry.org/docs/#installation).

### 2. Fork the Repository:

Before you start making changes, fork the repository to your own GitHub account.

### 3. Clone Your Fork:

Clone your forked repository to your local machine.

```bash
git clone https://github.com/dms-viz/configure_dms_viz.git
cd configure_dms_viz
```

### 4. Install Dependencies:

With `Poetry`, setting up the project environment and installing dependencies is easy:

```bash
poetry install
```

## Contributing Guidelines:

### 1. Work on a New Branch:

Don't work directly on the main branch. Create a new branch for your feature or bug fix.

```bash
git checkout -b your-new-feature-or-fix
```

### 2. Document Your Changes:

Make sure to comment your code appropriately. If you're introducing a new feature or making significant changes, update the README.md file as necessary.

### 3. Commit Your Changes:

Make granular commits with meaningful commit messages. This makes it easier to review your contributions.

### 4. Push to Your Fork:

Push the changes to your forked repository.

```bash
git push origin your-new-feature-or-fix
```

### 5. Create a Pull Request:

Once you're done with your changes and you think it's ready for review, create a pull request from your forked repository to the original repository.

## Code Formatting

The code is formatted using `Black`, which will be installed as a development dependence by `Poetry`. Linting is handled by `Ruff`, which will also be installed by `Poetry`.
