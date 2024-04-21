# LLM Workflow Engine (LWE) OpenRouter Provider plugin

OpenRouter Provider plugin for [LLM Workflow Engine](https://github.com/llm-workflow-engine/llm-workflow-engine)

Access to [OpenRouter](https://openrouter.ai/models) models.
## Installation

### From packages

Install the latest version of this software directly from github with pip:

```bash
pip install git+https://github.com/llm-workflow-engine/lwe-plugin-provider-openrouter
```

### From source (recommended for development)

Install the latest version of this software directly from git:

```bash
git clone https://github.com/llm-workflow-engine/lwe-plugin-provider-openrouter.git
```

Install the development package:

```bash
cd lwe-plugin-provider-openrouter
pip install -e .
```

## Configuration

Add the following to `config.yaml` in your profile:

```yaml
plugins:
  enabled:
    - provider_openrouter
    # Any other plugins you want enabled...
```

## Usage

From a running LWE shell:

```
/provider openrouter
/model model_name openai/gpt-3.5-turbo
```
