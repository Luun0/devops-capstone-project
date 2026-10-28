# Customer Accounts Service — IBM DevOps Capstone

[![CI Build](https://github.com/Luun0/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg)](https://github.com/Luun0/devops-capstone-project/actions/workflows/ci-build.yaml)

A customer accounts REST microservice with Flask, PostgreSQL, automated tests,
GitHub Actions CI, Talisman, CORS, Docker, Kubernetes and Tekton CD.

Based on the [official IBM starter template](https://github.com/ibm-developer-skills-network/aolwx-devops-capstone-template).
Original IBM copyright and Apache-2.0 license are retained. CRUD completion,
security configuration, additional tests and deployment automation were added for this project.

## API

- `POST /accounts`: create an account; returns 201 and a readable Location header.
- `GET /accounts`: list accounts; optional `?name=` exact-name filter.
- `GET /accounts/<id>`: read an account, or 404.
- `PUT /accounts/<id>`: replace customer fields, or 400/404/415.
- `DELETE /accounts/<id>`: idempotent deletion, returns 204.
- `GET /health`: readiness and liveness response.

Account JSON fields: name, email, address, optional phone_number and date_joined (ISO date).

## Run and test

The course requires legacy `nosetests`; Python 3.9 is used for compatibility.
This course environment is intended for demonstration; update Python and migrate
from nose before production use.

```sh
python3.9 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URI=sqlite:////tmp/accounts.db
flake8 service tests
nosetests
gunicorn --bind 0.0.0.0:8080 service:app
```

Tests use disposable databases. PostgreSQL is used by GitHub Actions and the
Kubernetes deployment. Never run the test suite against production data.

## Container and Kubernetes

```sh
docker build -t accounts:1.0 .
docker run --rm -p 8080:8080 -e DATABASE_URI=sqlite:////tmp/accounts.db accounts:1.0
```

Create a Kubernetes secret named `accounts-db` with `password` and `uri` keys;
URI format: `postgresql://postgres:PASSWORD@postgres:5432/accounts`.
Load `accounts:1.0` into your local cluster, then apply `k8s/postgres.yaml` and
`k8s/accounts.yaml`. The app runs as UID 10001 with two replicas and health probes.
Use `kubectl port-forward service/accounts 8080:8080` for local access.

## Continuous delivery

Install Tekton Pipelines and apply `tekton/rbac.yaml`, `tekton/tasks.yaml`,
`tekton/pipeline.yaml`. Create a run with `kubectl create -f tekton/run.yaml`.
The pipeline clones this repository, installs dependencies, lints, runs nosetests
with a 95% coverage gate, builds/pushes a Docker image and waits for Kubernetes rollout.

The local demonstration uses a dedicated kind cluster and an HTTP development
registry (`k8s/registry-local.yaml`). Configure the kind node's registry host
mapping before running CD. The privileged Docker-in-Docker builder and this
local registry are for the isolated lab environment. Production should use an
authenticated TLS registry and a builder appropriate for its security policy.

CORS allows `https://example.com` by default; override with comma-separated
`CORS_ORIGINS`. Set `FORCE_HTTPS=true` behind an HTTPS ingress in production.

## Planning and evidence

[GitHub project](https://github.com/users/Luun0/projects/1).
Issues use sprint milestones, estimates, labels and acceptance criteria.
Actual command output is saved under `evidence/`.
