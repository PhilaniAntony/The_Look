var updateBtns = document.getElementsByClassName("update-cart");
var viewDetails = document.getElementsByClassName("view-details");
for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;

    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}
for (var i = 0; i < viewDetails.length; i++) {
  viewDetails[i].addEventListener("click", function () {
    var productName = this.dataset.product;
    var productPrice = this.dataset.price;
    var productImage = this.dataset.image;
    var modalHeader = document.querySelector(".modal-header");
    var modalBody = document.querySelector(".modal-body");

    // Create Modal Title
    var modalTitle = document.createElement("h5");
    modalTitle.classList = "product-name modal-title";
    modalTitle.innerHTML = `<strong> ${productName} </strong>`;
    //Create Close button
    var closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.className = "close";
    closeButton.dataset.dismiss = "modal";
    closeButton.innerHTML = '<span aria-hidden="true">&times;</span>';
    // Create Product image
    var modalImage = document.createElement("img");
    modalImage.src = productImage;
    modalImage.classList = "thumbnail product-image";
    //Create product price
    var modalPrice = document.createElement("h5");
    modalPrice.className = "modal-price";
    modalPrice.textContent = productPrice;
    console.log(productName);
    //Append the element to the modal
    modalHeader.appendChild(modalTitle);
    modalHeader.appendChild(closeButton);
    modalBody.appendChild(modalImage);
    modalBody.appendChild(modalPrice);

    //Clear the conent when close button is clicked
    closeButton.addEventListener("click", function () {
      //Reset Content modal content
      modalTitle.innerHTML = "";
      modalImage.src = "";
      modalPrice.textContent = "";
    });
  });
}

function updateUserOrder(productId, action) {
  console.log("User is aunthenticated, send data");

  var url = "/update_item/";
  fetch("/update_item/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      location.reload();
    });
}
function addCookieItem(productId, action) {
  console.log("User not logged in");

  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
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
