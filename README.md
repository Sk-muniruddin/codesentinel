# CodeSentinel

## AI-Powered GitHub Pull Request Code Reviewer

CodeSentinel is an AI-powered GitHub App that automatically reviews Pull Requests and provides structured code-review feedback directly on GitHub.

It receives Pull Request webhook events, retrieves the Pull Request diff through the GitHub API, sends the changed code to an LLM for analysis, applies an authoritative review decision, and submits the result back to the Pull Request as a GitHub review.

---

## What Problem Does CodeSentinel Solve?

Code reviews are essential for identifying security vulnerabilities, logic errors, error-handling problems, and maintainability issues before code is merged.

CodeSentinel automates the first layer of review by analyzing Pull Request changes and identifying issues that materially affect the code.

The goal is not to replace human reviewers, but to provide an automated first-pass review that can surface important problems early.

---

## How It Works

```text
Developer creates or updates a Pull Request
                    |
                    v
            GitHub Pull Request
                    |
                    v
             GitHub Webhook
                    |
                    v
          CodeSentinel FastAPI
                    |
                    v
          GitHub App Authentication
                    |
                    v
             GitHub API
                    |
                    v
             Pull Request Diff
                    |
                    v
              Diff Parser
                    |
                    v
             AI Code Reviewer
                    |
                    v
           Structured CodeReview
                    |
                    v
          Authoritative Decision
                    |
                    v
          GitHub Pull Request Review
