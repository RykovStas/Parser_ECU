-----
# First TASK

 The data loading project is designed to load and process data using web pages and store them in a database.
 
## Download

1. Install the necessary dependencies by running the command:
```
pip install -r requirements.txt
```
2. Make sure you have Google Chrome web browser installed as the script uses Selenium WebDriver to automatically interact with the web page.

## Setting

1. Open the `main.py` file and set the following options in the "SETTINGS" section:

- `download_directory`: Specify the path to the directory where downloaded files will be saved.

2. Create a SQLite database named `database.db` using the SQLite tool of your choice.

3. Run the `create_last_processed_file_table()` script once to create the `LastProcessedFile` table in the database.

## Run

Run the `main.py` script to initially load the data and save it to the database.

```shell
python main.py
```
-----

-----
# Second Task

The Flask project provides the ability to get data from a database and return it in JSON format.

## Installation

1. Install the project dependencies with the command:
```
pip install -r requirements.txt
```

2. Create a database file `database.db` with the required schema and data.

## Run

1. Run the Flask application with the command:
```
python app.py
```

2. The application will be available at `http://localhost:5000/`.

## Usage

### Getting data

- To get all data from the database in JSON format, send a GET request to `http://localhost:5000/`.

- To get data for a specific date, send a GET request to `http://localhost:5000/get_data/<date>`, where `<date>` is the date in the format `DD-MM-YYYY`. For example, `http://localhost:5000/get_data/12-06-2023`.

Answer example:
```
[
{
"Дата": "12.06.2023",
"Година": "01:00",
"Ціна_грн_МВт_год": "2 000,00",
"Обсяг_продажу_МВт_год": "1 427,1",
"Обсяг_купівлі_МВт_год": "1 427,1",
"Заявлений_обсяг_продажу_МВт_год": "1 427,1",
"Заявлений_обсяг_купівлі_МВт_год": "2 726,0"
},
...
]
```
If no data is found for the specified date, it will return:
```
{
"error": "Data not found for the given date."
}
```

-----