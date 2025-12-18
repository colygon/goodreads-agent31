# CrewAI Upgrade Documentation

## Overview

This document describes the CrewAI enhancement to the Goodreads Analysis App. The upgrade introduces AI-powered agents that provide personalized insights and recommendations based on user reading data.

## Agent 31 Upgrade

**Agent ID**: 31
**Project**: Goodreads Analysis App
**Repository**: https://github.com/tylerjrichards/streamlit_goodreads_app
**Upgrade Date**: December 2025

## What's New

### AI-Powered Reading Insights

The upgraded application now features three specialized CrewAI agents equipped with the CSVSearchTool that work together to analyze your Goodreads reading history and provide intelligent, personalized insights:

### CSVSearchTool Integration

All agents are now equipped with CrewAI's CSVSearchTool, which enables them to:
- Query the complete book reading history database (books_read.csv)
- Search and analyze specific fields like ratings, dates, authors, and book metadata
- Perform detailed data exploration for more accurate and comprehensive insights
- Access real-time book data instead of relying solely on pre-computed summaries

#### 1. Reading Pattern Analyst Agent
- **Role**: Analyzes reading patterns, habits, and trends
- **Tools**: CSVSearchTool for querying books_read.csv
- **Capabilities**:
  - Identifies temporal reading patterns and trends using read_at and started_at fields
  - Analyzes reading speed and volume through book.num_pages data
  - Evaluates rating behaviors and preferences from rating field
  - Spots interesting habits in reading behavior across multiple dimensions
  - Queries publication years to understand historical reading preferences
- **Output**: 3-5 key insights about reading behavior and patterns

#### 2. Genre & Diversity Specialist Agent
- **Role**: Evaluates diversity of reading choices
- **Tools**: CSVSearchTool for querying books_read.csv
- **Capabilities**:
  - Analyzes author demographics using book.authors.author.name and author_gender fields
  - Assesses variety in publication eras through book.publication_year data
  - Identifies author variety and repeat authors via book.authors.author.id
  - Infers genres and themes from book titles and descriptions
  - Evaluates popular vs niche choices using book.average_rating
  - Identifies potential blind spots in reading choices
  - Provides thoughtful, non-judgmental feedback
- **Output**: Diversity assessment with 2-3 specific suggestions for expanding literary horizons

#### 3. Personalized Book Recommender Agent
- **Role**: Generates tailored book recommendations
- **Tools**: CSVSearchTool for querying books_read.csv
- **Capabilities**:
  - Analyzes highest-rated books using the rating field
  - Identifies favorite authors from book.authors.author.name
  - Determines preferred book lengths via book.num_pages
  - Understands publication year preferences from book.publication_year
  - Identifies current reading interests through read_at_year patterns
  - Matches reading preferences with new suggestions
  - Considers writing style, themes, pacing, and emotional tone
  - Provides diverse recommendations across genres
  - Explains why each recommendation fits the reader's profile
- **Output**: 3 specific book recommendations with personalized explanations

## Technical Implementation

### New Files

#### `book_agents.py`
Contains the CrewAI agent definitions and orchestration logic:
- `BookAnalysisAgents` class: Container for all three agents
- Individual agent factory methods for each specialist
- `analyze_reading_data()`: Main orchestration method
- `get_ai_insights()`: Convenience function for easy integration

#### Updated Files

#### `books.py`
Enhanced with new AI insights section:
- Import of `get_ai_insights` function
- New "AI-Powered Reading Insights" section
- Interactive button to trigger agent analysis
- Display of comprehensive insights from all three agents

#### `requirements.txt`
Added CrewAI dependencies:
- `crewai>=0.86.0` - Multi-agent orchestration framework
- `crewai-tools>=0.12.0` - CrewAI tools including CSVSearchTool
- `langchain-openai>=0.3.0` - OpenAI integration for LLM capabilities

## Setup and Configuration

### Prerequisites

1. Python 3.8 or higher
2. OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/goodreads-agent31.git
cd goodreads-agent31

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The AI agents require an OpenAI API key to function. Configure it using one of these methods:

#### Method 1: Streamlit Secrets (Recommended for deployment)
Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your-api-key-here"
goodreads_key = "your-goodreads-key"
```

#### Method 2: Environment Variable (For local development)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Running the Application

```bash
streamlit run books.py
```

## Features

### Original Features (Preserved)
- Goodreads profile scraping and analysis
- Books read by year visualization
- Book age and publication year analysis
- Rating behavior analysis
- Book length distribution
- Reading speed analysis
- Gender breakdown of authors
- Book list recommendations from famous readers

### New CrewAI Features
- **AI-Powered Reading Pattern Analysis**: Deep insights into reading habits
- **Diversity Assessment**: Thoughtful evaluation of reading breadth
- **Personalized Recommendations**: AI-curated book suggestions
- **Interactive Analysis**: On-demand generation of insights
- **Multi-Agent Collaboration**: Three specialized agents working in concert
- **CSVSearchTool Integration**: Agents can directly query and analyze the complete book database for enhanced accuracy

## Usage

1. Enter your Goodreads profile URL or select a sample profile
2. Review the standard analytics (reading history, patterns, ratings, etc.)
3. Scroll to the "AI-Powered Reading Insights" section
4. Click "Generate AI Insights" button
5. Wait for the AI agents to analyze your data (typically 30-60 seconds)
6. Review the personalized insights from each agent:
   - Reading patterns and habits
   - Diversity assessment
   - Book recommendations

## Architecture

### Agent Workflow

```
User Reading Data (DataFrame)
         ↓
