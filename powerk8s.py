from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import yaml
from kubernetes.config.kube_config import KUBE_CONFIG_DEFAULT_LOCATION, KubeConfigLoader
from powerline import PowerlineLogger

KUBERNETES_LOGO: str = "\U00002388 "


class HighlightGroup:
    KUBERNETES_CLUSTER_ALERT: str = "kubernetes_cluster:alert"
    KUBERNETES_CLUSTER: str = "kubernetes_cluster"
    KUBERNETES_DIVIDER: str = "kubernetes:divider"
    KUBERNETES_NAMESPACE_ALERT: str = "kubernetes_namespace:alert"
    KUBERNETES_NAMESPACE: str = "kubernetes_namespace"


@dataclass
class SegmentData:
    contents: Optional[str]
    highlight_groups: Sequence[str]
    divider_highlight_group: Optional[str] = field(default="")


def get_kubernetes_logo(color: str) -> SegmentData:
    return SegmentData(KUBERNETES_LOGO, [color], HighlightGroup.KUBERNETES_DIVIDER)


def powerk8s(
    *args: Sequence[Any], **kwargs: Mapping[str, Any]
) -> Sequence[SegmentData]:
    pl: PowerlineLogger = None
    if "pl" in kwargs:
        pl: PowerlineLogger = kwargs["pl"]

    with Path(KUBE_CONFIG_DEFAULT_LOCATION).expanduser().open() as f:
        cfg: KubeConfigLoader = KubeConfigLoader(yaml.load(f, Loader=yaml.SafeLoader))
        current_cluster: str = cfg.current_context["context"]["cluster"]

        if pl is not None:
            pl.debug(f"Current Kubernetes cluster: {current_cluster}")

        return [
            asdict(
                SegmentData(
                    contents=cfg.current_context["context"]["cluster"],
                    highlight_groups=[HighlightGroup.KUBERNETES_CLUSTER],
                    divider_highlight_group=HighlightGroup.KUBERNETES_NAMESPACE,
                )
            )
        ]
