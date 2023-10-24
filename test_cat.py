from .models import Category

def main():
    category = Category.create_category(label="Tee-shirt")
    if category:
        print("succes")
    else:
        print("echec")

if __name__ == "__main__":
    main()