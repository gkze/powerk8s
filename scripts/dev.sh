#!/bin/bash
set -eo pipefail

declare -r JQ_EXE="jq"
declare -r POETRY_EXE="poetry"
declare -ar REQUIRED_EXES=("${JQ_EXE}" "python" "${POETRY_EXE}")

declare -r VSCODE_DEFAULT_SETTINGS=".vscode/settings.default.json"
declare -r VSCODE_SETTINGS=".vscode/settings.json"

poetry_install() {
  printf "Installing Python dependencies with Poetry...\n"
  "${POETRY_EXE}" install
}

vscode_python_path() {
  printf "Configuring Poetry Python path for VS Code...\n"
  "${JQ_EXE}" -r ".\"python.pythonPath\" = \"$(poetry env info -p | sed "s#$HOME#\${env:HOME}#g")\"" "${VSCODE_DEFAULT_SETTINGS}" >"${VSCODE_SETTINGS}"
}

check_exes() {
  for exe in "${REQUIRED_EXES[@]}"; do
    if ! command >/dev/null -v "${exe}"; then
      printf "%s is missing - please ensure it is installed.\n" "${exe}"
    fi
  done
}

main() {
  check_exes
  poetry_install
  vscode_python_path
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
