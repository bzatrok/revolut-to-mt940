#!/bin/bash
set -e

# Check for uncommitted changes
if git diff-index --quiet HEAD --; then
    echo "No uncommitted changes, ready to proceed."
else
    echo "There are uncommitted changes. Please commit them before proceeding."
    exit 1
fi

# Get version from package.jso
PACKAGE_VERSION=$(python -c "import version; print(version.VERSION)")
echo "Package version: $PACKAGE_VERSION"

# Docker repository settings
DOCKER_USERNAME="amberglass"
DOCKER_IMAGE_NAME="revolut-mt940"
DOCKER_REPO="$DOCKER_USERNAME/$DOCKER_IMAGE_NAME"

# Login to Docker Hub using 1password CLI
if command -v op &> /dev/null; then
    if ! op account get > /dev/null 2>&1; then
        eval $(op signin)
    fi
    
    # Get Docker credentials
    DOCKER_PASSWORD=$(op item get "goc4y6fiobfjrmqw4yojs5l4ue" --format json | jq -r '.fields[] | select(.id=="credential").value')

    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
else
    echo "1Password CLI (op) not found. Please install it first."
    exit 1
fi

# Build and tag Docker image
docker build \
    --platform=linux/amd64 \
    -t $DOCKER_REPO:latest \
    -t $DOCKER_REPO:$PACKAGE_VERSION \
    .

# Push Docker images
docker push $DOCKER_REPO:latest
docker push $DOCKER_REPO:$PACKAGE_VERSION

# Clean up
docker image rm $DOCKER_REPO:latest
docker image rm $DOCKER_REPO:$PACKAGE_VERSION

# Logout from Docker Hub
docker logout

echo "Successfully built and pushed version $PACKAGE_VERSION"