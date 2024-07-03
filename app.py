import os
from src import app

if __name__ == "__main__":
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    debug = os.getenv('DEBUG') == 'True'

    app.run(host=host,
            port=port,
            debug=debug)
