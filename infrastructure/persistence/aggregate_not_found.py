class AggregateNotFound(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Aggregate not found exception error, {0} '.format(self.message)
        else:
            return 'Aggregate not found exception error'
