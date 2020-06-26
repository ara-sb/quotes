quotes
======

The quotation blog app is based on the [Flask Tutorial](https://github.com/pallets/flask/tree/1.1.2/examples/tutorial) and is used as an example for academic purposes.


Install
======

Clone the respository:

    $ git clone https://github.com/ara-sb/quotes
    $ cd quotes

Create a virtualenv and activate it:

    $ python3 -m venv venv
    $ . venv/bin/activate

Install quotes:

    $ pip install -e .

Run
======


    $ export FLASK_APP=quotes
    $ export FLASK_ENV=development
    $ export FLASK_DEBUG=1
    $ flask init-db
    $ flask run

Open http://127.0.0.1:5000 in a browser.


Test
======

    $ pip install '.[test]'
    $ pytest

Run with coverage report:

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser