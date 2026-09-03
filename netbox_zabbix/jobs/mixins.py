class JobInstanceMixin:
    """
    Mixin for JobInstance models.
    """

    def get_instance(self):
        """
        Return the Job instance.
        """
        if hasattr(self, 'job') and hasattr(self.job, 'object') and self.job.object:
            return self.job.object
        return None
