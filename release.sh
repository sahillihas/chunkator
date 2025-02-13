#!/bin/bash

# Checking if the working directory is clean
git status --porcelain | grep -q . && echo "Error: Working directory is not clean!" && exit 1

# Step 1: Bump the version (You can change patch to minor or major based on your needs)
echo "Bumping version..."
bumpversion patch  # Use patch, minor, or major

# Step 2: Get the current version tag (e.g., v0.0.5)
VERSION=$(git describe --tags --abbrev=0)
if [ -z "$VERSION" ]; then
  echo "Error: No version found, please check your tags"
  exit 1
fi

# Step 3: Create the new release tag
RELEASE_TAG="${VERSION}-release"
echo "Creating tag: $RELEASE_TAG"
git tag "$RELEASE_TAG"

# Step 4: Push the new tag to GitHub
echo "Pushing tag to GitHub..."
git push origin "$RELEASE_TAG"

# Step 5: Trigger CI/CD workflow
echo "Triggering GitHub Actions workflow..."
git push origin --tags

echo "Release process completed successfully!"
