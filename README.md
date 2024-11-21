# Claude Web Scraper

A web content scraper utilizing Claude LLM (Language Learning Model) through AWS Bedrock to intelligently extract and structure data from web pages. Currently optimized for extracting League of Legends champion tactics articles.

## Features

- Intelligent web content extraction using Claude LLM
- Structured data output in JSONL format
- Configurable schema-based parsing
- AWS Bedrock integration
- Logging support

## Prerequisites

- Docker
- Python 3.12+
- AWS Account with Bedrock access
- AWS CLI configured

## Installation

1. Clone the repository:

```bash
git clone https://github.com/haandol/claude-web-scraper.git
cd claude-web-scraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:
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
python app.py
```

The script will:

- Crawl the specified data webpage
- Extract article information using Claude LLM
- Save the results in `output/output.jsonl`, unless you specify a different path.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.
