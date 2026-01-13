# Gemini Context: `pangumd` Project

## Project Overview

This is a Python project named `pangumd`. Its primary purpose is to intelligently add spacing between Chinese/Japanese/Korean (CJK) characters and Latin alphabet/numeric characters. The key feature is its special handling of Markdown syntax, ensuring that formatting like code blocks, bold/italic text, and links are not broken by the spacing logic.

The project uses the `pangu` library for the core spacing algorithm and `marko` for parsing Markdown. It provides a library interface, a command-line tool, and a pre-commit hook.

## Key Files

- `pangumd.py`: The main module containing all the logic. It defines the custom Markdown renderer and the CLI interface.
- `pyproject.toml`: The project definition file. It specifies dependencies (`marko`, `pangu`), development tools (`pytest`, `ruff`), and defines the `pangumd` console script.
- `README.md`: Contains general information, installation instructions, and usage examples. **Note:** There is a discrepancy between the CLI usage shown in the README and the actual implementation in `pangumd.py`.
- `tests/`: Contains unit tests for the project, verifying both the general spacing logic and the Markdown-specific handling.
- `.pre-commit-config.yaml`: Configures `ruff` to automatically lint and format code before commits.

## Building, Running, and Testing

### Dependencies

To install all dependencies, including for development and testing, run:

```bash
# This project uses uv, but pip can also be used.
uv pip install -e ".[test,lint]"
```

### Running the Tool

The project can be run as a command-line tool to format files in-place.

```bash
# The CLI tool modifies files directly.
python -m pangumd <file1.md> <file2.txt> ...
```

**Note:** The current CLI implementation in `pangumd.py` only supports file paths as arguments and modifies them in-place. The `README.md` shows more advanced usage (like processing strings from arguments or stdin), which is not currently implemented.

### Running Tests

Tests are located in the `tests/` directory and are run using `pytest`.

```bash
pytest
```

## Development Conventions

- **Code Style**: The project uses `ruff` for both formatting and linting. The configuration is in `pyproject.toml` (`[tool.ruff]`). Key styles include a line length of 100 characters and single quotes for strings.
- **Pre-commit Hooks**: The repository is set up with pre-commit hooks (see `.pre-commit-config.yaml`) that automatically run `ruff` to format and lint staged files. To enable this, you need to run `pre-commit install` once after cloning the repository.
- **Testing**: The project uses `pytest`. New features should be accompanied by tests in the `tests/` directory.
