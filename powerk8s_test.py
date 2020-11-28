from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

import kubernetes.config.kube_config  # type: ignore

from powerk8s import (
    KUBERNETES_LOGO,
    HighlightGroup,
    SegmentArg,
    SegmentData,
    get_kubernetes_logo,
    get_segment_args,
    powerk8s,
)


class TestGetKubernetesLogo(unittest.TestCase):
    def test_simple(self: TestGetKubernetesLogo) -> None:
        self.assertEqual(
            get_kubernetes_logo(HighlightGroup.KUBERNETES_CLUSTER),
            SegmentData(
                KUBERNETES_LOGO,
                [HighlightGroup.KUBERNETES_CLUSTER],
                HighlightGroup.KUBERNETES_DIVIDER,
            ),
        )


class TestGetSegmentArgs(unittest.TestCase):
    def test_simple(self: TestGetSegmentArgs) -> None:
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
    def setUp(self: TestPowerK8s) -> None:
        self.kube_config_loader: Mock = Mock(
            return_value=Mock(
                current_context={
                    "context": {
                        "cluster": "some-cluster",
                        "namespace": "some-namespace",
                    }
                }
            )
        )
        self.original_kube_config_loader: kubernetes.config.kube_config.KubeConfigLoader = (
            kubernetes.config.kube_config.KubeConfigLoader
        )
        kubernetes.config.kube_config.KubeConfigLoader = self.kube_config_loader

    def test_simple(self: TestPowerK8s) -> None:
        with patch("powerk8s.KubeConfigLoader", self.kube_config_loader), patch("powerk8s.Path"):
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
        with patch("powerk8s.KubeConfigLoader", self.kube_config_loader), patch("powerk8s.Path"):
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
