/* Ateliê Bruma | loja demonstrativa (DEV-002) | marca FICTÍCIA
   Menu e sacola em gaveta, carrossel com setas e bullets, filtro por categoria e sacola local.
   Sem JavaScript o conteúdo continua acessível: vitrines rolam na horizontal e as âncoras funcionam. */
(function () {
  "use strict";

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var FRETE = window.BRUMA_FRETE_GRATIS || 299;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function brl(v) {
    var s = v.toFixed(2).split(".");
    var int = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return "R$ " + int + (s[1] === "00" ? "" : "," + s[1]);
  }

  /* ---------- Header: linha fina depois de rolar ---------- */
  var header = $("[data-header]");
  var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Gavetas (menu e sacola) ---------- */
  var openDrawer = null;
  var lastFocus = null;
  var FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

  function setExpanded(drawer, value) {
    $$('[aria-controls="' + drawer.id + '"]').forEach(function (b) { b.setAttribute("aria-expanded", String(value)); });
  }

  function open(drawer) {
    var t = document.querySelector("[data-toast]");
    if (t) t.classList.remove("is-on");
    if (openDrawer && openDrawer !== drawer) close(openDrawer, true);
    lastFocus = document.activeElement;
    drawer.hidden = false;
    document.body.classList.add("is-locked");
    setExpanded(drawer, true);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { drawer.classList.add("is-open"); });
    });
    openDrawer = drawer;
    var first = $(FOCUSABLE, $(".drawer__panel", drawer));
    if (first) first.focus({ preventScroll: true });
  }

  function close(drawer, silent) {
    drawer.classList.remove("is-open");
    setExpanded(drawer, false);
    document.body.classList.remove("is-locked");
    openDrawer = null;
    var done = function () { if (!drawer.classList.contains("is-open")) drawer.hidden = true; };
    if (reduceMotion) done(); else setTimeout(done, 300);
    if (!silent && lastFocus && document.contains(lastFocus)) lastFocus.focus({ preventScroll: true });
  }

  $$("[data-drawer]").forEach(function (drawer) {
    drawer.addEventListener("click", function (e) {
      var t = e.target.closest("[data-close], a[href^='#']");
      if (t) close(drawer, t.matches("a"));
    });
  });

  document.addEventListener("keydown", function (e) {
    if (!openDrawer) return;
    if (e.key === "Escape") { close(openDrawer); return; }
    if (e.key !== "Tab") return;
    var items = $$(FOCUSABLE, $(".drawer__panel", openDrawer)).filter(function (el) { return el.offsetParent !== null; });
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  var menu = $("#menu");
  var cartDrawer = $("#sacola");
  $$("[data-open-menu]").forEach(function (b) { b.addEventListener("click", function () { open(menu); }); });
  $$("[data-open-cart]").forEach(function (b) { b.addEventListener("click", function () { open(cartDrawer); }); });
  window.matchMedia("(min-width: 1024px)").addEventListener("change", function (mq) {
    if (mq.matches && openDrawer === menu) close(menu, true);
  });

  /* ---------- Carrossel ---------- */
  var carousels = $$("[data-carousel]").map(function (root) {
    var track = $(".carousel__track", root);
    var nav = $(".carousel__nav", root);
    var prev = $('[data-dir="-1"]', root);
    var next = $('[data-dir="1"]', root);
    var dotsBox = $(".carousel__dots", root);
    var state = { perPage: 1, pages: 1, step: 0 };

    function items() { return $$(":scope > li:not([hidden])", track); }

    function measure() {
      var list = items();
      if (!list.length) return;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      var w = list[0].getBoundingClientRect().width;
      var view = track.clientWidth - (parseFloat(getComputedStyle(track).paddingRight) || 0);
      state.perPage = Math.max(1, Math.floor((view + gap + 1) / (w + gap)));
      state.step = state.perPage * (w + gap);
      state.pages = Math.max(1, Math.ceil(list.length / state.perPage));
      buildDots();
      update();
    }

    function buildDots() {
      dotsBox.textContent = "";
      var many = state.pages > 1;
      dotsBox.hidden = !many;
      nav.hidden = !many;
      if (!many) return;
      for (var i = 0; i < state.pages; i++) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "dot";
        b.setAttribute("aria-label", "Página " + (i + 1) + " de " + state.pages);
        b.dataset.page = i;
        dotsBox.appendChild(b);
      }
    }

    function current() {
      var max = track.scrollWidth - track.clientWidth;
      if (track.scrollLeft >= max - 2) return state.pages - 1;
      return Math.min(state.pages - 1, Math.round(track.scrollLeft / state.step));
    }

    function update() {
      var page = current();
      $$(".dot", dotsBox).forEach(function (d, i) { d.setAttribute("aria-current", String(i === page)); });
      var max = track.scrollWidth - track.clientWidth;
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= max - 2;
    }

    function go(page) {
      track.scrollTo({ left: page * state.step, behavior: reduceMotion ? "auto" : "smooth" });
    }

    prev.addEventListener("click", function () { go(Math.max(0, current() - 1)); });
    next.addEventListener("click", function () { go(Math.min(state.pages - 1, current() + 1)); });
    dotsBox.addEventListener("click", function (e) {
      var d = e.target.closest(".dot");
      if (d) go(Number(d.dataset.page));
    });
    var ticking = false;
    track.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { update(); ticking = false; });
    }, { passive: true });

    return { measure: measure, reset: function () { track.scrollLeft = 0; } };
  });

  var measureAll = function () { carousels.forEach(function (c) { c.measure(); }); };
  if ("ResizeObserver" in window) {
    var ro = new ResizeObserver(function () { measureAll(); });
    $$(".carousel__track").forEach(function (t) { ro.observe(t); });
  } else {
    window.addEventListener("resize", measureAll);
  }
  measureAll();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measureAll);

  /* ---------- Filtro por categoria ---------- */
  var bar = $("[data-filterbar]");
  var names = {};
  $$(".cat[data-filter]").forEach(function (a) { names[a.dataset.filter] = $(".cat__name", a).textContent; });

  function applyFilter(cat) {
    $$(".carousel__track > li").forEach(function (li) { li.hidden = !!cat && li.dataset.cat !== cat; });
    $$(".past").forEach(function (block) {
      block.hidden = !!cat && !$(".carousel__track > li:not([hidden])", block);
    });
    var novidades = $("#novidades");
    novidades.hidden = !!cat && !$(".carousel__track > li:not([hidden])", novidades);
    var pastIntro = $("#colecoes .sec__intro");
    if (pastIntro) pastIntro.hidden = !!cat && !$(".past:not([hidden])");
    bar.hidden = !cat;
    if (cat) $("[data-filter-name]", bar).textContent = names[cat];
    carousels.forEach(function (c) { c.reset(); c.measure(); });
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-filter]");
    if (!a) return;
    e.preventDefault();
    applyFilter(a.dataset.filter);
    var target = $("#novidades:not([hidden])") || $(".past:not([hidden])");
    if (target) {
      var y = target.getBoundingClientRect().top + window.scrollY - header.offsetHeight - 52 - 8;
      window.scrollTo({ top: y, behavior: reduceMotion ? "auto" : "smooth" });
    }
    var heading = target && $("h2, h3", target);
    if (heading) { heading.setAttribute("tabindex", "-1"); heading.focus({ preventScroll: true }); }
  });
  $("[data-clear-filter]").addEventListener("click", function () {
    applyFilter(null);
    $("#categorias").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" });
  });

  /* ---------- Sacola ---------- */
  var KEY = "bruma-sacola-v1";
  var cart = [];
  try { cart = JSON.parse(localStorage.getItem(KEY) || "[]") || []; } catch (err) { cart = []; }

  var list = $("[data-cart-list]");
  var empty = $("[data-cart-empty]");
  var foot = $("[data-cart-foot]");
  var notice = $("[data-checkout-notice]");
  var toast = $("[data-toast]");
  var toastTimer;

  function save() { try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch (err) { /* sem armazenamento: a sacola vale só nesta visita */ } }

  function render() {
    var count = 0, total = 0;
    list.textContent = "";
    cart.forEach(function (item) {
      count += item.qty;
      total += item.qty * item.price;
      var li = document.createElement("li");
      li.className = "cart__item";
      li.innerHTML =
        '<img class="cart__thumb" alt="" width="72" height="90">' +
        '<div><p class="cart__name"></p><p class="cart__price"></p>' +
        '<div class="qty"><button type="button" data-qty="-1"></button><output></output><button type="button" data-qty="1"></button></div></div>' +
        '<button class="cart__remove" type="button" data-remove>Remover</button>';
      var img = $(".cart__thumb", li);
      img.src = item.img;
      img.dataset.col = item.col;
      $(".cart__name", li).textContent = item.name;
      $(".cart__price", li).textContent = brl(item.price);
      $("output", li).textContent = item.qty;
      var minus = $('[data-qty="-1"]', li), plus = $('[data-qty="1"]', li);
      minus.textContent = "−";
      plus.textContent = "+";
      minus.setAttribute("aria-label", "Diminuir quantidade de " + item.name);
      plus.setAttribute("aria-label", "Aumentar quantidade de " + item.name);
      $("[data-remove]", li).setAttribute("aria-label", "Remover " + item.name);
      li.dataset.id = item.id;
      list.appendChild(li);
    });
    empty.hidden = cart.length > 0;
    foot.hidden = cart.length === 0;
    $("[data-cart-subtotal]").textContent = brl(total);
    $$("[data-cart-count]").forEach(function (el) {
      el.textContent = count;
      if (count) el.removeAttribute("data-empty"); else el.setAttribute("data-empty", "");
    });
    $$("[data-cart-count-sr]").forEach(function (el) { el.textContent = ", " + count + (count === 1 ? " item" : " itens"); });
    var falta = Math.max(0, FRETE - total);
    $("[data-ship-text]").textContent = falta > 0 ? "Faltam " + brl(falta) + " para o frete grátis." : "Seu pedido tem frete grátis.";
    $("[data-ship-bar]").style.width = Math.min(100, (total / FRETE) * 100) + "%";
    notice.textContent = "";
  }

  function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add("is-on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("is-on"); }, 2200);
  }

  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-add]");
    if (!btn) return;
    var id = btn.dataset.add;
    var found = cart.filter(function (i) { return i.id === id; })[0];
    if (found) found.qty += 1;
    else cart.push({ id: id, name: btn.dataset.name, price: Number(btn.dataset.price), img: btn.dataset.img, col: btn.dataset.col, qty: 1 });
    save();
    render();
    btn.classList.add("is-done");
    var label = $(".add__label", btn);
    var original = label.textContent;
    label.textContent = "Adicionada à sacola";
    setTimeout(function () { btn.classList.remove("is-done"); label.textContent = original; }, 1600);
    $$(".bag-btn").forEach(function (b) {
      b.classList.remove("is-bumped"); void b.offsetWidth; b.classList.add("is-bumped");
    });
    showToast(btn.dataset.name + " foi para a sacola");
  });

  list.addEventListener("click", function (e) {
    var li = e.target.closest(".cart__item");
    if (!li) return;
    var idx = cart.findIndex(function (i) { return i.id === li.dataset.id; });
    if (idx < 0) return;
    var q = e.target.closest("[data-qty]");
    if (q) {
      cart[idx].qty += Number(q.dataset.qty);
      if (cart[idx].qty < 1) cart.splice(idx, 1);
    } else if (e.target.closest("[data-remove]")) {
      cart.splice(idx, 1);
    } else return;
    var focusSel = q ? '[data-qty="' + q.dataset.qty + '"]' : null;
    var id = li.dataset.id;
    save();
    render();
    var again = focusSel && $('.cart__item[data-id="' + id + '"] ' + focusSel, list);
    (again || $(".drawer__head .icon-btn", cartDrawer)).focus();
  });

  $("[data-checkout]").addEventListener("click", function () {
    notice.textContent = "Esta é uma loja demonstrativa de uma marca fictícia: nenhum pedido é criado e nenhum pagamento é processado.";
  });

  render();
})();
