/*
 * audit-logic.js — pure, side-effect-free logic for the Digital Arc Self-Audit tool.
 * UMD so it loads in the browser AND in node for testing.
 * All decisions here are deterministic from the input slugs; no DOM, no network.
 *
 * Input slugs (must match the option <input value="..."> in the HTML):
 *   footprint  assets|identity|network|data
 *   cadence    never|yearly|quarterly|monthly
 *   interest   legibility|risk|trajectory|network
 *   legibility clear|partial|fog
 *   focus      list|defend|plan|publish
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    root.auditLib = api;
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const VERDICT = {
    assets:      {t:"owned",     v:"your footprint is a stack of things that deserve a single ledger",           r:"start by listing everything you own. inventory first, strategy second."},
    identity:    {t:"identity",  v:"your name flows across the web without a single source of truth",           r:"pick one home for your name and make it yours before you build on top of it."},
    network:     {t:"network",   v:"your reputation is carried by the people who cite or mirror you",           r:"stop building on borrowed surface. name your own home first."},
    data:        {t:"data",      v:"the cost of your footprint hides in subscriptions you forgot",              r:"run a subscription + data sweep this week. kill what you forgot."},
    clear:       {t:"clear",     v:"you already have a baseline",                                             r:"protect the baseline. drift will come, but you're ahead of it."},
    partial:     {t:"legibility",v:"you have a partial map but no single source of truth",                     r:"consolidate into one list. clarity is the first deliverable, not the last."},
    fog:         {t:"fog",       v:"you don't even know what you own",                                        r:"inventory first. a 60-second list beats a 60-hour strategy."},
    never:       {t:"cadence",   v:"no recent map of where your digital self sits",                           r:"run the audit now. the map is the deliverable, strategy is only the next step."},
    yearly:      {t:"cadence",   v:"your map is 12 months stale",                                            r:"re-run this quarterly. drift compounds silently until it bites."},
    quarterly:   {t:"cadence",   v:"your cadence is tight enough to course-correct",                          r:"keep going quarterly. you're already on the right track."},
    monthly:     {t:"cadence",   v:"you are already running the right cadence",                               r:"protect that discipline. cadence is your edge."},
    legibility:  {t:"legibility",v:"knowing exactly what I own & where it lives",                              r:"start with a single list. inventory is the deliverable."},
    risk:        {t:"risk",      v:"the risk is the slow bleed of subscriptions and forgotten data",          r:"subscription + data sweep. kill what you forgot this week."},
    trajectory:  {t:"trajectory",v:"you care about the 3–5 year direction",                                  r:"write a plain-english 3-year plan. the arc is the point."},
    plan:        {t:"plan",      v:"you already know the fix: a stated direction",                            r:"write the plan down. a stated direction is the whole job."},
    list:  {t:"list",   v:"the missing piece is a single inventory",                       r:"list everything you own this week. inventory is the deliverable."},
    defend:{t:"defend", v:"the risk is the slow bleed of subscriptions and forgotten data", r:"subscription + data sweep. kill what you forgot this week."},
    publish:     {t:"publish",   v:"you want your reputation to live somewhere, on purpose",                  r:"name your own home first. the rest of the web is borrowed surface."},
  };

  const audit = function (inputs) {
    const { footprint, cadence, interest, legibility, focus } = inputs || {};
    const bits = [];
    if (footprint) bits.push({t: VERDICT[footprint] ? VERDICT[footprint].t : "owned", v: VERDICT[footprint] ? VERDICT[footprint].v : "your footprint needs inventory", r: VERDICT[footprint] ? VERDICT[footprint].r : "start by inventorying what you own."});
    if (cadence) bits.push({t:"cadence", v: cadence === "never" ? "no recent map of where your digital self sits" : cadence === "yearly" ? "your map is 12 months stale" : cadence === "monthly" ? "you are already running the right cadence" : "your cadence is tight enough to course-correct", r: cadence === "never" ? "run the audit now. the map is the deliverable." : cadence === "yearly" ? "re-run this quarterly. drift compounds silently." : cadence === "monthly" ? "protect that discipline. cadence is your edge." : "tight enough to course-correct before drift bites."});
    if (interest) bits.push({t: interest === "legibility" ? "legibility" : interest === "risk" ? "risk" : interest === "network" ? "network" : "trajectory", v: interest === "legibility" ? "knowing exactly what I own & where it lives" : interest === "risk" ? "the risk is the slow bleed of subscriptions and forgotten data" : interest === "network" ? "your reputation is carried by the people who cite or mirror you" : "you care about the 3–5 year direction", r: interest === "legibility" ? "start with a single list. inventory is the deliverable." : interest === "risk" ? "subscription + data sweep. kill what you forgot this week." : interest === "network" ? "stop building on borrowed surface. name your own home first." : "write a plain-english 3-year plan. the arc is the point."});
    if (legibility) bits.push({t: legibility === "clear" ? "clear" : legibility === "fog" ? "fog" : "legibility", v: legibility === "clear" ? "you have a baseline" : legibility === "fog" ? "you don't even know what you own" : "you have a partial map but no single source of truth", r: legibility === "clear" ? "protect the baseline." : legibility === "fog" ? "inventory first. clarity is the deliverable." : "consolidate into one list. clarity first, strategy second."});
    if (focus) bits.push({t: VERDICT[focus] ? VERDICT[focus].t : focus, v: VERDICT[focus] ? VERDICT[focus].v : focus, r: VERDICT[focus] ? VERDICT[focus].r : "keep this as your north star."});

    return {
      verdict: bits.map(function (x) { return x.t; }).join(" · "),
      recommend: bits[0] ? bits[0].r : "start by inventorying what you own.",
      bits: bits,
      themes: bits.map(function (x) { return x.t; })
    };
  };

  return {
    VERDICT: VERDICT,
    audit: audit
  };
});
