
class ShortIdToLowerCaseMixin:
    def save(self, *args, **kwargs):
        self.short_id = self.short_id.lower()
        super().save(*args, **kwargs)