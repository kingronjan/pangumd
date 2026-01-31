#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Get Current Version ---
# Using grep and cut to extract the version string from pyproject.toml
CURRENT_VERSION=$(grep -E "^version = \"[0-9]+\.[0-9]+\.[0-9]+\"$" pyproject.toml | cut -d '"' -f 2)

if [ -z "$CURRENT_VERSION" ]; then
  echo "Error: Could not find current version in pyproject.toml"
  exit 1
fi

# --- Validation ---
if [ -z "$1" ]; then
  echo "Error: No version specified, current version is $CURRENT_VERSION"
  echo "Usage: ./release.sh <version>"
  exit 1
fi

NEW_VERSION=$1
echo "Releasing version $NEW_VERSION..."

echo "Current version: $CURRENT_VERSION, New version: $NEW_VERSION"

# --- Update Version in Files ---
echo "Updating version in pyproject.toml, pangumd.py, and README.md..."

# pyproject.toml
sed -i "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

# pangumd.py
sed -i "s/^__version__ = '$CURRENT_VERSION'/__version__ = '$NEW_VERSION'/" pangumd.py

# README.md
sed -i "s/rev: $CURRENT_VERSION/rev: $NEW_VERSION/" README.md

echo "Files updated."

# --- Git Commit and Push ---
echo "Committing and pushing changes..."

# Stage the changes
git add pyproject.toml pangumd.py README.md

# Commit the changes
git commit -m "chore: Bump version to $NEW_VERSION"

# Tag the commit
git tag "$NEW_VERSION"

# Push the commit and tag
git push origin main
git push origin "$NEW_VERSION"

echo ""
echo "Version $NEW_VERSION released successfully!"
echo "Check the GitHub Actions tab for the publish status."
