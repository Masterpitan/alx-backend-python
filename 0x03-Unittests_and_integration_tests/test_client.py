#!/usr/bin/env python3
"""We start by importing modules needed"""
import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock, Mock
from fixtures import TEST_PAYLOAD

"""Unit test for client.GitHubOrgClient
define a class and functions"""

PARAMS = [
    {
        "org_payload": org,
        "repos_payload": repos,
        "expected_repos": expected,
        "apache2_repos": apache
    }
    for org, repos, expected, apache in TEST_PAYLOAD
]

@parameterized_class(PARAMS)
class TestGithubOrgClient(unittest.TestCase):
    """This is unittest for TestGithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org calls json,
            and returns result expected"""
        """Arrange: fake payload to return from get_json"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Act
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert
        self.assertEqual(result, expected_payload)
        url_display = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(url_display)

    """Defining the functions"""
    def test_public_repos_url(self):
        """Test that _public_repos_url
        returns mocked repos_url"""
        repos_url = "https://api.github.com/orgs/test_org/repos"
        test_payload = {"repos_url": repos_url}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("test_org")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method
        with mocked payload and URL"""
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://fake-url.com"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://fake-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license static method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

    @classmethod
    def setUpClass(cls):
        """Set up class-level patch for get_json to return test payloads"""
        cls.get_patcher = patch('client.get_json')
        cls.mock_get_json = cls.get_patcher.start()

        # Directly return dictionaries, not mock response objects
        cls.mock_get_json.side_effect = [
            cls.org_payload,     # for self.org
            cls.repos_payload    # for self.repos_payload
        ]


    @classmethod
    def tearDownClass(cls):
        """Stop patching"""
        cls.get_patcher.stop()


    def test_public_repos(self):
        """Test something using self.org_payload, etc."""

        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)
