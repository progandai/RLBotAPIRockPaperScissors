import argparse
from api.app import initialize_app

if __name__ == '__main__':
    app = initialize_app()
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", required=False, default="127.0.0.1", help="Host arg.")
    parser.add_argument("--port", required=False, default="5000", help="Port arg.")
    parser.add_argument("--debug", required=False, default=True, help="Mode debug arg.")

    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug="True" == args.debug)
