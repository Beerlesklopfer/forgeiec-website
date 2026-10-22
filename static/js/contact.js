/* ForgeIEC contact form (progressive enhancement, no dependencies).
   Fetches a signed token from /api/contact/token, submits the form as JSON
   to /api/contact/ and reports the result in an aria-live region. Makes no
   requests other than those two, sets no cookies, stores nothing. */
(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  var msgEl = document.getElementById("contact-form-messages");
  if (!form || !msgEl || !window.fetch || !window.JSON) return;

  var M;
  try { M = JSON.parse(msgEl.textContent); } catch (e) { return; }

  var endpoint = form.getAttribute("data-endpoint") || "/api/contact/";
  var status = document.getElementById("cf-status");
  var button = form.querySelector(".cf-submit");
  var message = form.elements["message"];
  var counter = document.getElementById("cf-message-count");
  var MIN_AGE_MS = 3500;          // server minimum is 3 s
  var REFRESH_MS = 60 * 60 * 1000; // server maximum is 2 h
  var token = null;
  var tokenAt = 0;
  var busy = false;

  var FIELD_IDS = {
    "name": "cf-name", "email": "cf-email", "subject-type": "cf-type",
    "message": "cf-message", "consent": "cf-consent"
  };

  function mailLink() {
    var a = document.createElement("a");
    a.href = "mailto:" + M.mail;
    a.textContent = M.mail;
    return a;
  }

  function setStatus(kind, text, withMail) {
    status.textContent = "";
    status.className = "cf-status" + (kind ? " cf-status-" + kind : "");
    if (!text) return;
    status.appendChild(document.createTextNode(text + (withMail ? " " : "")));
    if (withMail) {
      status.appendChild(mailLink());
      status.appendChild(document.createTextNode("."));
    }
  }

  function fieldError(name, text) {
    var input = document.getElementById(FIELD_IDS[name]);
    var err = document.getElementById(FIELD_IDS[name] + "-err");
    if (!input || !err) return;
    if (text) {
      input.setAttribute("aria-invalid", "true");
      err.textContent = text;
      err.hidden = false;
    } else {
      input.removeAttribute("aria-invalid");
      err.textContent = "";
      err.hidden = true;
    }
  }

  function clearErrors() {
    for (var k in FIELD_IDS) fieldError(k, "");
  }

  function codeText(field, code) {
    if (field === "consent") return M.consent;
    if (code === "required") return M.required;
    if (code === "too_long") return M.tooLong;
    if (code === "too_short") return M.tooShort;
    if (code === "control_chars") return M.controlChars;
    if (field === "email") return M.invalidEmail;
    return M.invalid;
  }

  /* Mirrors the server rules so most mistakes show before sending. */
  function localCheck() {
    var errors = {};
    var name = form.elements["name"].value.trim();
    var email = form.elements["email"].value.trim();
    var text = message.value.trim();
    if (!name) errors["name"] = "required";
    else if (name.length > 100) errors["name"] = "too_long";
    if (!email) errors["email"] = "required";
    else if (email.length > 254 ||
             !/^[A-Za-z0-9!#$%&'*+\/=?^_`{|}~-]+(\.[A-Za-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@([A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$/.test(email))
      errors["email"] = "invalid";
    if (!form.elements["subject-type"].value) errors["subject-type"] = "required";
    if (!text) errors["message"] = "required";
    else if (text.length < 10) errors["message"] = "too_short";
    else if (text.length > 5000) errors["message"] = "too_long";
    if (!form.elements["consent"].checked) errors["consent"] = "required";
    return errors;
  }

  function showErrors(errors) {
    var first = null;
    for (var k in errors) {
      fieldError(k, codeText(k, errors[k]));
      if (!first) first = document.getElementById(FIELD_IDS[k]);
    }
    if (first) {
      setStatus("error", M.checkFields);
      first.focus();
      return true;
    }
    return false;
  }

  function updateCounter() {
    counter.textContent = M.counter.replace("{n}", String(message.value.length));
    counter.classList.toggle("cf-count-warn", message.value.length > 4800);
  }

  function fetchToken() {
    return fetch(endpoint + "token", {
      method: "GET", credentials: "omit", cache: "no-store",
      headers: { "Accept": "application/json" }
    }).then(function (r) {
      if (!r.ok) throw new Error("token");
      return r.json();
    }).then(function (data) {
      if (!data || !data.ok || typeof data.token !== "string") throw new Error("token");
      token = data.token;
      tokenAt = Date.now();
    });
  }

  function wait(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  function setBusy(on) {
    busy = on;
    button.disabled = on;
    form.setAttribute("aria-busy", on ? "true" : "false");
    button.textContent = on ? M.sending : M.submit;
  }

  function payload() {
    return JSON.stringify({
      "name": form.elements["name"].value,
      "email": form.elements["email"].value.trim(),
      "subject-type": form.elements["subject-type"].value,
      "message": message.value,
      "consent": form.elements["consent"].checked,
      "website": form.elements["website"].value,
      "lang": M.lang,
      "token": token
    });
  }

  function post(retried) {
    var age = Date.now() - tokenAt;
    var pre = age < MIN_AGE_MS ? wait(MIN_AGE_MS - age) : Promise.resolve();
    return pre.then(function () {
      return fetch(endpoint, {
        method: "POST", credentials: "omit", cache: "no-store",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: payload()
      });
    }).then(function (r) {
      return r.json().catch(function () { return { ok: false, error: "http_" + r.status }; });
    }).then(function (data) {
      if (data.ok) return data;
      var e = data.error;
      if (!retried && (e === "token_too_fresh" || e === "token_expired" || e === "invalid_token")) {
        // One silent retry with a new token (it needs its minimum age).
        return fetchToken().then(function () { return post(true); });
      }
      return data;
    });
  }

  function onSubmit(ev) {
    ev.preventDefault();
    if (busy) return;
    clearErrors();
    setStatus("", "");
    if (showErrors(localCheck())) return;
    setBusy(true);
    var start = token ? Promise.resolve() : fetchToken();
    start.then(function () { return post(false); }).then(function (data) {
      if (data.ok) {
        form.reset();
        updateCounter();
        setStatus("ok", M.sent);
        status.focus();
        fetchToken().catch(function () {});
        return;
      }
      switch (data.error) {
        case "invalid_fields":
          showErrors(data.fields || {});
          break;
        case "token_too_fresh":
        case "token_expired":
        case "invalid_token":
          setStatus("error", M.tokenRetry);
          break;
        case "rate_limited":
          setStatus("error", M.rateLimited, true);
          break;
        default:
          setStatus("error", M.unavailable, true);
      }
    }).catch(function () {
      setStatus("error", M.unavailable, true);
    }).then(function () {
      setBusy(false);
    });
  }

  // Optional preselection: /kontakt/?type=pilot
  try {
    var wanted = (new URLSearchParams(window.location.search).get("type") || "").replace(/[^a-z]/g, "");
    var select = form.elements["subject-type"];
    if (wanted && select.querySelector('option[value="' + wanted + '"]')) {
      select.value = wanted;
    }
  } catch (e) { /* old browser: no preselection */ }

  form.hidden = false;
  form.addEventListener("submit", onSubmit);
  message.addEventListener("input", updateCounter);
  updateCounter();

  fetchToken().catch(function () {
    setStatus("error", M.unavailable, true);
  });
  setInterval(function () { fetchToken().catch(function () {}); }, REFRESH_MS);
})();
