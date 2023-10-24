from django.test import TestCase
from mercadona.models import Product, Category
from datetime import date


class ProductModelTest(TestCase):

    def setUp(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price=95.95)['obj']

    def test_create_product(self):
        # self.assertEqual(self.product.product_label, "Product")self.assertEqual(self.product.product_label, "Product")
        self.assertIsNotNone(self.product)

    def test_create_product_empty_product_label(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="", description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_product_label(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label=None, description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_empty_description(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="",
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_none_description(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description=None,
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_empty_category(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id="", picture_file="Picture",
                                              reduction=0, price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_category(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=None, picture_file="Picture",
                                              reduction=0, price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_price(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price=None)['obj']
        self.assertIsNone(self.product)

    def test_create_product_Empty_price(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              reduction=0, price="")['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_reduction(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              price=95.95)['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.reduction, 0)

    def test_create_product_empty_reduction(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture", reduction="",
                                              price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_not_decimal_reduction(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture", reduction="ABC",
                                              price=95.95)['obj']
        self.assertIsNone(self.product)

    def test_create_product_not_date_begin_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture", reduction="0",
                                              price=95.95, begin_promo="AAAAAA")['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.begin_promo, date(2000, 12, 25))

    def test_create_product_None_begin_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture", reduction="0",
                                              price=95.95, begin_promo=None)['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.begin_promo, date(2000, 12, 25))

    def test_create_product_not_date_end_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture", reduction="0",
                                              price=95.95, end_promo="AAAAAA")['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.end_promo, date(2000, 12, 25))

    def test_create_product_None_end_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_id=category.id, picture_file="Picture", reduction="0",
                                              price=95.95, end_promo=None)['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.end_promo, date(2000, 12, 25))

    def test_create_product_default_values(self):
        category = Category()
        category.label = "test"
        category.save()
        self.product = Product.create_product(Product(), product_label="product", description="Description",
                                              category_id=category.id, picture_file="Picture",
                                              price=95.95)['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.reduction, 0)
        self.assertEqual(self.product.begin_promo, date(2000, 12, 25))
        self.assertEqual(self.product.end_promo, date(2000, 12, 25))

    def test_update_product(self):
        category = Category()
        category.label = "test"
        category.save()
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="newProduct",
                                                      description="newDescription", category=newcategory,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertEqual(self.product_updated.product_label, "newProduct")
        self.assertEqual(self.product_updated.description, "newDescription")
        self.assertEqual(self.product_updated.category, newcategory)
        self.assertEqual(self.product_updated.picture_file, "newPicture")
        self.assertEqual(self.product_updated.reduction, 5)
        self.assertEqual(self.product_updated.price, 55)
        self.assertEqual(self.product_updated.begin_promo, begin)
        self.assertEqual(self.product_updated.end_promo, end)

    def test_update_product_None_product_id(self):
        category = Category()
        category.label = "test"
        category.save()
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=None, product_label="newProduct",
                                                      description="newDescription", category=newcategory,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_inexistant_product_id(self):
        category = Category()
        category.label = "test"
        category.save()
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=654321, product_label="newProduct",
                                                      description="newDescription", category=newcategory,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_product_label(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label=None,
                                                      description="newDescription", category=category,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_description(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description=None, category=category,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_category(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description=None, category=None,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_inexistant_description(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description=None, category=12345,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_picture_file(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file=None, reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_price(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=5, price=None,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_Not_decimal_price(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=5, price="AAAA",
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_reduction(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=None, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_Not_decimal_reduction(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction="AA", price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_default_begin_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      end_promo=end)['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.begin_promo, begin)

    def test_update_product_Not_date_begin_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo="AAA", end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_default_end_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=end)['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.end_promo, end)

    def test_update_product_Not_date_end_promo(self):
        category = Category()
        category.label = "test"
        category.save()
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category=category,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo="AAA")['obj']
        self.assertIsNone(self.product_updated)

    def test_delete_product(self):
        is_delete = Product.delete_product(self=Product(), product_id=self.product.id)['obj']
        self.assertTrue(is_delete)

    def test_delete_product_inexistante(self):
        is_deleted = Product.delete_product(self=Product(), product_id=12345)['obj']
        self.assertFalse(is_deleted)
