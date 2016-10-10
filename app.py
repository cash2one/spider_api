# # -*- coding: utf-8 -*-
from app_spider import app


if __name__ == "__main__":
    import argparse
    from gevent import monkey

    def app_argsparse():
        parser = argparse.ArgumentParser(description=u'服务参数配置')
        parser.add_argument("-p", "--port", help=u"服务端口", type=int, default="8080")
        parser.add_argument("-d", "--domain", help=u"the domain host", type=str, default="0.0.0.0")
        args = parser.parse_args()
        return args

    def run(args):
        if app.config.get("DEBUG"):
            # it's only for development
            from flask import render_template
            @app.route('/')
            def index():
                return render_template('vds-mock.html')
        host, port = args.domain, args.port
        # socketio.run(app) runs a production ready server when eventlet or gevent are installed,
        # so gevent WSGIServer is not in use now
        monkey.patch_all()
        app.run(host, port, debug=True, threaded=True)

    run(app_argsparse())
