
class ShortIdToLowerCaseMixin:  # pylint: disable=too-few-public-methods
    def save(self, *args, **kwargs):
        self.short_id = self.short_id.lower()
        super().save(*args, **kwargs)
