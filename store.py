# My module
class store:
  app = {}
  db = {}
  login_manager = {}

  @staticmethod
  def store_app(application):
    store.app = application

  @staticmethod
  def store_db(database):
    store.db = database

  @staticmethod
  def store_login_manager(login_manager_object):
    store.login_manager = login_manager_object
