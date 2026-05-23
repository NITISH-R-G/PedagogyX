# Cloud Architecture Report

**Status:** Draft v1.0
**Date:** 2026-05-20
**Role:** Senior Cloud Engineer & Cloud Infrastructure Architect

## 1. Cloud Problem Analysis

PedagogyX requires a hybrid environment: an edge presence in highly constrained, unreliable school networks, a control plane in AWS `ap-south-1` for strict DPDP compliance, and a pool of bare-metal GPU instances (to bypass prohibitive AWS GPU costs and meet the ₹0 hardware budget). Bridging these environments securely and reliably is the primary challenge.

## 2. Cloud Architecture

A multi-tier hybrid architecture.

- **Tier 1: The Edge.** Lightweight Docker/Podman environments on school LAN hardware buffering streams.
- **Tier 2: AWS Control Plane.** Managed EKS or ECS clusters hosting the stateless API layer, Web UI, and managed databases (RDS Postgres, MSK for Kafka/RabbitMQ).
- **Tier 3: Bare-Metal GPU Pool.** Dedicated unmanaged servers (e.g., RunPod, Lambda Labs, or colocation) running Docker Swarm. These nodes connect back to AWS via secure VPN tunnels to pull tasks and push artifacts.

## 3. Infrastructure Automation

- **IaC:** Terraform is used to provision all AWS resources, enforcing immutability and repeatability.
- **Configuration Management:** Ansible configures the bare-metal GPU nodes, installing necessary NVIDIA drivers, Docker, and the VPN client.

## 4. Networking Architecture

- **VPC Peering/VPN:** A WireGuard or Tailscale overlay network securely connects the ephemeral bare-metal GPU pool to the AWS VPC, ensuring ML traffic never traverses the public internet unencrypted.
- **Ingest Routing:** AWS Route 53 routes traffic from Edge nodes to the nearest/healthiest MediaMTX ingest gateway.
- **Egress Control:** Strict NAT gateways and Security Groups prevent bare-metal nodes from accessing arbitrary external IPs, mitigating supply chain attacks in the ML dependencies.

## 5. Reliability Strategy

- **Multi-AZ Deployment:** All control plane components in AWS `ap-south-1` are deployed across at least two Availability Zones.
- **GPU Node Ephemerality:** Bare-metal nodes are treated as cattle. If a GPU fails or the provider goes down, the Ansible scripts automatically provision a replacement node and join it to the Swarm/Tailnet.

## 6. Security Architecture

- **WAF:** AWS WAF protects the public API endpoints from standard DDoS and injection attacks.
- **IAM / RBAC:** Principle of least privilege. The GPU worker nodes only have S3/MinIO permissions to read `raw-media` and write to `ml-artifacts`. They have no access to the operational Postgres database.
- **Secrets Management:** AWS Secrets Manager injects API keys and DB credentials into containers at runtime.

## 7. Observability

- **Centralized Logging:** AWS CloudWatch for managed services, combined with a self-hosted Grafana Loki stack for unified logs across the Hybrid Edge and Bare-Metal pools.
- **Alerting:** PagerDuty integration triggered by Prometheus thresholds (e.g., VPN tunnel down, GPU utilization < 10% indicating a stalled queue).

## 8. Performance & Cost Optimization

- **Cost Avoidance:** Moving GPU workloads off AWS saves an estimated 70-80% on compute costs.
- **Spot Instances:** For non-critical control plane workers, AWS Spot Instances will be utilized.
- **Bandwidth:** Edge nodes compress video heavily (H.265 if supported) before uploading to reduce AWS ingress/egress costs.

## 9. Risks & Tradeoffs

- **Risk:** Managing bare-metal servers introduces significant operational overhead compared to a managed service like AWS SageMaker. **Tradeoff:** This is unavoidable to meet the strict financial constraints of the pilot phase while utilizing RTX 5070 class hardware. We mitigate via aggressive Ansible automation.

## 10. Agile Sprint Plan

- **Sprint 1:** Terraform the base AWS `ap-south-1` infrastructure (VPC, Subnets, RDS, ECS). Deploy a "Hello World" API.
- **Sprint 2:** Establish the secure overlay network (Tailscale/WireGuard). Manually provision one bare-metal GPU node and verify secure connection to AWS.
- **Sprint 3:** Automate GPU node provisioning with Ansible. Load test the network throughput between AWS MinIO and the bare-metal cluster.
