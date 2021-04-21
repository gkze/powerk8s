"""Unit tests for Powerk8s."""
from __future__ import annotations

import unittest
from pathlib import Path

from powerk8s import (
    KUBERNETES_LOGO,
    HighlightGroup,
    SegmentArg,
    SegmentData,
    get_kubernetes_logo,
    get_segment_args
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


if __name__ == "__main__":
    unittest.main()
