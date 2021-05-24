import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"
    #SQLALCHEMY_DATABASE_URI = "postgresql://bm_app_user:bm_app_password@localhost/budgetmonitor"
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+ os.getcwd() +"/budgetmonitor.db"
    DOWNLOADED_STATEMENT = os.path.join('/Users',os.environ['USER'],'Downloads')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 15
    ALLOWED_EXTENSIONS = set(['qif'])
    CHART_1_MONTH_COUNT = 6
    CHART_2_MONTH_COUNT = 12
    CHART_3_MONTH_COUNT = 12
