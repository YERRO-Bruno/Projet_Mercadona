# from django.db import models
# from django.db.utils import DatabaseError
#
# class CategoryManager(models.Manager):
#     def create_category(self, label):
#         category = self.model(label=label)
#         try:
#             category.save()
#             return category
#         except DatabaseError:
#             return None
#
#     def update_category(self, category_id, new_label):
#         try:
#             category = self.get(id=category_id)
#             if category:
#                 category.label = new_label
#                 category.save()
#                 return category
#         except (Category.DoesNotExist, DatabaseError):
#             return None
#
#     def delete_category(self, category_id):
#         try:
#             category = self.get(id=category_id)
#             if category:
#                 category.delete()
#                 return True
#         except (Category.DoesNotExist, DatabaseError):
#             return False