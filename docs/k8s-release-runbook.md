# DeepSeek V4 Paper Release Runbook

## Deployment Mapping

- GitHub repository: `gateszhangc/deepseek-v4-paper`
- Git branch: `main`
- Dokploy project: `none`
- Image repository: `registry.144.91.77.245.sslip.io/deepseek-v4-paper`
- K8s manifest path: `deploy/k8s/overlays/prod`
- Argo CD application: `deepseek-v4-paper`
- Primary domain: `deepseekv4paper.lol`
- Preview URL: `https://deepseek-v4-paper.144.91.77.245.sslip.io/`

GitHub repository -> branch -> image repository -> K8s manifest path -> Argo CD application  
`gateszhangc/deepseek-v4-paper -> main -> registry.144.91.77.245.sslip.io/deepseek-v4-paper -> deploy/k8s/overlays/prod -> deepseek-v4-paper`

## What This Repo Owns

- `Dockerfile`: static Node runtime image for the site.
- `.github/workflows/build-and-release.yml`: GitHub Actions workflow that submits a Kaniko build `Job` into the `build-jobs` namespace, waits for completion, and writes the released SHA back into `deploy/k8s/overlays/prod/kustomization.yaml`.
- `deploy/k8s/base`: deployment, service, live ingress, `www` redirect ingress, preview ingress, and production certificate.
- `deploy/argocd/application.yaml`: standalone Argo CD `Application` pointing at this repository. This is intentionally not wired to Dokploy.

## Required GitHub Secret

- `KUBECONFIG_B64`: base64-encoded kubeconfig with access to `build-jobs`, `argocd`, and the target application namespace.

The workflow assumes the repository is readable by the cluster build job over public HTTPS. Keep the repo public unless you also add a repo-read token secret path for the init container.

## One-Time Bootstrap

1. Push the repo to `main`.
2. Add `KUBECONFIG_B64` to the GitHub repository secrets.
3. Apply the Argo CD application once:

```bash
kubectl apply -f deploy/argocd/application.yaml
```

4. Delegate DNS to Cloudflare and create the live records:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR="${WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR:-$CODEX_HOME/skills/webapp-launch-analytics}"
export PRIMARY_URL="https://deepseekv4paper.lol"
export DNS_TARGET_APEX_IP="144.91.77.245"
export DNS_TARGET_WWW="deepseekv4paper.lol"
export PORKBUN_NS_MODE="api"

bash "$WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR/scripts/ensure-cloudflare-dns.sh" deepseekv4paper.lol
```

5. After the live domain resolves and `https://deepseekv4paper.lol/` returns the site, configure Google Search Console:

```bash
export PRIMARY_URL="https://deepseekv4paper.lol"
export SKIP_GA4="true"
export SKIP_CLARITY="true"

bash "$WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR/scripts/setup-gsc.sh" deepseekv4paper.lol
bash "$WEBAPP_LAUNCH_ANALYTICS_SKILL_DIR/scripts/check-gsc-property.sh" deepseekv4paper.lol
```

## Release Flow

1. Push to `main`.
2. GitHub Actions submits a `Job` to `build-jobs`.
3. The job clones the repository at the pushed SHA and builds the Docker image with Kaniko.
4. The workflow updates `newTag` in `deploy/k8s/overlays/prod/kustomization.yaml`.
5. The workflow commits the tag bump back to `main`.
6. Argo CD auto-syncs the overlay and rolls the deployment.

## Verification Gates

- `kubectl -n argocd get application deepseek-v4-paper`
- `curl -I https://deepseekv4paper.lol/`
- `curl -I https://deepseekv4paper.lol/robots.txt`
- `curl -I https://deepseekv4paper.lol/sitemap.xml`
- Playwright browser tests in this repo must pass before release is considered done.
