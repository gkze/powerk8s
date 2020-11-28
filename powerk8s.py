from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence

import yaml
from kubernetes.config.kube_config import (  # type: ignore
    KUBE_CONFIG_DEFAULT_LOCATION,
    KubeConfigLoader,
)
from powerline import PowerlineLogger  # type: ignore

KUBERNETES_LOGO: str = "\U00002388 "


class SegmentArg(Enum):
    SHOW_KUBERNETES_LOGO: str = "show_kube_logo"
    SHOW_CLUSTER: str = "show_cluster"
    SHOW_NAMESPACE: str = "show_namespace"
    SHOW_DEFAULT_NAMESPACE: str = "show_default_namespace"


class HighlightGroup:
    KUBERNETES_CLUSTER_ALERT: str = "kubernetes_cluster:alert"
    KUBERNETES_CLUSTER: str = "kubernetes_cluster"
    KUBERNETES_DIVIDER: str = "kubernetes:divider"
    KUBERNETES_NAMESPACE_ALERT: str = "kubernetes_namespace:alert"
    KUBERNETES_NAMESPACE: str = "kubernetes_namespace"


@dataclass
class SegmentData:
    contents: Optional[str]
    highlight_groups: List[str]
    divider_highlight_group: Optional[str] = field(default="")


def get_kubernetes_logo(color: str) -> SegmentData:
    return SegmentData(KUBERNETES_LOGO, [color], HighlightGroup.KUBERNETES_DIVIDER)


def get_segment_args(**kwargs: Mapping[str, Any]) -> Mapping[SegmentArg, Any]:
    return {sa: kwargs.get(sa.value, None) for sa in SegmentArg}


def powerk8s(
    *args: List[Any], **kwargs: Mapping[str, Any]
) -> Sequence[Mapping[str, str]]:
    segment_args: Mapping[SegmentArg, Any] = get_segment_args(**kwargs)

    pl: PowerlineLogger = None
    if "pl" in kwargs:
        pl = kwargs["pl"]

    cfg: KubeConfigLoader = None
    with Path(KUBE_CONFIG_DEFAULT_LOCATION).expanduser().open() as f:
        cfg = KubeConfigLoader(yaml.load(f, Loader=yaml.SafeLoader))

    if pl is not None:
        pl.debug(f"Context: {cfg.current_context}")
        pl.debug(f"Segment arguments: {segment_args}")

    segments: List[SegmentData] = []

    if segment_args.get(SegmentArg.SHOW_KUBERNETES_LOGO, False):
        segments.extend([get_kubernetes_logo(HighlightGroup.KUBERNETES_CLUSTER)])

    if segment_args.get(SegmentArg.SHOW_CLUSTER, False):
        segments.extend(
            [
                SegmentData(
                    contents=cfg.current_context["context"]["cluster"],
                    highlight_groups=[HighlightGroup.KUBERNETES_CLUSTER],
                    divider_highlight_group=HighlightGroup.KUBERNETES_NAMESPACE,
                )
            ]
        )

    if (
        segment_args.get(SegmentArg.SHOW_DEFAULT_NAMESPACE, False)
        and "namespace" in cfg.current_context["context"]
    ):
        segments.extend(
            [
                SegmentData(" ", [HighlightGroup.KUBERNETES_DIVIDER]),
                SegmentData(
                    contents=cfg.current_context["context"]["namespace"],
                    highlight_groups=[HighlightGroup.KUBERNETES_CLUSTER],
                    divider_highlight_group=HighlightGroup.KUBERNETES_NAMESPACE,
                ),
            ]
        )

    return list(map(asdict, segments))
