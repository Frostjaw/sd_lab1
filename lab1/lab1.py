import pytz, urllib, json
from html import escape
from pytz import timezone
from datetime import datetime
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

class AppClass:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        response_headers = [('Content-type', 'text/plain')]
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'

        # GET
        if self.environ['REQUEST_METHOD'] == 'GET':
            path = escape(self.environ.get('PATH_INFO', ''))
            if path != '/favicon.ico':
                global response, status

                if path == '/':
                    tz = timezone('GMT')
                    dt = datetime.now(tz)
                    response = dt.strftime(fmt)
                    status = '200 OK'
                else:
                    try:
                        tz = timezone(path[1:])
                        dt = datetime.now(tz)
                        response = dt.strftime(fmt)
                        status = '200 OK'
                    except Exception:
                        response = 'Invalid timezone'
                        status = '400 Bad Request'

                self.start(status, response_headers)            
                yield bytes(response, 'utf-8')
            else:
                status = '200 OK'
                self.start(status, response_headers)

        # POST
        elif self.environ['REQUEST_METHOD'] == 'POST':
            # /api/v1/convert
            if self.environ['PATH_INFO'] == '/api/v1/convert':
                try:
                    request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
                except ValueError:
                    request_body_size = 0

                request_body = self.environ['wsgi.input'].read(request_body_size).decode('utf-8')
                data = json.loads(request_body)    
                
                try:
                    date = data['date']
                    target_tz_str = data['target_tz']
                    
                    target_tz = timezone(target_tz_str)
                    current_tz_str = date['tz']   
                    current_date_time_str = date['date']
                    current_date_time = datetime.strptime(current_date_time_str, '%m.%d.%Y %H:%M:%S')
                    target_date_time = current_date_time.astimezone(target_tz)

                    response = target_date_time.strftime(fmt)
                    status = '200 OK'

                except Exception:
                    response = 'Invalid parameters'
                    status = '400 Bad Request'

                self.start(status, response_headers)
                yield bytes(response, 'utf-8')

            # /api/v1/datediff
            elif self.environ['PATH_INFO'] == '/api/v1/datediff':
                try:
                    request_body_size = int(self.environ.get('CONTENT_LENGTH', 0))
                except (ValueError):
                    request_body_size = 0

                request_body = self.environ['wsgi.input'].read(request_body_size).decode('utf-8')
                data = json.loads(request_body)
                
                try:
                    first_date_str = data['first_date']
                    first_tz_str = data['first_tz']
                    second_date_str = data['second_date']
                    second_tz_str = data['second_tz']
                    
                    first_tz = timezone(first_tz_str)
                    first_date_time = datetime.strptime(first_date_str, '%m.%d.%Y %H:%M:%S')
                    first_date_time = first_tz.localize(first_date_time)

                    second_tz = timezone(second_tz_str)
                    second_date_time = datetime.strptime(second_date_str, '%I:%M%p %Y-%m-%d')
                    second_date_time = second_tz.localize(second_date_time)

                    time_diff = abs((second_date_time - first_date_time).total_seconds())

                    response = str(time_diff)
                    status = '200 OK'

                except Exception:
                    response = 'Invalid parameters'
                    status = '400 Bad Request'

                self.start(status, response_headers)
                yield bytes(response, 'utf-8')

            else:
                status = '400 Bad Request'
                self.start(status, response_headers)


with make_server('', 8000, AppClass) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
