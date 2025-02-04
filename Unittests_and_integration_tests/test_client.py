#!/usr/bin/env python3
"""Unit tests for the client module."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from requests.exceptions import HTTPError
from fixtures import TEST_PAYLOAD

# Define your fixtures directly in this file as a workaround
org_payload = {"repos_url": "test_repos_url"}
repos_payload = [
    {"name": "repo1", "license": {"key": "my_license"}},
    {"name": "repo2", "license": {"key": "other_license"}}
]
expected_repos = ["repo1", "repo2"]
apache2_repos = ["repo1"]  # Modify as needed


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org."""
        mock_get_json.return_value = {"payload": True}
        test_instance = GithubOrgClient(org_name)
        self.assertEqual(test_instance.org, {"payload": True})
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url method."""
        json_payload = {"repos_url": "test_url"}
        mock_org.return_value = json_payload
        test_instance = GithubOrgClient("test_org")
        result = test_instance._public_repos_url
        self.assertEqual(result, json_payload["repos_url"])

    @patch('client.get_json')
    @patch(
        'client.GithubOrgClient._public_repos_url',
        new_callable=PropertyMock
    )
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test public_repos method."""
        mock_public_repos_url.return_value = "test_url"
        mock_get_json.return_value = repos_payload
        test_instance = GithubOrgClient("test_org")
        result = test_instance.public_repos()
        expected_names = [repo['name'] for repo in repos_payload]
        self.assertEqual(result, expected_names)
        mock_get_json.assert_called_once_with("test_url")
        mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for the GithubOrgClient.public_repos method."""
    @classmethod
    def setUpClass(cls):
        """Set up resources before any test cases are run."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            Mock(status_code=200, json=lambda: org_payload),
            Mock(status_code=200, json=lambda: repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Clean up resources after all test cases have been run."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method in an integration test scenario."""
        test_instance = GithubOrgClient("test_org")
        self.assertEqual(test_instance.public_repos(), expected_repos)


if __name__ == '__main__':
    unittest.main()
