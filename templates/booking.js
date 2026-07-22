/* booking.js — self-contained booking/appointment function for a static site.
 *
 * No backend required. On submit it validates the form, then:
 *   1. shows an inline confirmation,
 *   2. builds a downloadable .ics calendar invite,
 *   3. offers a mailto: link pre-filled with the booking details.
 *
 * Optional: set window.BOOKING_CONFIG before this script loads to customize:
 *   window.BOOKING_CONFIG = {
 *     businessName: "BRAND",
 *     email: "hello@brand.com",       // where mailto is addressed
 *     durationMinutes: 60,
 *     services: ["Consultation", "Full session"],
 *     // Optional POST endpoint (Formspree, your API, etc.). If set, the form
 *     // is also POSTed there as JSON; failure falls back to mailto/.ics only.
 *     endpoint: null,
 *   };
 *
 * Markup contract (see index.html #booking):
 *   <form id="booking-form"> with named fields:
 *     service (select), date (input[type=date]), time (input[type=time]),
 *     name, email, notes; plus a submit button.
 *   <div id="booking-result"> for the confirmation UI.
 */
(function () {
  "use strict";

  const cfg = Object.assign(
    {
      businessName: "BRAND",
      email: "hello@example.com",
      durationMinutes: 60,
      services: ["Consultation", "Full session", "Quick call"],
      endpoint: null,
    },
    window.BOOKING_CONFIG || {}
  );

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  // Build a UTC timestamp string for ICS: YYYYMMDDTHHMMSSZ
  function icsStamp(date) {
    return (
      date.getUTCFullYear() +
      pad(date.getUTCMonth() + 1) +
      pad(date.getUTCDate()) +
      "T" +
      pad(date.getUTCHours()) +
      pad(date.getUTCMinutes()) +
      pad(date.getUTCSeconds()) +
      "Z"
    );
  }

  function escapeICS(s) {
    return String(s)
      .replace(/\\/g, "\\\\")
      .replace(/;/g, "\\;")
      .replace(/,/g, "\\,")
      .replace(/\n/g, "\\n");
  }

  function buildICS(booking) {
    const start = new Date(`${booking.date}T${booking.time}`);
    const end = new Date(start.getTime() + cfg.durationMinutes * 60000);
    const uid = `${Date.now()}-${Math.random().toString(36).slice(2)}@${location.hostname || "local"}`;
    const summary = `${cfg.businessName} — ${booking.service}`;
    const desc =
      `Booking for ${booking.name} (${booking.email}).` +
      (booking.notes ? `\nNotes: ${booking.notes}` : "");
    return [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//scroll-cinematic//booking//EN",
      "CALSCALE:GREGORIAN",
      "METHOD:PUBLISH",
      "BEGIN:VEVENT",
      `UID:${uid}`,
      `DTSTAMP:${icsStamp(new Date())}`,
      `DTSTART:${icsStamp(start)}`,
      `DTEND:${icsStamp(end)}`,
      `SUMMARY:${escapeICS(summary)}`,
      `DESCRIPTION:${escapeICS(desc)}`,
      `ORGANIZER;CN=${escapeICS(cfg.businessName)}:mailto:${cfg.email}`,
      `ATTENDEE;CN=${escapeICS(booking.name)};RSVP=TRUE:mailto:${booking.email}`,
      "END:VEVENT",
      "END:VCALENDAR",
    ].join("\r\n");
  }

  function mailtoLink(booking) {
    const subject = `Booking request: ${booking.service} — ${booking.date} ${booking.time}`;
    const body =
      `Hi ${cfg.businessName},\n\n` +
      `I'd like to book:\n` +
      `• Service: ${booking.service}\n` +
      `• Date: ${booking.date}\n` +
      `• Time: ${booking.time}\n` +
      `• Name: ${booking.name}\n` +
      `• Email: ${booking.email}\n` +
      (booking.notes ? `• Notes: ${booking.notes}\n` : "") +
      `\nThanks!`;
    return `mailto:${cfg.email}?subject=${encodeURIComponent(
      subject
    )}&body=${encodeURIComponent(body)}`;
  }

  function validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function fieldError(form, name, msg) {
    const el = form.elements[name];
    const wrap = el ? el.closest(".field") : null;
    if (wrap) {
      wrap.classList.toggle("field--error", !!msg);
      const hint = wrap.querySelector(".field__error");
      if (hint) hint.textContent = msg || "";
    }
    return !msg;
  }

  function validate(form, booking) {
    let ok = true;
    ok = fieldError(form, "service", booking.service ? "" : "Please choose a service.") && ok;
    ok = fieldError(form, "date", booking.date ? "" : "Pick a date.") && ok;
    ok = fieldError(form, "time", booking.time ? "" : "Pick a time.") && ok;
    ok = fieldError(form, "name", booking.name ? "" : "Your name, please.") && ok;
    ok =
      fieldError(
        form,
        "email",
        !booking.email ? "Your email, please." : !validEmail(booking.email) ? "That email looks off." : ""
      ) && ok;

    // Date must not be in the past.
    if (booking.date && booking.time) {
      const when = new Date(`${booking.date}T${booking.time}`);
      if (when.getTime() < Date.now()) {
        ok = fieldError(form, "date", "Please pick a future date/time.") && ok;
      }
    }
    return ok;
  }

  function download(filename, text) {
    const blob = new Blob([text], { type: "text/calendar;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function showConfirmation(form, result, booking, icsText) {
    const pretty = new Date(`${booking.date}T${booking.time}`).toLocaleString(undefined, {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
    form.hidden = true;
    result.hidden = false;
    result.innerHTML = `
      <div class="booking-confirm" role="status">
        <div class="booking-confirm__check" aria-hidden="true">✓</div>
        <h3>You're booked in${booking.name ? ", " + escapeHTML(booking.name.split(" ")[0]) : ""}!</h3>
        <p><strong>${escapeHTML(booking.service)}</strong><br>${escapeHTML(pretty)}</p>
        <p class="booking-confirm__muted">We'll confirm by email at ${escapeHTML(booking.email)}.</p>
        <div class="booking-confirm__actions">
          <button type="button" class="btn" id="booking-ics">Add to calendar</button>
          <a class="btn btn--ghost" id="booking-mail" href="${mailtoLink(booking)}">Email us the request</a>
          <button type="button" class="btn btn--ghost" id="booking-again">Make another booking</button>
        </div>
      </div>`;
    result.querySelector("#booking-ics").addEventListener("click", () =>
      download(`booking-${booking.date}.ics`, icsText)
    );
    result.querySelector("#booking-again").addEventListener("click", () => {
      result.hidden = true;
      result.innerHTML = "";
      form.hidden = false;
      form.reset();
    });
  }

  function escapeHTML(s) {
    const d = document.createElement("div");
    d.textContent = String(s);
    return d.innerHTML;
  }

  function populateServices(form) {
    const select = form.elements["service"];
    if (!select || select.options.length > 1) return; // author supplied options
    cfg.services.forEach((s) => {
      const opt = document.createElement("option");
      opt.value = s;
      opt.textContent = s;
      select.appendChild(opt);
    });
  }

  function setDateFloor(form) {
    const date = form.elements["date"];
    if (date && !date.min) {
      const now = new Date();
      date.min = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    }
  }

  ready(function () {
    const form = document.getElementById("booking-form");
    const result = document.getElementById("booking-result");
    if (!form || !result) return;

    populateServices(form);
    setDateFloor(form);

    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const booking = {
        service: form.elements["service"].value.trim(),
        date: form.elements["date"].value,
        time: form.elements["time"].value,
        name: form.elements["name"].value.trim(),
        email: form.elements["email"].value.trim(),
        notes: form.elements["notes"] ? form.elements["notes"].value.trim() : "",
      };

      if (!validate(form, booking)) return;

      const icsText = buildICS(booking);

      // Optional: POST to a configured endpoint. Never block the UX on it.
      if (cfg.endpoint) {
        try {
          await fetch(cfg.endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(booking),
          });
        } catch (err) {
          /* fall back to mailto/.ics silently */
        }
      }

      showConfirmation(form, result, booking, icsText);
    });
  });
})();
