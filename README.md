# Speedtype
TUI for training typing speed.

## What is Speedtype?
Main features of *Speedtype*:
- Train your typing speed. Configure a text with various settings: language, time, word length, etc., and feel free to start improving your typing skills.

And all of this is running inside your terminal!

## Setup

--

## Development
This section is intended only for developing the *Speedtype*. If you only want to install the application, go to the [Setup](#Setup) section.

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) installed
- [`just`](https://github.com/casey/just) installed

### Initialize the project
1. Clone the repository
2. Run `just init`

### Development conventions

#### Developing
1. Checkout from the `main` a new branch with the following name `<feature/bugfix/task>/<short description>`.
   2. How to choose what to specify: *feature*, *bugfix* or *task*:
      - *feature* - adds a new functionality to the end users - it is what they will see when *Speedtype* is launched.
      - *bugfix* - fixing the bug that occurs in the *Speedtype*
      - *task* - anything else: updating *README*, adding new tests, configuring linters, etc.
2. Do some changes...
3. Push the branch to the `origin`
4. Create PR

#### Pull requests
- Merge request's title must follow the next structure `<feature/bugfix/task>: <short description>`.
- Merge request's body must contain the following sections
  - *What was done* - description of what was changed/added/removed.
  - *Issues* - link to the issue which will be resolved after PR is merged.
  - *Attachments* (optional) - contains the additional attachments: photo, videos, etc.
- Apply only the ***squash and merge*** strategy when merging changes into the `main` branch.
  - Add PR description into the merge request's `Extended description`.
- After the PR is merged, delete the original branch.
