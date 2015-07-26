# coding=utf-8

class MasterSlaveRouter(object):
    """
    master slave router
    by:尚宗凯 at：2015-04-28
    """
    def db_for_read(self, model, **hints):
        """
        Reads always go to the slave.
        """
        return "slave"

    def db_for_write(self, model, **hints):
        """
        Writes always go to master.
        """
        return 'master'

    def allow_syncdb(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True