BookAnalysisAgents.analyze_reading_data()
         ↓
    ┌────┴────┬────────────┐
    ↓         ↓            ↓
Pattern    Diversity   Recommender
Analyst    Specialist    Agent
    ↓         ↓            ↓
    └────┬────┴────────────┘
         ↓
  Consolidated Insights
         ↓
   Streamlit Display
```

### Agent Communication

- Each agent runs independently via CrewAI's `Crew` orchestration
- Agents use `Process.sequential` for predictable execution
- Results are aggregated in a dictionary for display
- No inter-agent delegation to maintain focused expertise

## Technical Details

### CSVSearchTool Configuration
- **Tool**: CrewAI's CSVSearchTool
- **Data Source**: books_read.csv (automatically generated from Goodreads data)
- **Capabilities**:
  - Semantic search across all book data fields
  - Natural language queries for data exploration
  - Real-time data access for each agent
  - Supports queries on ratings, dates, authors, titles, publication info, and more
- **Integration**: All three agents are equipped with the tool for autonomous data exploration

### Available CSV Fields for Agent Queries
The CSVSearchTool has access to comprehensive book data including:
- **Book Information**: book.title, book.title_without_series, book.num_pages, book.publication_year
- **Author Data**: book.authors.author.name, book.authors.author.id, author_gender
- **Reading Data**: read_at, read_at_year, started_at, rating
- **Metadata**: book.average_rating, book.ratings_count, book.description
- **And many more fields** from the Goodreads export

### LLM Configuration
- **Default Model**: GPT-4o-mini (configurable)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Framework**: LangChain with OpenAI integration

### Data Processing
- Agents receive both summarized statistics and CSV query access
- CSVSearchTool allows agents to explore specific data points on-demand
- Privacy-conscious: data remains local, only queries and results sent to LLM
- Efficient: combines summary statistics with targeted CSV searches
- Enhanced accuracy: agents can verify insights against actual data

### Error Handling
- Graceful degradation if API key is missing
- Informative error messages for troubleshooting
- Fallback to original features if AI analysis fails

## Performance Considerations

- **Analysis Time**: 30-90 seconds depending on data complexity
- **API Costs**: Approximately $0.01-0.03 per analysis with GPT-4o-mini
- **Caching**: Results are not cached; re-analysis generates fresh insights

## Future Enhancements

Potential areas for expansion:
- Session state caching of AI insights
- Additional specialized agents (e.g., Literary Analysis Expert)
- Comparative analysis between multiple readers
- Time-series pattern recognition
- Integration with more book data sources
- Additional CrewAI tools (e.g., WebSearchTool for finding new book releases)
- Custom CSV queries based on user-defined criteria

## Limitations

- Requires OpenAI API key (paid service)
- Analysis quality depends on completeness of Goodreads data
- Gender detection algorithms have known biases and limitations
- Recommendations are AI-generated and may not always be perfect

## Contributing

Contributions are welcome! Areas of interest:
- Additional agent types
- Enhanced data analysis capabilities
- Alternative LLM provider support
- Performance optimizations
- UI/UX improvements

## Credits

- **Original Application**: Tyler Richards (https://www.tylerjrichards.com)
- **CrewAI Upgrade**: Agent 31
- **Framework**: CrewAI by CrewAI Inc.
- **UI Framework**: Streamlit

## License

This project maintains the original license from the upstream repository.

## Support

For issues or questions:
- Original app issues: See original repository
- CrewAI upgrade issues: Create issue on forked repository
- CrewAI framework: https://docs.crewai.com

## Version History

### v2.1.0 (CSVSearchTool Enhancement)
- Integrated CSVSearchTool into all three agents
- Enhanced agent capabilities with direct CSV database querying
- Improved accuracy of insights through data-driven analysis
- Updated requirements with crewai-tools>=0.12.0

### v2.0.0 (CrewAI Upgrade)
- Added three specialized CrewAI agents
- Integrated AI-powered insights section
- Updated dependencies for LLM support
- Enhanced requirements with crewai>=0.86.0 and langchain-openai>=0.3.0

### v1.0.0 (Original)
- Initial Goodreads analysis application
- Basic reading statistics and visualizations
- Author gender analysis
- Book list recommendations
