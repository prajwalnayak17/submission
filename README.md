# Project Dependencies

This document lists the dependencies required to run the web scraping script.

## Dependencies

The following Python packages are required:

- **selenium**: A web automation tool used for web scraping.
- **pandas**: A library for data manipulation and analysis.

## Installation

To install the required dependencies, follow these steps:

1. **Ensure you have Python 3.7+ installed**.

2. **Create a virtual environment** (recommended but optional):

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    Make sure you have a `requirements.txt` file in your project directory with the following content:

    ```plaintext
    selenium
    pandas
    ```

## Additional Setup

- **Google Chrome**: Ensure you have Google Chrome installed.
- **ChromeDriver**: Download the ChromeDriver version that matches your Google Chrome version and place it in your project directory or add it to your system's PATH.

For further details on using the script, please refer to the project documentation.

## License

This project is licensed under the MIT License.
