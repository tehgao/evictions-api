# Evictions API

The Evictions API is a simple web application that faciliates tracking of evictions cases.

## Usage
Before starting the application set your SECRET_KEY environment variable to something nice and high entropy. You can use something like [djecrety](https://djecrety.ir/) to get one.

```bash
pip install -e .
manage.py migrate
manage.py runserver
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)