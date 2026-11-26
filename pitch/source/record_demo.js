const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const DIR = __dirname;
const URL = 'https://deploy-project-product-management.vercel.app/?demo';
const W = 1920, H = 1080;

(async () => {
  const browser = await chromium.launch({ channel: 'chrome' });
  const ctx = await browser.newContext({
    viewport: { width: W, height: H }, deviceScaleFactor: 1,
    recordVideo: { dir: path.join(DIR, 'raw'), size: { width: W, height: H } },
  });
  // Visible fake cursor (Playwright video has no OS cursor).
  await ctx.addInitScript(() => {
    const install = () => {
      if (document.getElementById('__cursor')) return;
      const c = document.createElement('div');
      c.id = '__cursor';
      c.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M4 2 L4 20 L9 15 L12.5 22 L15.5 20.5 L12 13.5 L19 13.5 Z" fill="#111" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>';
      Object.assign(c.style, { position: 'fixed', left: '0', top: '0', zIndex: 2147483647, pointerEvents: 'none', transform: 'translate(-200px,-200px)', filter: 'drop-shadow(0 1px 2px rgba(0,0,0,.4))' });
      document.documentElement.appendChild(c);
      const ring = document.createElement('div');
      Object.assign(ring.style, { position: 'fixed', width: '34px', height: '34px', marginLeft: '-17px', marginTop: '-17px', borderRadius: '50%', border: '3px solid rgba(37,99,235,.8)', zIndex: 2147483646, pointerEvents: 'none', opacity: '0', transition: 'opacity .35s, transform .35s', left: '0', top: '0' });
      document.documentElement.appendChild(ring);
      window.addEventListener('mousemove', (e) => { c.style.transform = `translate(${e.clientX - 4}px,${e.clientY - 2}px)`; }, true);
      window.addEventListener('mousedown', (e) => {
        ring.style.left = e.clientX + 'px'; ring.style.top = e.clientY + 'px';
        ring.style.transition = 'none'; ring.style.opacity = '1'; ring.style.transform = 'scale(.6)';
        requestAnimationFrame(() => { ring.style.transition = 'opacity .5s, transform .5s'; ring.style.opacity = '0'; ring.style.transform = 'scale(1.4)'; });
      }, true);
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install); else install();
  });
  const page = await ctx.newPage();
  const t0 = Date.now();
  const marks = [];
  const mark = (label) => { const s = (Date.now() - t0) / 1000; marks.push([s, label]); console.log(s.toFixed(1), label); };
  const P = 1.6; const wait = (ms) => page.waitForTimeout(ms >= 1000 ? ms * P : ms);
  let mx = W / 2, my = H / 2;
  let shot = 0;
  const snap = async (name) => { await page.screenshot({ path: path.join(DIR, `check_${++shot}_${name}.png`) }); };

  async function smoothScrollTo(loc, block = 'center') {
    await loc.evaluate((el, block) => el.scrollIntoView({ behavior: 'smooth', block }), block);
    await wait(900);
  }
  async function moveTo(loc) {
    const box = await loc.boundingBox();
    if (!box) throw new Error('no box');
    const x = box.x + Math.min(box.width / 2, 60 + Math.random() * 10), y = box.y + box.height / 2;
    await page.mouse.move(x, y, { steps: 28 });
    mx = x; my = y;
  }
  async function click(sel, opts = {}) {
    const loc = typeof sel === 'string' ? page.locator(sel).first() : sel;
    await loc.waitFor({ state: 'visible', timeout: 15000 });
    const box = await loc.boundingBox();
    if (!box || box.y < 70 || box.y + box.height > H - 40) await smoothScrollTo(loc, opts.block || 'center');
    await moveTo(loc);
    await wait(350);
    await page.mouse.down(); await wait(80); await page.mouse.up();
  }

  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.mouse.move(W / 2, H / 2);
  await page.waitForFunction(() => !/Connecting/.test(document.getElementById('assist-mode').textContent), null, { timeout: 20000 }).catch(() => {});
  console.log('assist:', await page.locator('#assist-mode').textContent());
  mark('App loaded, DEMO-01 open');
  await wait(3500);

  // ---- 1. DEMO-01 ----
  const sources = page.locator('#sources button');
  const n = await sources.count();
  console.log('sources', n, await sources.allTextContents());
  await click(sources.nth(0));
  mark('DEMO-01: ledger record opened');
  await wait(2500);
  await click(sources.nth(1));
  mark('DEMO-01: clearing record opened');
  for (let i = 2; i < n; i++) { await wait(1200); await click(sources.nth(i)); }
  await wait(800);
  await smoothScrollTo(page.locator('#summary-panel'), 'center');
  await moveTo(page.locator('#payment-status'));
  mark('DEMO-01: amber status "Sent to recipient\'s bank · not yet received"');
  await wait(3000);
  await snap('ledger_status');

  await smoothScrollTo(page.locator('#step-review'), 'start');
  mark('DEMO-01: Step 2 - cited reply pre-filled with verified facts');
  await wait(1500);
  await moveTo(page.locator('#verified-facts'));
  await wait(1500);
  await moveTo(page.locator('#editor'));
  await wait(2000);
  await snap('step2_reply');

  await click('#final-review', { block: 'center' });
  mark('DEMO-01: ticked "I checked the facts and the wording"');
  await wait(1500);
  await click('#record-reply');
  mark('DEMO-01: Approve & close clicked');
  await page.locator('#outcome-card').waitFor({ state: 'visible', timeout: 15000 });
  await wait(700);
  await smoothScrollTo(page.locator('#outcome-card'), 'center');
  mark('DEMO-01: outcome card "Case closed"');
  await wait(3500);
  await snap('outcome');

  console.log('next btn:', await page.locator('#next-ticket').textContent());
  // ---- 2. DEMO-05 ----
  const nextText = await page.locator('#next-ticket').textContent();
  await moveTo(page.locator('#next-ticket')); await wait(1200);
  if (/DEMO-05/.test(nextText)) await click('#next-ticket');
  else await click(page.locator('#ticket-list button.ticket', { hasText: 'DEMO-05' }));
  await wait(1200);
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
  await wait(800);
  console.log('title:', await page.locator('#ticket-title').textContent());
  mark('DEMO-05 "A USD transfer has failed" opened');
  await wait(2500);
  const s5 = page.locator('#sources button');
  const n5 = await s5.count();
  for (let i = 0; i < n5; i++) { await click(s5.nth(i)); await wait(1300); }
  mark('DEMO-05: sources checked, reply pre-filled');
  await smoothScrollTo(page.locator('#step-review'), 'start');
  await wait(2000);
  const ed = page.locator('#editor');
  await click(ed);
  await page.keyboard.press('Meta+ArrowDown');
  await page.keyboard.press('End');
  await wait(500);
  await page.keyboard.type(' We will refund you next week.', { delay: 95 });
  await page.locator('#policy-alert').waitFor({ state: 'visible', timeout: 5000 });
  await wait(400);
  await smoothScrollTo(page.locator('#policy-alert'), 'center');
  await moveTo(page.locator('#policy-alert-quotes'));
  mark('DEMO-05: red notice quoting the refund promise, approval disabled');
  console.log('record-reply disabled:', await page.locator('#record-reply').isDisabled());
  await wait(3500);
  await snap('refusal');
  await click('#restore-reply');
  mark('DEMO-05: "Put FlowAssist\'s reply back" clicked, notice gone');
  await wait(2500);
  console.log('alert hidden after restore:', await page.locator('#policy-alert').isHidden());

  // ---- 3. DEMO-03 ----
  await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'smooth' }));
  await wait(900);
  await click(page.locator('#ticket-list button.ticket', { hasText: 'DEMO-03' }));
  await wait(1200);
  mark('DEMO-03 "Release the compliance hold" opened');
  await wait(2000);
  await smoothScrollTo(page.locator('#blocked-card'), 'start');
  await moveTo(page.locator('#blocked-why'));
  mark('DEMO-03: card explains why no draft + what to do');
  await wait(4000);
  await snap('blocked');
  const ho = page.locator('#handover');
  if (!(await ho.evaluate((e) => e.open))) await click('#handover summary');
  await smoothScrollTo(page.locator('#reason'), 'center');
  await moveTo(page.locator('#reason'));
  console.log('reason:', await page.locator('#reason').evaluate((s) => s.options[s.selectedIndex].text));
  mark('DEMO-03: suggested hand-over reason');
  await wait(2500);
  await click('#escalate');
  await page.locator('#packet').waitFor({ state: 'visible', timeout: 10000 });
  await wait(500);
  await smoothScrollTo(page.locator('#packet'), 'center');
  mark('DEMO-03: hand-over preview shown');
  await wait(3500);
  await click('#record-handover');
  mark('DEMO-03: Confirm hand-over clicked');
  await page.locator('#outcome-card').waitFor({ state: 'visible', timeout: 15000 });
  await wait(600);
  await smoothScrollTo(page.locator('#outcome-card'), 'center');
  mark('DEMO-03: outcome "Handed over"');
  await wait(4000);
  await snap('handover_done');
  mark('end');

  fs.writeFileSync(path.join(DIR, 'marks.json'), JSON.stringify(marks, null, 1));
  const vpath = await page.video().path();
  await ctx.close(); await browser.close();
  fs.copyFileSync(vpath, path.join(DIR, 'raw.webm'));
  console.log('video', vpath, 'total', ((Date.now() - t0) / 1000).toFixed(1));
})().catch((e) => { console.error(e); process.exit(1); });
