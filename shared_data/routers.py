class SharedDataRouter(object):

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'shared_data':
            return 'shared_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Point all operations on myapp models to 'other'
        """
        if model._meta.app_label == 'shared_data':
            return 'shared_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        return None

    def allow_migrate(self, db, app_label, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'shared_data':
            return db == 'shared_db'
        return db == 'default'