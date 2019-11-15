from webapp import create_app
from webapp.python_org_news import get_python_news

app = create_app()
with app.app_context():
    get_python_news()