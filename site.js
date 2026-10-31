"use strict";

// Set this ONE value to the final HTTPS checkout URL to enable both languages.
const PURCHASE_URL = "";
const SELLER_NAME = "LK REALTY CONSULTING INC.";
const CONTACT_EMAIL = "woowachart@gmail.com";
const PAYMENT_PROVIDER_NAME = "";

document.querySelectorAll("[data-seller-name]").forEach((element) => {
  element.textContent = SELLER_NAME;
});
document.querySelectorAll("[data-contact-email]").forEach((element) => {
  element.textContent = CONTACT_EMAIL;
  if (element.tagName === "A") element.href = "mailto:" + CONTACT_EMAIL;
});
if (PAYMENT_PROVIDER_NAME) {
  document.querySelectorAll("[data-payment-provider]").forEach((element) => {
    element.textContent = PAYMENT_PROVIDER_NAME;
  });
}

if (PURCHASE_URL.startsWith("https://")) {
  document.querySelectorAll("[data-purchase]").forEach((link) => {
    link.href = PURCHASE_URL;
    link.removeAttribute("aria-disabled");
    link.removeAttribute("tabindex");
    link.textContent = link.dataset.readyLabel;
  });
  document.querySelectorAll("[data-purchase-pending]").forEach((note) => {
    note.hidden = true;
  });
}

// Keep the poster and a useful message if an encoding has not arrived yet.
document.querySelectorAll("video").forEach((video) => {
  const showError = () => {
    const message = document.getElementById(video.dataset.errorId);
    if (message) message.hidden = false;
  };
  video.addEventListener("error", showError);
  if (video.error) showError();
});
