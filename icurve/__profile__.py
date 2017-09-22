# -*- coding: utf-8 -*-
from icurve import create_app
from werkzeug.contrib.profiler import ProfilerMiddleware

if __name__ == '__main__':
    app = create_app()
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
