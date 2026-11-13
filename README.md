# CareGuard Health — DevSecOps Demonstration

A responsive, demo-only healthcare operations dashboard built with Flask. This is the application component for a DevSecOps coursework project.

## Features
- Responsive healthcare operations dashboard
- Summary cards and recent activity feed
- `/health` endpoint for container/Kubernetes health checks
- `/api/summary` JSON endpoint
- Non-root Docker container and Docker health check
- Jenkins pipeline example with Trivy filesystem and image scans

> **Safety note:** All data is fictional and aggregate. Do not enter, upload, or store real patient information. This is not a certified medical system and does not implement production-grade identity, authorization, encryption, audit, or regulatory controls. The security score shown in the UI is illustrative, not a real scan result.

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

## Run with Docker
```powershell
docker build -t careguard-health:local .
docker run --rm -p 5000:5000 careguard-health:local
```
Open http://localhost:5000

## Trivy scans
Install Trivy, then:
```powershell
trivy fs --scanners vuln,misconfig,secret --severity HIGH,CRITICAL .
trivy image --severity HIGH,CRITICAL careguard-health:local
```
Review findings and remediate them; do not blindly suppress results.

## Jenkins setup
1. Push this project to a GitHub repository.
2. Create a separate Jenkins Pipeline job.
3. Configure Jenkins credential ID `dockerhub-creds` as username/password. Use your Docker Hub username and a Docker Hub access token with push permissions.
4. Install Trivy and Docker CLI on the Jenkins agent and ensure both are on PATH.
5. Run the pipeline. Image publishing runs only on the `main` branch.

The pipeline intentionally stops after image publishing. Add Kubernetes deployment only after scan policy and cluster credentials are configured.
