#!/usr/bin/env bash
set -e

# Create build environment if needed
if [ ! -d ".build_env" ]; then
    echo "Creating build environment..."
    python3 -m venv .build_env
fi

# Move original python binaries
if [ ! -f ".build_env/bin/python3.real" ]; then
    echo "Wrapping python3 binary to filter --user flag..."
    mv .build_env/bin/python3 .build_env/bin/python3.real
fi

# Create python3 wrapper script
cat << 'EOF' > .build_env/bin/python3
#!/usr/bin/env bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$1" == "-m" && "$2" == "pip" ]]; then
    args=()
    for arg in "$@"; do
        if [ "$arg" != "--user" ]; then
            args+=("$arg")
        fi
    done
    exec "$DIR/python3.real" "${args[@]}"
fi
exec "$DIR/python3.real" "$@"
EOF

chmod +x .build_env/bin/python3
ln -sf python3 .build_env/bin/python

# Ensure VIRTUAL_ENV environment variable is explicitly exported
export VIRTUAL_ENV="$(pwd)/.build_env"
export PATH="$(pwd)/.build_env/bin:$PATH"

echo "Build environment ready with python3 wrapper"
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo "PATH: $PATH"

# Add your p4a build commands here
# Example:
# p4a apk --requirements=python3,kivy --private . --package=com.example.app --name "App" --version 0.1
