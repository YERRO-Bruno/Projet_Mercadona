document.addEventListener("DOMContentLoaded", function () {
    alert("admin2")
    const categoryFilter = document.getElementById("category-filter");
    const productList = document.getElementById("product-list");
    //Checkbox 'que les promotions'
    const promochek = document.getElementById("sel-promo");
    // liste categorie du bloc  administration produit
    const currentCategory = document.getElementById("id_category");
    const imgcour = document.getElementById("currentimg")
    const productlist = document.getElementById("product-list")
    const picturelist = document.getElementById("picture-list")
    const productCatalog = document.getElementById("id_catalog_products")
    const pictureCatalog = document.getElementById("id_catalog_pictures")
    const picturesearch = document.getElementById("picture_search")
    const picturesearchbutton = document.getElementById("picture_search_button")
    const cancelpicturesearchbutton = document.getElementById("cancel_picture_search_button")

    document.getElementById("id_description").value=desc
    pictureCatalog.style.display = "none"
    productCatalog.style.display = "none"
    if (imgcur !== "" ) {
        fillcurrentpicture(imgcur)
    }

// remplissage du selecteur de categorie du formulaire
    fillcurrentCategories().then(r => {
        // Gestion de l'absence de categories par l'ajout d'une categorie fictive
        if (currentCategory.options.length === 0) {
            alert("Il n'y a aucun categorie. Vous devez créer une catégorie!");
            const option = document.createElement("option");
            option.textContent = "Categorie fictive";
            currentCategory.appendChild(option);
            document.getElementById("button_addprod").disabled = true;
            document.getElementById("button_updprod").disabled = true;
            document.getElementById("button_delprod").disabled = true;
            document.getElementById("button_updcat").disabled = true;
            document.getElementById("button_delcat").disabled = true;

        }
        currentCategory.selectedIndex = 0
     })

    //remplissage catalogue picrures (imagkit)
   fillpictures()
// affichage catalogue produits
    productCatalog.style.display = ""

    //ecoute clic sur selecteur category (dans le cadre administration)
    document.getElementById("id_category").addEventListener("change", function (e) {
        document.getElementById("id_updcat").value = currentCategory.value
        document.getElementById("id_delcat").textContent = currentCategory.value

    })
//mise a jour selecteur cetegoty zone administration

//    écoute evenement clic sur un produit
    const gallery = document.getElementById("product-list");
    gallery.addEventListener("click", function (event) {
        var imgfils = (document.getElementById("currentimg"))
        if (imgfils) {
            imgfils.remove()
        }
        const currentproduct = document.getElementById("currentproduct")
        const tabid = []
        idClicked = event.target
        tabid.push(idClicked.id)
        idClicked1 = idClicked.parentNode
        tabid.push(idClicked1.id)
        idClicked2 = idClicked1.parentNode
        tabid.push(idClicked2.id)
        idClicked3 = idClicked2.parentNode
        tabid.push(idClicked3.id)
        idClicked4 = idClicked3.parentNode
        tabid.push(idClicked4.id)
        idClicked5 = idClicked4.parentNode
        tabid.push(idClicked5.id)
        idClicked6 = idClicked5.parentNode
        tabid.push(idClicked6.id)
        tabelement = [idClicked, idClicked1, idClicked2, idClicked3, idClicked4, idClicked5, idClicked6]
        //recherche id de l'element avec l'id XXXXXXX dont le parent a comme id product.id
        for (var i = 0; i < 7; i++) {
            if (tabid[i] == "XXXXXXX") {
                id_prod = tabelement[i].parentNode.id
            }
        }
        fillcurrentproduct(id_prod)

    })


        // ecoute clic sur le bouton 'Choisir image' : efface le catalogue produits et affiche le catalogue photos
    btnimg = document.getElementById("imageInput");
    btnimg.addEventListener("click", function (e) {
        e.preventDefault()
        productCatalog.style.display = "none"
        pictureCatalog.style.display = ""
    })

    // ecoute clic sur une photo du catalogue : affiche la photo dans le cadre suppérieur
    // efface le catalog photos et affiche le catalogue produits
    document.getElementById("picture-list").addEventListener("click", function (e) {
        e.preventDefault()
        var imgfils = (document.getElementById("currentimg"))
        if (imgfils) {
            imgfils.remove()
        }
        fillcurrentpicture(e.target.getAttribute("value"))
        productCatalog.style.display = ""
        pictureCatalog.style.display = "none"
    })

//     // ecoute clic sur le bouton 'Effacer les champs"
    document.getElementById("btnraz").addEventListener("click", function (e) {
        e.preventDefault();
        document.getElementById("id_prodid").value = "0"
        document.getElementById("id_fileimage").value = null
        document.getElementById("id_label").value = null
        document.getElementById("id_description").value = null
        document.getElementById("id_category").value = null
        document.getElementById("id_price").value = null
        document.getElementById("id_price_reduc").value = null
        document.getElementById("id_promo").value = null
        document.getElementById("id_begin").value = null
        document.getElementById("id_end").value = null
        document.getElementById("currentimg").remove()
        // document.getElementById("id_label").value = null
    })

    //pour la page administration ecoute click sur champ recherche et annule recherche (X) catalogue photos
    picturesearchbutton.addEventListener('click', function () {
        fillpictures()
        })
    cancelpicturesearchbutton.addEventListener('click', function () {
         picturesearch.value = "";
         fillpictures()

        })
    //ecoute clic sur lien fermeture catalogue photos
    closephotosbutton = document.getElementById("closephotos")
    closephotosbutton.addEventListener('click', function () {
        productCatalog.style.display = ""
        pictureCatalog.style.display = "none"
    })

    //ecoute clic bouton Ajouter un produit
    addproductbutton.document.getElementById("button_addprod")
    addproductbutton.addEventListener("click", function (e) {
        document.getElementById("id_prodid").value = "0"
    })



    cancelcategorybutton = document.getElementById("button_delcat")
    cancelcategorybutton.addEventListener('click', function (e) {
        deletecategory = document.getElementById("id_delcat")
        e.preventDefault()
        // async function searchnumberproductpercategory (deletecategory, e) {
        fetch('/mercadona/api/products/')
            .then(response => response.json())
            .then(data => {
                var res = 0
                i=0
                for (prod in data) {
                    if (data[i]["category"]["label"] === deletecategory.innerHTML) {
                        res++
                    }
                    i++
                }
                if (res>0) {
                    if (confirm("voulez-vous supprimer la catégorie qui est peux-être liée à des produits?")) {
                        document.getElementById("buttonValue").name = "BTN";
                        e.target.form.submit();
                    }
                } else {
                    document.getElementById("buttonValue").name = "BTN";
                    e.target.form.submit();
                }
            })
    })

//     // FUNCTIONS
//
//     // renseigne les options du Sélécteur de catégorie du formulaire
    async function fillcurrentCategories() {
        await $.ajax({
            url: '/mercadona/api/categories',
            method: "GET",
            dataType: "json",
            success: function (data) {
                var i = 0;
                data.forEach(category => {
                    const option = document.createElement("option");
                    option.value = data[i].label
                    option.textContent = data[i].label;
                    currentCategory.appendChild(option);
                    i++
                });
            },
            error: function (xhr, status, error) {
                console.error("Problème de récupération des catégories :", xhr, status, error);
            }
        });
        document.getElementById("id_updcat").value = currentCategory.value
        document.getElementById("id_delcat").textContent = currentCategory.value
    }

    //recuperation du produit cliqué et traitement des champs de formulaire
    function fillcurrentproduct(idprod) {
        $.ajax({
            url: `/mercadona/api/products/${idprod}`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                let product = data
                document.getElementById("id_prodid").value = product.id
                fillcurrentpicture(product.picture_file)
                document.getElementById("id_fileimage").value = product.picture_file
                document.getElementById("id_label").value = product.product_label
                document.getElementById("id_description").value = product.description
                document.getElementById("id_category").value = product.category.label
                document.getElementById("id_updcat").value = product.category.label
                document.getElementById("id_delcat").textContent = product.category.label
                document.getElementById("id_price").value = product.price
                document.getElementById("id_promo").value = product.reduction
                document.getElementById("id_begin").value = product.begin_promo
                document.getElementById("id_end").value = product.end_promo
                document.getElementById("imageInput").value = product.image
                if (product.reduction === 0.00) {
                    document.getElementById("id_price_reduc").value = product.price
                } else {
                    document.getElementById("id_price_reduc").value =
                        Math.round(product.price * (1 - product.reduction / 100) * 100) / 100
                }
            },
            error: function (error) {
                console.error("Erreur lors de la récupération des produits :", error);
            }
        })
    }

    // affichage des images imagekitio (démasquées pour choisir image
    function fillpictures () {
        const divpicture = document.querySelectorAll(".divpicture")
        divpicture.forEach(function (ind) {
            ind.remove()
        })
        $.ajax({
            url: `/mercadona/api/pictures`,
            method: "GET",
            dataType: "json",
            success: function (data) {
                var keys = Object.keys(data)
                for (i = 0; i < keys.length; i++) {
                    rech = data[keys[i]]
                    if (rech.startsWith(picturesearch.value)) {
                        key = `img'+${i}`
                        var imghtml = `
                            <div class="divpicture col-1">
                                <p style="height: 1vh">${data[keys[i]].split(".")[0]}</p>
                                <img class="imgagekit mt-0" id="id_imagekit" value="${data[keys[i]]}"
                                src="https://ik.imagekit.io/kpvotazbj/${data[keys[i]]}" style="height: 20vh">
                            </div>
                        `
                        $(".imagekit").append(imghtml)
                    }
                }
            },
            error: function (error) {
                console.error("Erreur lors de la récupération des produits :", error);
            }
        })
    }


    function fillcurrentpicture(picture) {
        document.getElementById("id_fileimage").value = picture
        var imghtml = `
            <img class="imgproduct" id="currentimg" style="height: 25vh" 
            src="https://ik.imagekit.io/kpvotazbj/${picture}">
        `;
        imgnew = $(".imgcour").append(imghtml)
    }

    currentCategory.value = currentcateg

})
