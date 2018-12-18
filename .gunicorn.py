from config.json import Config

cfg = Config(section='app')

bind = f"{cfg.get('start_host', '127.0.0.1')}:{cfg.get('start_port', 5000)}"
if isinstance(cfg.get("gunicorn"), dict):
    locals().update(cfg.get("gunicorn"))

if __name__ == '__main__':
    print(locals())
