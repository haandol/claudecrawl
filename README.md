# ClaudeCrawl

A web content scraper utilizing
[Playwright](https://playwright.dev) and [Claude LLM](https://claude.ai)
through [AWS Bedrock](https://aws.amazon.com/bedrock/)
to intelligently extract and structure data from web pages.

![Simple Overview](/docs/simple-overview.png)

## Features

- Intelligent web content extraction using Claude LLM
- Structured data output in JSONL format
- Configurable schema-based parsing
- AWS Bedrock integration
- Logging support

## Prerequisites

- Docker
- Python 3.13+
- AWS Account with Bedrock access
- AWS CLI configured

## Installation

1. Clone the repository:

```bash
git clone https://github.com/haandol/claude-web-scraper.git
cd claude-web-scraper
```

1. Install `uv`:

```bash
pip install uv
```

1. Install dependencies

```bash
uv sync
```

1. Install Playwright dependencies:

```bash
uv run playwright install
```

1. Configure environment variables:
   Create a `.env` file in the project root with:

```env
MODEL_ID=us.anthropic.claude-3-5-haiku-20241022-v1:0
AWS_PROFILE_NAME=your_profile_name
AWS_REGION=your_aws_region
```

## Usage

1. open `app.py` and modify `url`, `OutputSchema` and `instruction`

1. Run the scraper:

```bash
uv run -- python app.py
```

The script will:

- Crawl the specified data webpage
- Extract article information using Claude LLM
- Save the results in `output/output.jsonl`, unless you specify a different path.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](/LICENSE) file for details.
