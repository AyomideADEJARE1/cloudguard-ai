from unittest.mock import Mock

from backend.app.aws_scanner import scan_security_groups


def test_detects_public_ssh_access():
    ec2 = Mock()
    ec2.describe_security_groups.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-demo123",
                "GroupName": "demo-web",
                "IpPermissions": [
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 22,
                        "ToPort": 22,
                        "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                        "Ipv6Ranges": [],
                    }
                ],
            }
        ]
    }

    findings = scan_security_groups(ec2)

    assert len(findings) == 1
    assert findings[0]["severity"] == "HIGH"
    assert findings[0]["id"] == "AWS-SSH-sg-demo123"
    assert "IPv4" in findings[0]["issue"]


def test_ignores_restricted_ssh_access():
    ec2 = Mock()
    ec2.describe_security_groups.return_value = {
        "SecurityGroups": [
            {
                "GroupId": "sg-restricted",
                "GroupName": "private-web",
                "IpPermissions": [
                    {
                        "IpProtocol": "tcp",
                        "FromPort": 22,
                        "ToPort": 22,
                        "IpRanges": [{"CidrIp": "203.0.113.10/32"}],
                        "Ipv6Ranges": [],
                    }
                ],
            }
        ]
    }

    assert scan_security_groups(ec2) == []


def test_returns_no_findings_for_empty_account():
    ec2 = Mock()
    ec2.describe_security_groups.return_value = {"SecurityGroups": []}

    assert scan_security_groups(ec2) == []
