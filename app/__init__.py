from app.manage import create_app

app, logger = create_app()

from app.resource.pinger import Pinger
from app.resource.sentiment_analysis_app import Dashboard, Index

app['static_root_url'] = '/static'
app.router.add_static(app['static_root_url'], 'app/static/')

app.router.add_view('/', Index, name="index")
app.router.add_view('/dashboard/{time}', Dashboard, name='dashboard')
