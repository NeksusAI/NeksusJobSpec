# Get Started

## Installation

Install from PyPI:

```bash
pip install neksus-jobspec
```

Or install from local repository:

```bash
pip install -e .[dev]
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
```

### 5. Run project checks

```bash
neksus-jobspec check
```

### 6. Export schema

```bash
neksus-jobspec spec schema --output schemas/jobspec.v1.json
```
