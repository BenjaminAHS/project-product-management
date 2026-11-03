'use strict';
const examples = {
  ready: {id:'DEMO-01', merchant:'M-ALPHA', language:'EN', title:'Where is my payment?', message:'Could you trace our EUR 1,240 payment, reference INV-DEMO? Our supplier is still waiting.', state:'ready', gate:'Unique reference · TX-100 · tenant verified', sources:[{id:'LED-100',text:'M-ALPHA · TX-100 · INV-DEMO\nEUR 1,240 · sent_to_bank\nFetched: 2 Nov 2026, 10:00 UTC'}, {id:'CLE-100',text:'M-ALPHA · TX-100\nSent to bank: 2 Nov 2026, 09:58 UTC\nBeneficiary credit: NOT confirmed\nFetched: 2 Nov 2026, 10:00 UTC'}], draft:'Your EUR 1,240 payment (INV-DEMO, TX-100) was sent to the bank on 2 November at 09:58 UTC. Beneficiary credit is not yet confirmed in the available clearing record. [LED-100; CLE-100]'},
  ambiguous: {id:'DEMO-02', merchant:'M-ALPHA', language:'FR', title:'Two possible payments', message:'Où est notre paiement de 500 euros envoyé hier ? Je ne retrouve pas la référence.', state:'blocked', gate:'A unique payment reference is needed', reason:'Two authorized payments match this amount. Ask for a unique reference or escalate. No draft can be prepared from an arbitrary match.', sources:[{id:'LED-201',text:'M-ALPHA · TX-201 · EUR 500\n1 Nov 2026 · reference INV-A · pending\nFetched: 2 Nov 2026, 10:00 UTC'}, {id:'LED-202',text:'M-ALPHA · TX-202 · EUR 500\n1 Nov 2026 · reference INV-B · pending\nFetched: 2 Nov 2026, 10:00 UTC'}]},
  sensitive: {id:'DEMO-03', merchant:'M-BETA', language:'DE', title:'Release the compliance hold', message:'Unsere Auszahlung ist wegen einer Compliance-Prüfung gesperrt. Bitte erklären Sie den Grund und geben Sie sie frei.', state:'blocked', gate:'Human only · compliance specialist', reason:'Compliance explanations and hold release are outside this MVP. Route to an authorized specialist. No hold diagnosis, release promise or draft is available.', sources:[]},
  denied: {id:'DEMO-04', merchant:'M-ALPHA', language:'EN', title:'Reference outside account', message:'Please show the bank details and current status for TX-FOREIGN.', state:'blocked', gate:'Access denied · no authorized evidence', reason:'The requested reference is unavailable in this assigned merchant scope. No transaction context is exposed. Continue with authorized support or escalate.', sources:[]}
};
const $ = id => document.getElementById(id);
let current='ready'; let inspectedSources=new Set(); let manualMode=false;
const snapshotTime='2026-11-02T10:00:00Z';
function render(key){
  current=key;inspectedSources=new Set();manualMode=false; const t=examples[key];
  document.querySelectorAll('[data-ticket]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.ticket===key)));
  $('ticket-meta').textContent=`#${t.id} · ${t.language} · Synthetic ticket`;
  $('ticket-title').textContent=t.title; $('merchant').textContent=`Authenticated merchant: ${t.merchant}`; $('message').textContent=t.message;
  $('gate').textContent=t.gate; $('gate').className=t.state==='ready'?'safe':'warning';
  $('sources').replaceChildren();
  t.sources.forEach(s=>{ const b=document.createElement('button'); b.textContent=`Open ${s.id} · ${t.merchant}`;b.addEventListener('click',()=>{ $('source-detail').hidden=false;$('source-detail').textContent=s.text;inspectedSources.add(s.id);b.textContent=`Checked ${s.id} · ${t.merchant}`;updateApproval();});$('sources').append(b); });
  if(!t.sources.length){const p=document.createElement('p');p.textContent='No authorized evidence available in this scope.';p.className='empty';$('sources').append(p);}
  $('source-detail').hidden=true;$('source-detail').textContent='';$('draft-panel').hidden=t.state!=='ready';$('draft').value=t.draft||'';
  $('blocked').hidden=t.state==='ready';$('blocked').textContent=t.reason||'';
  $('review').checked=false;$('editor').value='';$('manual-note').value='';$('reason').value='';$('status').textContent='';$('packet').hidden=true;$('packet').replaceChildren();updateApproval();
}
function updateApproval(){
  const t=examples[current], allInspected=t.sources.length>0 && t.sources.every(s=>inspectedSources.has(s.id));
  $('use-draft').disabled=!(t.state==='ready' && !manualMode && allInspected && $('review').checked && $('draft').value.trim());
  $('review-progress').textContent=manualMode?'Manual handling selected. Reset or reopen the ticket to resume assisted drafting.':`${inspectedSources.size}/${t.sources.length} sources inspected. Open every source and confirm review before using the draft.`;
}
document.querySelectorAll('[data-ticket]').forEach(b=>b.addEventListener('click',()=>render(b.dataset.ticket)));
$('review').addEventListener('change',updateApproval);
$('draft').addEventListener('input',()=>{$('review').checked=false;updateApproval();});
$('use-draft').addEventListener('click',()=>{if($('use-draft').disabled)return;$('editor').value=$('draft').value;$('status').textContent='Reviewed draft placed in your editor. No message sent.';});
$('escalate').addEventListener('click',()=>{
  const t=examples[current],reason=$('reason').value,note=$('manual-note').value.trim();
  if(!reason){$('status').textContent='Choose a handover reason first.';$('reason').focus();return;}
  if(reason==='Other — see agent note' && !note){$('status').textContent='Add an agent note for this handover reason.';$('manual-note').focus();return;}
  $('packet').hidden=false;$('packet').replaceChildren();
  const title=document.createElement('h2');title.textContent=`Handover preview · ${current==='sensitive'?'Tier-2 compliance':'Tier-2 payments'}`;$('packet').append(title);
  for(const line of [`Ticket: ${t.id}`,`Verified merchant: ${t.merchant}`,`Reason: ${reason}`,`Gate: ${t.gate}`,`Authorized sources: ${t.sources.map(s=>`${s.id} (snapshot fetched ${snapshotTime})`).join(', ')||'none'}`,`Agent note: ${note||'none'}`]){const p=document.createElement('p');p.textContent=line;$('packet').append(p);}
  $('status').textContent='Escalation simulated in this page. Nothing sent to a real queue.';
});
$('manual').addEventListener('click',()=>{manualMode=true;$('review').checked=false;updateApproval();$('draft-panel').hidden=true;$('status').textContent='Manual handling selected. Continue in the reply editor; no customer message sent.';$('editor').focus();});
$('reset').addEventListener('click',()=>render('ready'));
render('ready');
