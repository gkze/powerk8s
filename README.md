# ☸️ powerk8s: Powerline Plugin for Kubernetes ☸️

This simple plugin is designed to show the Kubernetes cluster configured
for the current context in `$KUBECONFIG`.

This work is inspired by https://github.com/so0k/powerline-kubernetes,
and intends to be a drop-in **replacement** as well as an improvement upon the original work.

## Installation

For the time being, `powerk8s` can be installed directly from GitHub:

```bash
$ pip3 install https://github.com/gkze/powerk8s/archive/master.tar.gz 
```

Or, if you prefer SSH:

```bash
$ pip3 install git+ssh://git@github.com/gkze/powerk8s
```

## Configuration

Just like with [so0k/powerline-kubernetes], you'll need a few things to get going:

* **Colorschemes**

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

  Here is a good starting point:

  ```json
  {
    "function": "powerline_kubernetes.kubernetes",
    "priority": 30,
    "args": {
        "show_kube_logo": true, // set to false to omit the Kube logo
        "show_cluster": true, // show cluster name
        "show_namespace": true, // show namespace name
        "show_default_namespace": false, // do not show namespace name if it's "default"
        "alerts": [
          "live", // show line in different color when namespace matches
          "cluster:live"  // show line in different color when cluster name and namespace match
        ]
    }
  }
  ```

# Authors

[@gkze](https://github.com/gkze)

# License

[MIT](LICENSE)
