"""Unit tests for Powerk8s."""
from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from powerk8s import (
    KUBERNETES_LOGO,
    HighlightGroup,
    SegmentArg,
    SegmentData,
    get_kubernetes_logo,
    get_segment_args,
    powerk8s,
)

FILE_DIR: Path = Path(__file__).resolve().parent


class TestGetKubernetesLogo(unittest.TestCase):
    """Test getting the Kubernetes logo."""

    def test_simple(self: TestGetKubernetesLogo) -> None:
        """Simple test case for getting the Kubernetes logo."""
        self.assertEqual(
            get_kubernetes_logo(HighlightGroup.KUBERNETES_CLUSTER.value),
            SegmentData(
                KUBERNETES_LOGO,
                [HighlightGroup.KUBERNETES_CLUSTER.value],
                HighlightGroup.KUBERNETES_DIVIDER.value,
            ),
        )


class TestGetSegmentArgs(unittest.TestCase):
    """Test getting the segment arguments."""

    def test_simple(self: TestGetSegmentArgs) -> None:
        """Test getting segment args in a simple (most obvious) case."""
        self.assertEqual(
            get_segment_args(
                show_kube_logo=True,
                show_cluster=True,
                show_namespace=True,
                show_default_namespace=True,
            ),
            {
                SegmentArg.SHOW_KUBERNETES_LOGO: True,
                SegmentArg.SHOW_CLUSTER: True,
                SegmentArg.SHOW_NAMESPACE: True,
                SegmentArg.SHOW_DEFAULT_NAMESPACE: True,
            },
        )

    def test_missing(self: TestGetSegmentArgs) -> None:
        """Test missing segment arguments."""
        self.assertEqual(
            get_segment_args(show_cluster=True),
            {
                SegmentArg.SHOW_KUBERNETES_LOGO: None,
                SegmentArg.SHOW_CLUSTER: True,
                SegmentArg.SHOW_NAMESPACE: None,
                SegmentArg.SHOW_DEFAULT_NAMESPACE: None,
            },
        )


class TestPowerK8s(unittest.TestCase):
    """Test the Powerk8s entry point."""

    def setUp(self: TestPowerK8s) -> None:
        """Set up $KUBECONFIG and mock out pathlib.Path."""
        self.kube_config_yaml = open(f"{FILE_DIR}/fixtures/dummy_kubeconfig.yaml")

        self.mock_path: Mock = Mock(
            return_value=Mock(
                expanduser=Mock(
                    return_value=Mock(
                        open=Mock(
                            return_value=Mock(
                                __enter__=Mock(return_value=self.kube_config_yaml),
                                __exit__=Mock(return_value=False),
                            )
                        )
                    )
                )
            )
        )

    def tearDown(self: TestPowerK8s) -> None:
        """Close the file descriptor for $KUBECONFIG."""
        self.kube_config_yaml.close()

    def test_simple(self: TestPowerK8s) -> None:
        """Simple test case for powerk8s entry point."""
        with patch("powerk8s.Path", self.mock_path):
            self.assertEqual(
                powerk8s(show_cluster=True),
                [
                    {
                        "contents": "some-cluster",
                        "highlight_groups": ["kubernetes_cluster"],
                        "divider_highlight_group": "kubernetes_namespace",
                    }
                ],
            )

    def test_complete(self: TestPowerK8s) -> None:
        """More extensive, table-driven case coverage for Powerk8s entry point."""
        with patch("powerk8s.Path", self.mock_path):
            self.assertEqual(
                powerk8s(
                    show_kube_logo=True,
                    show_cluster=True,
                    show_namespace=True,
                    show_default_namespace=True,
                ),
                [
                    {
                        "contents": KUBERNETES_LOGO,
                        "highlight_groups": ["kubernetes_cluster"],
                        "divider_highlight_group": "kubernetes:divider",
                    },
                    {
                        "contents": "some-cluster",
                        "highlight_groups": ["kubernetes_cluster"],
                        "divider_highlight_group": "kubernetes_namespace",
                    },
                    {
                        "contents": "some-namespace",
                        "highlight_groups": ["kubernetes_cluster"],
                        "divider_highlight_group": "kubernetes_namespace",
                    },
                ],
            )


if __name__ == "__main__":
    unittest.main()
