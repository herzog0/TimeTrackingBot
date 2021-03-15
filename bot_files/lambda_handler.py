import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
from src.main import main
from src.support.logger import logger


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': str(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    """

    operations = {
        'POST': main,
    }

    if event.get('httpMethod', False):
        operation = event['httpMethod']
    else:
        operation = "not available"

    payload = base64.b64decode(event['body'])
    try:
        payload = json.loads(payload)
    except TypeError:
        pass

    if operation in operations:
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError(f'Unsupported method {operation}'))


if __name__ == '__main__':
    # for local testing
    # start ngrok and register the https url to telegram webhooks
    from sys import argv

    class S(BaseHTTPRequestHandler):
        def _set_response(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself
            logger.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                        str(self.path), str(self.headers), post_data.decode('utf-8'))
            main(json.loads(post_data.decode('utf-8')))
            self._set_response()
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


    def run(server_class=HTTPServer, handler_class=S, port=8080):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        logger.info('Starting httpd...\n')
        try:
            logger.info('You should now start Ngrok pointing to your port 8080')
            logger.info('Then, set the webhook to the https url given by ngrok')
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logger.info('Stopping httpd...\n')

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
