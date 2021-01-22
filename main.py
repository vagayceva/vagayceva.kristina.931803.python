from datetime import datetime
from pytz import timezone, UnknownTimeZoneError
from paste import reloader
from paste.httpserver import serve
from tzlocal import get_localzone
import json


def time_server(environ, start_response):

    if environ['REQUEST_METHOD'] == 'GET':
        define = environ['PATH_INFO'][1:]
        if not define:
            text = 'Time - '
            define = None
        else:
            try:
                define = timezone(define)
                text = 'Time in %s - ' % define
            except UnknownTimeZoneError:
                start_response('200 OK', [('Content-Type', 'text/plain')])
                return [b'Error: Unknown time zone']

        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [bytes(text + datetime.now(define).strftime('%H:%M:%S'), encoding='utf-8')]

    elif environ['REQUEST_METHOD'] == 'POST':
        data = environ['wsgi.input'].read().decode("utf-8")
        data = json.loads(data)
        try:
            timezone1 = timezone(data['tz_start'])
        except KeyError:
            timezone1 = get_localzone()
        try:
            timezone2 = timezone(data['tz_end'])
        except KeyError:
            timezone2 = get_localzone()
        try:
            type = data['type']
        except:
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes('Error in type Data', encoding='utf-8')]
        time_now = datetime.now(timezone1)
        tz1 = datetime.now(timezone1).utcoffset()
        tz2 = datetime.now(timezone2).utcoffset()
        if tz1 < tz2:
            diff = tz2 - tz1
        else:
            diff = '-' + str(tz1 - tz2)
        diff = str(diff)
        if data['type'] == 'time':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'time': datetime.now(timezone1).strftime('%H:%M:%S'), 'timezone': str(timezone1)}), encoding='utf-8')]
        elif data['type'] == 'date':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'date': datetime.now(timezone1).strftime('%d.%m.%Y'), 'timezone': str(timezone1)}), encoding='utf-8')]
        elif data['type'] == 'datediff':
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return [bytes(json.dumps({'time_diff': diff, 'timezone1': str(timezone1), 'timezone2': str(timezone2)}),
                          encoding='utf-8')]


if __name__ == '__main__':

    reloader.install()
    serve(time_server)