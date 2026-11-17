# Mise en place CI/CD, API et PostHog — guide pour Benjamin

**Pour qui :** Benjamin, admin du repo principal `BenjaminAHS/project-product-management`. Seule l'étape 2 demande l'accès au projet Vercel, qui est sur le compte de Lenny (`lsantus-mines`) : demande-lui de t'ajouter au projet, ou fais-la ensemble.
**Durée :** ~30 min. **Coût :** 0 € — tout tient dans les offres gratuites (GitHub Actions, Vercel Hobby, PostHog Free).
**Contexte :** la PR `anthony/production-hardening` ajoute une API FastAPI (guardrails côté serveur), une CI, un déploiement conditionné à la CI, un interrupteur global et le suivi PostHog. Rien ne change pour la démo tant que la PR n'est pas mergée.

Ordre conseillé : **1 → 2 → 3 → merge de la PR → 4**.

---

## 1. GitHub — la CI (sur ton repo)

La CI tourne sur le repo principal `BenjaminAHS/project-product-management`, donc sur les minutes GitHub Actions de **ce** compte (illimitées si le repo est public, 2 000 min/mois sinon ; un run dure ~2 min).

1. **Vérifier que les Actions sont actives :** *Settings → Actions → General → Allow all actions*.
2. **Rendre la CI obligatoire avant tout merge sur `main`** : *Settings → Branches → Add branch protection rule* (ou *Rules → Rulesets*) :
   - Branch name pattern : `main`
   - ☑ *Require a pull request before merging*
   - ☑ *Require status checks to pass* → chercher et cocher **`lint, tests, evals, attacks`** (le check apparaît après le premier run de la CI sur la PR)
   - ☐ ne pas cocher *Do not allow bypassing* si vous voulez garder un bouton d'urgence.
3. **Secret optionnel pour le juge LLM** : *Settings → Secrets and variables → Actions → New repository secret* → `ANTHROPIC_API_KEY`. Le workflow *LLM judge (manual)* ne tourne qu'à la main (*Actions → LLM judge → Run workflow*) et coûte quelques centimes.
4. Le secret existant `DEPLOY_REPO_TOKEN` ne change pas.

**Ce que fait la CI** (`.github/workflows/ci.yml`, identique à `make ci` en local) : lint Python, données front/serveur synchronisées, 144 tests Python (dont parité moteur JS ↔ Python et API), 39 tests d'interface, régression des 50 cas, **set d'attaques : un seul raté bloque la PR**.

**Ce qui change pour le déploiement** (`.github/workflows/sync-deploy.yml`) : la synchro vers le repo Vercel ne part plus à chaque push, mais **après une CI verte sur `main`**, puis lance un smoke test sur la prod. Si le smoke échoue, le run est rouge avec la marche à suivre (rollback).

## 2. Vercel — l'API Python (projet Vercel de Lenny : accès requis)

Le projet Vercel existant suffit : `vercel.json` déclare maintenant la fonction `api/index.py` (FastAPI, détectée automatiquement grâce à `requirements.txt`) et la règle `/api/* → api/index`. Le front statique ne change pas.

Dans *Vercel → projet `deploy-project-product-management` → Settings → Environment Variables*, ajouter (environnement **Production**, et **Preview** si vous voulez) :

| Variable | Valeur | Obligatoire ? |
|---|---|---|
| `ASSIST_MODE` | `on` | oui — position de l'interrupteur si PostHog n'est pas configuré |
| `FLOWASSIST_ENV` | `demo` | oui — tague toutes les données comme démo (référence avant lancement) |
| `POSTHOG_PROJECT_KEY` | la clé `phc_…` du projet PostHog (étape 3) | pour activer l'analytics et le flag |
| `POSTHOG_HOST` | `https://eu.i.posthog.com` | oui si PostHog |
| `POSTHOG_PERSONAL_API_KEY` | clé personnelle PostHog (scope *Feature flags: read*) | optionnel — évalue le flag localement, plus rapide |

Puis *Deployments → … → Redeploy* (les variables ne s'appliquent qu'aux nouveaux déploiements).

