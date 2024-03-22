MKCERT_VERSION="v1.4.3"
MKCERT_BIN="mkcert"
MKCERT_URL="https://github.com/FiloSottile/mkcert/releases/download/${MKCERT_VERSION}/mkcert-${MKCERT_VERSION}-linux-amd64"
LOCAL_BIN=${HOME}/bin
UNAME=$(uname)

if [ "${UNAME}" = "Darwin" ]; then
  echo "Checking for mkcert installation..."
  if ! command -v mkcert &>/dev/null; then
    echo "mkcert not found, installing..."
    brew install mkcert
  else
    echo "mkcert is already installed."
  fi;
else
  if [ ! -e "${LOCAL_BIN}/${MKCERT_BIN}" ]; then
    echo "Downloading mkcert..."
    mkdir -p "${LOCAL_BIN}"
    curl -L "${MKCERT_URL}" -o "${MKCERT_BIN}"
    chmod +x "${MKCERT_BIN}"
    mv "${MKCERT_BIN}" "${LOCAL_BIN}"
  fi;
  export PATH="${LOCAL_BIN}:$PATH";
fi

mkcert -version