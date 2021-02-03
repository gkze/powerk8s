# ☸️ powerk8s: Powerline Plugin for Kubernetes ☸️

[![Actions Test Workflow Widget](https://github.com/gkze/powerk8s/workflows/ci/badge.svg)](https://github.com/gkze/powerk8s/actions?query=workflow%3Aci)
[![PyPI Version](https://img.shields.io/pypi/v/powerk8s)](https://pypi.org/project/powerk8s/)
[![Pdoc Documentation](https://img.shields.io/badge/pdoc-docs-green)](https://gkze.github.io/powerk8s/powerk8s.html)

This simple plugin is designed to show the Kubernetes cluster configured
for the current context in `$KUBECONFIG`.

This work is inspired by [so0k/powerline-kubernetes](https://github.com/so0k/powerline-kubernetes),
and intends to be a drop-in **replacement** as well as an improvement upon the original work.

## Installation

```bash
$ pip3 install powerk8s
```

## Configuration

Just like with [so0k/powerline-kubernetes](https://github.com/so0k/powerline-kubernetes), you'll need a few things to get going:

* **Colorschemes**

  `~/.config/powerline/colorschemes/default.json`:

  ```json
  {
    "groups": {
      "kubernetes_cluster":         { "fg": "gray10", "bg": "darkestblue", "attrs": [] },
      "kubernetes_cluster:alert":   { "fg": "gray10", "bg": "darkestred",  "attrs": [] },
      "kubernetes_namespace":       { "fg": "gray10", "bg": "darkestblue", "attrs": [] },
      "kubernetes_namespace:alert": { "fg": "gray10", "bg": "darkred",     "attrs": [] },
      "kubernetes:divider":         { "fg": "gray4",  "bg": "darkestblue", "attrs": [] },
    }
  }
  ```

* **`powerk8s` invocation (& arguments)**

  Here is a good starting point.
  `~/.config/powerline/themes/shell/default.json`:

  ```json
  {
    "function": "powerline_kubernetes.kubernetes",
    "priority": 30,
    "args": {
        "show_kube_logo": true,
        "show_cluster": true,
        "show_namespace": true,
        "show_default_namespace": false,
        "alerts": [
          "live",
          "cluster:live"
        ]
    }
  }
  ```

  This will add the segment to the shell.
  Alternatively, placing this in `~/.config/powerline/colorschemes/default.json`
  will make it show up in the Tmux status line.

## Authors

[@gkze](https://github.com/gkze)

## License

[MIT](LICENSE)
