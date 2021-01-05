class OptimisticLockException(Exception):
    def __init__(self):
        super(OptimisticLockException, self).__init__()
