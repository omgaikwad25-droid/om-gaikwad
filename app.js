const cart = new Map();
const productData = {};
document.querySelectorAll(".product-card").forEach(card => {
  const button = card.querySelector(".add-button");
  const id = Number(button.dataset.id);
  const name = card.querySelector("h3").textContent;
  const priceText = card.querySelector(".price").textContent;
  const price = Number(priceText.replace(/[^\d.]/g, ""));
  const unit = priceText.split("/")[1]?.trim() || "unit";
  const icon = card.querySelector(".product-art").textContent.trim();
  productData[id] = { id, name, price, unit, icon };
  button.addEventListener("click", () => {
    const existing = cart.get(id);
    cart.set(id, { ...productData[id], quantity: existing ? existing.quantity + 1 : 1 });
    renderCart();
    document.getElementById("cart").scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
});

function renderCart() {
  const container = document.getElementById("cart-items");
  const items = [...cart.values()];
  const count = items.reduce((sum, item) => sum + item.quantity, 0);
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  document.getElementById("cart-count").textContent = count;
  document.getElementById("cart-total").textContent = total.toFixed(2);
  document.getElementById("checkout-items").value = JSON.stringify(items.map(({ id, quantity }) => ({ id, quantity })));
  document.getElementById("checkout-total").value = total.toFixed(2);

  if (!items.length) {
    container.innerHTML = '<p class="empty-state">Your cart is empty. Add a fresh pick to get started.</p>';
    return;
  }

  container.innerHTML = items.map(item => `
    <div class="cart-row">
      <div><h4>${item.icon} ${escapeHtml(item.name)}</h4>
      <p>₹${item.price.toFixed(2)} / ${escapeHtml(item.unit)} · ₹${(item.price * item.quantity).toFixed(2)}</p></div>
      <div class="quantity">
        <button type="button" aria-label="Decrease quantity" data-action="minus" data-id="${item.id}">−</button>
        <strong>${item.quantity}</strong>
        <button type="button" aria-label="Increase quantity" data-action="plus" data-id="${item.id}">+</button>
      </div>
      <button class="remove" type="button" data-action="remove" data-id="${item.id}">Remove</button>
    </div>`).join("");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[ch]));
}

document.getElementById("cart-items").addEventListener("click", event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const id = Number(button.dataset.id);
  const item = cart.get(id);
  if (!item) return;
  if (button.dataset.action === "plus") item.quantity++;
  if (button.dataset.action === "minus") item.quantity--;
  if (button.dataset.action === "remove" || item.quantity <= 0) cart.delete(id);
  else cart.set(id, item);
  renderCart();
});

const search = document.getElementById("search");
let activeCategory = "All";
function filterProducts() {
  const query = search.value.trim().toLowerCase();
  let visible = 0;
  document.querySelectorAll(".product-card").forEach(card => {
    const matchesText = card.dataset.name.includes(query);
    const matchesCategory = activeCategory === "All" || card.dataset.category === activeCategory;
    card.hidden = !(matchesText && matchesCategory);
    if (!card.hidden) visible++;
  });
  document.getElementById("no-results").hidden = visible !== 0;
}
search.addEventListener("input", filterProducts);
document.querySelectorAll(".filter").forEach(button => {
  button.addEventListener("click", () => {
    activeCategory = button.dataset.category;
    document.querySelectorAll(".filter").forEach(b => b.classList.toggle("active", b === button));
    filterProducts();
  });
});

document.getElementById("checkout-form").addEventListener("submit", event => {
  if (cart.size === 0) {
    event.preventDefault();
    alert("Please add at least one product before placing an order.");
  }
});
renderCart();
