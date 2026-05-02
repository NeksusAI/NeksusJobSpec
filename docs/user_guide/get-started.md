# Get Started

## Installation

Install from PyPI:

```bash
pip install neksus-jobspec
```

Or install from local repository:

```bash
uv sync
```

## Quick Start

### 1. Initialize a project

```bash
neksus-jobspec init
```

### 2. Create a JobSpec

```bash
neksus-jobspec spec new backend-engineer
```

### 3. Validate the JobSpec

```bash
neksus-jobspec spec validate jobspecs/backend-engineer.jobspec.yaml
```

### 4. Render outputs

```bash
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format markdown --output dist/backend-engineer.md
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format html --output dist/backend-engineer.html
neksus-jobspec spec render jobspecs/backend-engineer.jobspec.yaml --format json --output dist/backend-engineer.json
```

### 5. Run project checks

```bash
neksus-jobspec check
neksus-jobspec check --format github
```

### 6. Batch render project specs

```bash
neksus-jobspec render --format markdown
```

### 7. Export schema

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
```
