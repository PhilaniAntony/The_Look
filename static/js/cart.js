const updateBtns = document.getElementsByClassName("update-cart");
const productSizeButtons = document.getElementsByClassName("product-size-variable");
const wishlistBtns = document.getElementsByClassName("add-wishlist");


for (let i = 0; i < wishlistBtns.length; i++) {
  wishlistBtns[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    addUserWishlist(productId)

  });
}

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    let size = this.dataset.size

    if (user === "AnonymousUser") {
      addCookieItem(productId, size);
    } else {
      updateUserOrder(productId, action, size);
    }
  });
}
for (let i = 0; i < productSizeButtons.length; i++) {
  productSizeButtons[i].addEventListener('click', function () {
    let productId = this.dataset.product;
    let size = this.innerText;
    console.log(productId, size)
    addProductSize(productId, size);
  })
}

//Add product size, create a function that loops through all the buttons and 
//looops through them and check for dataset.product , if thats  the same with passed
//id , it will set the dataset.size into right size
function addProductSize(productId, size) {
  Array.from(updateBtns).forEach(function (updateBtn) {
    if (updateBtn.dataset.product = productId) {
      let prodSize = updateBtn.dataset.size
      prodSize = size
      console.log(prodSize)
    }
  })
}


//post the rpoducts to updateview that will save the order in a database
function updateUserOrder(productId, action, size) {
  console.log("User is aunthenticated, send data");

  let url = "/update_item/";
  fetch("/update_item/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action, size: size }),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      location.reload();
    });
}
function addUserWishlist(productId) {
  console.log("User is aunthenticated, send data");


  fetch("/add_wishlist/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId }),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      location.reload();
    });
}

function addCookieItem(productId, action, size) {
  console.log("User not logged in");


  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
      cart[productId] = { size: size }
    } else {
      cart[productId]["quantity"] += 1;
      cart[productId]["size"] = size
    }
  }
  if (action == "remove") {
    cart[productId]["quantity"] -= 1;

    if (cart[productId]["quantity"] <= 0) {
      delete cart[productId];
    }
  }
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

