from django.test import TestCase
from mercadona.models import Product, Category
from datetime import date


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category()
        self.category.label = "test"
        self.category.save()
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              price=95.95, reduction=0, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']

    def test_create_product(self):
        self.assertIsNotNone(self.product)

    def test_create_product_empty_product_label(self):
        self.product = Product.create_product(Product(), product_label="", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              price=95.95, reduction=0, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_product_label(self):
        self.product = Product.create_product(Product(), product_label=None, description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              price=95.95, reduction=0, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_empty_picture_file(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="",
                                              price=95.95, reduction=0, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_picture_file(self):
        self.product = Product.create_product(Product(), product_label="product", description="Description",
                                              category_label=self.category.label, picture_file=None,
                                              price=95.95, reduction=0, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_empty_description(self):
        self.product = Product.create_product(Product(), product_label="Product", description="",
                                              category_label=self.category.label, picture_file="Picture",
                                              reduction=0, price=95.95, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_none_description(self):
        self.product = Product.create_product(Product(), product_label="Product", description=None,
                                              category_label=self.category.label, picture_file="Picture",
                                              reduction=0, price=95.95, begin_promo=date(2023, 10, 30),
                                                  end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_empty_category(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label="", picture_file="Picture",
                                              reduction=0, price=95.95, begin_promo=date(2023, 10, 30),
                                                  end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_category(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=None, picture_file="Picture",
                                              reduction=0, price=95.95, begin_promo=date(2023, 10, 30),
                                                  end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_price(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              reduction=0, price=None, begin_promo=date(2023, 10, 30),
                                                  end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_Empty_price(self):
         self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              reduction=0, price="", begin_promo=date(2023, 10, 30),
                                                       end_promo=date(2023, 10, 30))['obj']
         self.assertIsNone(self.product)

    def test_create_product_not_numeric_price(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              reduction=0, price="ABCD", begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_reduction(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              price=95.95, reduction=None, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.reduction, 0)

    def test_create_product_empty_reduction(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture", reduction="",
                                              price=95.95, begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.reduction, 0)

    def test_create_product_not_numeric_reduction(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture",
                                              price=95.95, reduction="ABCD", begin_promo=date(2023, 10, 30),
                                              end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_not_date_begin_promo(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture", reduction="0",
                                              price=95.95, begin_promo="AAAAAA", end_promo=date(2023, 10, 30))['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_begin_promo(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture", reduction="0",
                                              price=95.95, begin_promo=None, end_promo=date(2023, 10, 30))['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.begin_promo, date(2000, 12, 25))

    def test_create_product_not_date_end_promo(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture", reduction="0",
                                              price=95.95, begin_promo=date(2023, 10, 30), end_promo="AAAAAA")['obj']
        self.assertIsNone(self.product)

    def test_create_product_None_end_promo(self):
        self.product = Product.create_product(Product(), product_label="Product", description="Description",
                                              category_label=self.category.label, picture_file="Picture", reduction="0",
                                              price=95.95, begin_promo=date(2023, 10, 30), end_promo=None)['obj']
        self.assertIsNotNone(self.product)
        self.assertEqual(self.product.end_promo, date(2000, 12, 25))

    def test_update_product(self):
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="newProduct",
                                                      description="newDescription", category_label=newcategory.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertEqual(self.product_updated.product_label, "newProduct")
        self.assertEqual(self.product_updated.description, "newDescription")
        self.assertEqual(self.product_updated.category, newcategory)
        self.assertEqual(self.product_updated.picture_file, "newPicture")
        self.assertEqual(self.product_updated.reduction, 5)
        self.assertEqual(self.product_updated.price, 55)
        self.assertEqual(self.product_updated.begin_promo, date(2010, 10, 10))
        self.assertEqual(self.product_updated.end_promo, date(2011, 11, 11))

    def test_update_product_None_product_id(self):
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=None, product_label="newProduct",
                                                      description="newDescription", category_label=newcategory.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_Empty_product_id(self):
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id="", product_label="newProduct",
                                                      description="newDescription", category_label=newcategory.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_inexistant_product_id(self):
        newcategory = Category()
        newcategory.label = "test2"
        newcategory.save()
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=654321, product_label="newProduct",
                                                      description="newDescription", category_label=newcategory.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_product_label(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label=None,
                                                      description="newDescription", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_empty_product_label(self):
            begin = date(2010, 10, 10)
            end = date(2011, 11, 11)
            self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="",
                                                          description="newDescription", category_label=self.category.label,
                                                          picture_file="newPicture", reduction=5, price=55,
                                                          begin_promo=begin, end_promo=end)['obj']
            self.assertIsNone(self.product_updated)

    def test_update_product_None_description(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description=None, category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_empty_description(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_category(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="newDescription", category_label=None,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_empty_category(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="newDescription", category_label="",
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_inexistant_category(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="newDescription", category_label=12345,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_picture_file(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file=None, reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_empty_picture_file(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_price(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=None,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_empty_price(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price="",
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_Not_decimal_price(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price="AAAA",
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_reduction(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=None, price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertEqual(self.product_updated.reduction, 0)

    def test_update_product_empty_reduction(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction="", price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertEqual(self.product_updated.reduction, 0)

    def test_update_product_Not_decimal_reduction(self):
        begin = date(2010, 10, 10)
        end = date(2011, 11, 11)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction="ABCD", price=55,
                                                      begin_promo=begin, end_promo=end)['obj']
        self.assertIsNone(self.product_updated)

    def test_update_product_None_begin_promo(self):
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55, begin_promo=None,
                                                      end_promo=end)['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.begin_promo, begin)

    def test_update_product_empty_begin_promo(self):
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55, begin_promo="",
                                                      end_promo=end)['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.begin_promo, begin)

    def test_update_product_not_date_begin_promo(self):
       end = date(2000, 12, 25)
       self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo="AAA", end_promo=end)['obj']
       self.assertIsNotNone(self.product_updated)
       self.assertEqual(self.product_updated.begin_promo, date(2000, 12, 25))

    def test_update_product_None_date_end_promo(self):
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=None)['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.end_promo, end)

    def test_update_product_empty_date_end_promo(self):
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo=None)['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.end_promo, end)


    def test_update_product_Not_date_end_promo(self):
        begin = date(2000, 12, 25)
        end = date(2000, 12, 25)
        self.product_updated = Product.update_product(Product(), product_id=self.product.id, product_label="Product",
                                                      description="Description", category_label=self.category.label,
                                                      picture_file="newPicture", reduction=5, price=55,
                                                      begin_promo=begin, end_promo="AAA")['obj']
        self.assertIsNotNone(self.product_updated)
        self.assertEqual(self.product_updated.end_promo, end)

    def test_delete_product(self):
        is_delete = Product.delete_product(self=Product(), product_id=self.product.id)['obj']
        self.assertTrue(is_delete)

    def test_delete_product_id_inexistante(self):
        is_deleted = Product.delete_product(self=Product(), product_id=12345)['obj']
        self.assertFalse(is_deleted)

    def test_delete_product_id_empty(self):
        is_deleted = Product.delete_product(self=Product(), product_id="")['obj']
        self.assertFalse(is_deleted)

    def test_delete_product_id_None(self):
        is_deleted = Product.delete_product(self=Product(), product_id=None)['obj']
        self.assertFalse(is_deleted)
