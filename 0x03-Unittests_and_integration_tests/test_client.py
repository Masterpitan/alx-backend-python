#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch

"""Unit test for client.GitHubOrgClient"""
class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected result and calls get_json"""
        # Arrange: fake payload to return from get_json
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
