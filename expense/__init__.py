import os 

from flask import Flask

test_config = None 
app = Flask(__name__, instance_relative_config = True)
app.config.from_mapping(
    SECRET_KEY='dev', 
    DATABASE=os.path.join(app.instance_path, 'expense.sqlite'),
)

if test_config is None: 
    app.config.from_pyfile('config.py', silent=True)
else: 
    app.config.from_mapping(test_config)

try: 
    os.makedirs(app.instance_path)
except OSError: 
    pass

from . import db
db.init_app(app)

from . import auth 
from . import record 

app.register_blueprint(auth.bp)
app.register_blueprint(record.bp)

app.add_url_rule('/personal', endpoint='personal')


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
