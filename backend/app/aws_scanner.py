import os

import boto3


def scan_security_groups(ec2_client=None) -> list[dict]:
    """Find EC2 security groups exposing SSH to the public internet."""
    if ec2_client is None:
        region = (
            os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        )
        ec2_client = boto3.client("ec2", region_name=region)

    findings = []
    response = ec2_client.describe_security_groups()

    for group in response.get("SecurityGroups", []):
        public_sources = set()

        for permission in group.get("IpPermissions", []):
            protocol = permission.get("IpProtocol")
            from_port = permission.get("FromPort")
            to_port = permission.get("ToPort")

            exposes_ssh = protocol == "-1" or (
                protocol == "tcp"
                and from_port is not None
                and to_port is not None
                and from_port <= 22 <= to_port
            )

            if not exposes_ssh:
                continue

            for item in permission.get("IpRanges", []):
                if item.get("CidrIp") == "0.0.0.0/0":
                    public_sources.add("IPv4")

            for item in permission.get("Ipv6Ranges", []):
                if item.get("CidrIpv6") == "::/0":
                    public_sources.add("IPv6")

        if public_sources:
            group_id = group["GroupId"]
            sources = " and ".join(sorted(public_sources))

            findings.append(
                {
                    "id": f"AWS-SSH-{group_id}",
                    "resource": (f"{group.get('GroupName', 'unnamed')} ({group_id})"),
                    "severity": "HIGH",
                    "issue": (f"SSH may be publicly accessible over {sources}"),
                    "recommendation": (
                        "Restrict inbound SSH access to trusted IP addresses "
                        "or use AWS Systems Manager Session Manager. "
                        "Review the security-group rules before making changes."
                    ),
                }
            )

    return findings
