/* Client for the FlowAssist API (api/index.py) and product analytics.

   The browser engine gives an instant preview; the server decides every
   recorded action. Opened from file:// there is no server: the page runs in
   local preview mode and says so. Analytics (PostHog EU) loads only when the
   server publishes a project key, never sends ticket, draft or note text, and
   is a no-op otherwise. */
(() => {
  "use strict";
  const enabled =
    typeof location !== "undefined" && /^https?:$/.test(location.protocol);
  const sessionId = `ops-${Math.random().toString(36).slice(2, 10)}`;
  let analytics = null;
  const queued = [];

  async function request(method, path, body) {
    const started = performance.now();
    const response = await fetch(`/api/${path}`, {
      method,
      headers: { "content-type": "application/json", "x-session-id": sessionId },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await response.json().catch(() => ({}));
    return { status: response.status, data, ms: Math.round(performance.now() - started) };
  }

  function loadAnalytics(settings) {
    if (!settings || !settings.posthog_key || analytics) return;
    // Official PostHog array snippet, EU cloud, privacy-first settings.
    !(function (t, e) {
      var o, n, p, r;
      e.__SV ||
        ((window.posthog = e),
        (e._i = []),
        (e.init = function (i, s, a) {
          function g(t, e) {
            var o = e.split(".");
            2 == o.length && ((t = t[o[0]]), (e = o[1])),
              (t[e] = function () {
                t.push([e].concat(Array.prototype.slice.call(arguments, 0)));
              });
          }
          ((p = t.createElement("script")).type = "text/javascript"),
            (p.crossOrigin = "anonymous"),
            (p.async = !0),
            (p.src = s.api_host.replace(".i.posthog.com", "-assets.i.posthog.com") + "/static/array.js"),
            (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(p, r);
          var u = e;
          for (
            void 0 !== a ? (u = e[a] = []) : (a = "posthog"),
              u.people = u.people || [],
              u.toString = function (t) {
                var e = "posthog";
                return "posthog" !== a && (e += "." + a), t || (e += " (stub)"), e;
              },
              u.people.toString = function () {
                return u.toString(1) + ".people (stub)";
              },
              o = "capture register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled getFeatureFlag onFeatureFlags reloadFeatureFlags".split(" "),
              n = 0;
            n < o.length;
            n++
          )
            g(u, o[n]);
          e._i.push([i, s, a]);
        }),
        (e.__SV = 1));
    })(document, window.posthog || []);
    window.posthog.init(settings.posthog_key, {
      api_host: settings.posthog_host,
      autocapture: false,
      capture_pageview: true,
      capture_pageleave: true,
      disable_session_recording: true,
      persistence: "memory",
      person_profiles: "never",
    });
    window.posthog.register({ env: settings.env, app: "flowassist", ops_session: sessionId });
    analytics = window.posthog;
    queued.splice(0).forEach(([event, props]) => analytics.capture(event, props));
  }

  globalThis.FlowServer = {
    enabled,
    sessionId,
    async config() {
      const result = await request("GET", "config");
      if (result.status !== 200) throw new Error(`config ${result.status}`);
      loadAnalytics(result.data.analytics);
      return result.data;
    },
    analyze: (body) => request("POST", "analyze", body),
    check: (body) => request("POST", "check", body),
    handover: (body) => request("POST", "handover", body),
    track(event, props = {}) {
      if (!enabled) return;
      if (analytics) analytics.capture(event, props);
      else if (queued.length < 50) queued.push([event, props]);
    },
  };
})();