**Vérifier après le déploiement :**
- `https://deploy-project-product-management.vercel.app/api/health` → `{"status":"ok","engine_version":"0.6.0"}`
- `…/api/config` → `assist_mode` vaut `on`
- Onglet *Functions* / *Logs* : une ligne JSON par requête (`trace_id`, spans) = la trace du cours (S7).
- En local : `make smoke URL=https://deploy-project-product-management.vercel.app` → 6 × `ok`.

> ⚠️ Ne jamais mettre `ANTHROPIC_API_KEY` sur Vercel : le juge ne tourne pas en production.

## 3. PostHog — analytics et interrupteur global (Benjamin ou Anthony)

1. Créer un compte sur **https://eu.posthog.com** (région **EU**, important pour le RGPD) → nouveau projet `FlowAssist`.
2. Copier la **Project API key** (`phc_…`, publique par conception) → variable Vercel `POSTHOG_PROJECT_KEY` (étape 2).
3. **Créer l'interrupteur global** : *Feature flags → New feature flag*
   - Key : **`assist-mode`** (exactement)
   - Type : *Multiple variants* → variantes `on`, `suggest_only`, `off`
   - Release conditions : 100 % des utilisateurs → variante **`on`**
   - Save.
   > Tant que le flag n'existe pas alors que la clé est configurée, le serveur se met **par sécurité** en `suggest_only` (brouillons visibles, non insérables). C'est voulu (fail-safe).
4. **Créer le flag du futur A/B** (sans l'activer) : key `copilot-ab`, variantes `control` / `copilot`, 0 % de rollout.
5. **Dashboards** (*Dashboards → New*), à partir des événements listés dans `docs/TRACKING_PLAN.md` :
   - Funnel : `ticket_opened` → `source_inspected` → `draft_used` → `reply_recorded`
   - Tendance : `guardrail_blocked` et `check_failed` ventilés par `gate` / `codes`
   - p50 / p95 de `handling_ms` sur `reply_recorded`, ventilé par `language` puis `plan`
   - Taux de handover : `handover_recorded` / `ticket_opened`
   - Répartition `assist_mode`, et `api_unavailable` (couche infra)

**Utiliser l'interrupteur (rollback en < 1 min, sans redéploiement) :** *Feature flags → assist-mode* → passer la variante servie à `suggest_only` (on garde les brouillons visibles, plus d'insertion) ou `off` (mode humains seuls). Le serveur relit le flag toutes les 30 s. Propriétaire : Head of Payment Ops (le jour), ingénieur d'astreinte (la nuit) — voir `governance.md`.

## 4. Après le merge — checklist de validation

- [ ] La CI de la PR est verte (*Pull request → Checks*).
- [ ] Après le merge : *Actions* montre **CI** puis **Sync Vercel deployment repository**, les deux verts.
- [ ] `/api/health` renvoie `engine_version` = `0.6.0`.
- [ ] La démo affiche dans le bandeau « Assistant on · you approve every reply ».
- [ ] Un ticket ouvert dans la démo apparaît dans PostHog *Activity → Live events* **sans aucun texte de ticket**.
- [ ] Test de l'interrupteur : passer `assist-mode` à `suggest_only` → dans les 30 s, le bandeau change et « Use draft » est désactivé → revenir à `on`. **Noter la date du test dans `governance.md`** (exigé par le plan de rollback).

## En cas de problème

| Symptôme | Cause probable | Action |
|---|---|---|
| Bandeau « Assistant server unavailable » | `/api/*` ne répond pas (fonction non déployée ou erreur) | *Vercel → Logs*. Le front est volontairement fermé (fail-closed) : la démo reste utilisable en manuel. |
| Bandeau « suggest-only » alors que rien n'a été changé | clé PostHog configurée mais flag `assist-mode` absent ou PostHog injoignable | créer le flag (étape 3.3) |
| Le run *Sync Vercel* ne part pas | la CI a échoué, ou le workflow n'est pas encore sur `main` | corriger la CI ; *Run workflow* manuel possible |
| Smoke test rouge après déploiement | régression en prod | revert du commit sur `main` (la CI repasse et redéploie) **ou** `assist-mode` → `off` immédiatement |

Commandes locales utiles : `make install`, `make dev` (API + démo sur http://127.0.0.1:8000), `make ci`, `make smoke URL=…`, `make help`.
