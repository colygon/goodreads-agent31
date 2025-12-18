"""
Book Analysis Agents using CrewAI
This module defines specialized agents for analyzing reading habits and book data.
"""

from crewai import Agent, Task, Crew, Process
from crewai_tools import CSVSearchTool
from langchain_openai import ChatOpenAI
import pandas as pd
from typing import Dict, List, Optional
import os


class BookAnalysisAgents:
    """Container class for book analysis agents using CrewAI"""

    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.7, csv_path: str = "books_read.csv"):
        """
        Initialize the LLM and tools for all agents

        Args:
            model: The OpenAI model to use
            temperature: Temperature setting for the LLM
            csv_path: Path to the books CSV file for CSVSearchTool
        """
        self.llm = ChatOpenAI(model=model, temperature=temperature)
        self.csv_path = csv_path
        self.csv_tool = None

        # Initialize CSVSearchTool if CSV file exists
        if os.path.exists(csv_path):
            self.csv_tool = CSVSearchTool(csv=csv_path)

    def reading_pattern_analyst(self) -> Agent:
        """
        Agent specialized in analyzing reading patterns and habits.
        Focuses on temporal patterns, reading speed, and volume analysis.
        """
        tools = [self.csv_tool] if self.csv_tool else []
        return Agent(
            role="Reading Pattern Analyst",
            goal="Analyze reading patterns, habits, and trends from book data to provide insights into reading behavior",
            backstory="""You are an expert data analyst specializing in reading habits and patterns.
            You excel at identifying trends in reading frequency, book completion times, and seasonal
            reading behaviors. You can spot interesting patterns in when and how people read, and provide
            actionable insights to help readers understand their habits better. You have access to a CSV
            search tool that allows you to query the complete book reading history database for detailed
            analysis of ratings, dates, book metadata, and reading patterns.""",
            llm=self.llm,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )

    def genre_diversity_specialist(self) -> Agent:
        """
        Agent specialized in analyzing genre diversity and author demographics.
        Focuses on diversity metrics, genre distribution, and author backgrounds.
        """
        tools = [self.csv_tool] if self.csv_tool else []
        return Agent(
            role="Genre & Diversity Specialist",
            goal="Evaluate the diversity of reading choices including genres, author demographics, and publication eras",
            backstory="""You are a literary diversity consultant with deep knowledge of book genres,
            publishing history, and author demographics. You help readers understand the breadth and
            diversity of their reading choices, identify potential blind spots, and suggest ways to
            expand their literary horizons. You're particularly skilled at analyzing representation
            in reading lists and providing thoughtful, non-judgmental feedback. You have access to a CSV
            search tool that allows you to query the complete book reading database to analyze author
            demographics, publication years, genres, and diversity metrics across the entire reading history.""",
            llm=self.llm,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )

    def personalized_recommender(self) -> Agent:
        """
        Agent specialized in generating personalized book recommendations.
        Focuses on matching reading preferences with new book suggestions.
        """
        tools = [self.csv_tool] if self.csv_tool else []
        return Agent(
            role="Personalized Book Recommender",
            goal="Generate highly personalized book recommendations based on reading history and preferences",
            backstory="""You are a seasoned book curator and recommendation specialist with an
            encyclopedic knowledge of literature across all genres. You excel at understanding
            individual reading tastes and finding the perfect next book based on patterns in what
            someone has enjoyed before. You consider not just genre preferences, but also writing
            style, themes, pacing, and emotional tone. Your recommendations are always thoughtful,
            diverse, and tailored to help readers discover their next favorite book. You have access
            to a CSV search tool that allows you to query the complete reading history to understand
            user preferences based on their ratings, favorite authors, book lengths, and reading patterns.""",
            llm=self.llm,
            tools=tools,
            verbose=True,
            allow_delegation=False
        )

    def analyze_reading_data(
        self,
        df: pd.DataFrame,
        user_name: str,
        analysis_type: str = "comprehensive"
    ) -> Dict[str, str]:
        """
        Run CrewAI analysis on reading data

        Args:
            df: DataFrame containing book reading data
            user_name: Name of the user being analyzed
            analysis_type: Type of analysis ('patterns', 'diversity', 'recommendations', 'comprehensive')

        Returns:
            Dictionary containing analysis results from each agent
        """

        # Prepare summary statistics for agents
        total_books = len(df)
        unique_authors = len(df['book.authors.author.name'].unique())
        avg_rating = df[df['rating'].isin(['1','2','3','4','5'])]['rating'].astype(float).mean()

        # Get sample of recent books
        recent_books = df.nlargest(10, 'read_at')['book.title_without_series'].tolist() if 'read_at' in df.columns else df.head(10)['book.title_without_series'].tolist()

        data_summary = f"""
        User: {user_name}
        Total Books Read: {total_books}
        Unique Authors: {unique_authors}
        Average Rating Given: {avg_rating:.2f}
        Recent Books: {', '.join(recent_books[:5])}
        """

        results = {}

        # Reading Pattern Analysis
        if analysis_type in ['patterns', 'comprehensive']:
            pattern_agent = self.reading_pattern_analyst()
            pattern_task = Task(
                description=f"""Analyze the reading patterns for this user based on their Goodreads data:
                {data_summary}

                Use the CSV search tool to query the books_read.csv file for detailed analysis.
                You can search for patterns in:
                - Reading dates (read_at, read_at_year, started_at) to analyze temporal patterns
                - Book ratings to understand rating behavior
                - Book lengths (book.num_pages) for reading volume analysis
                - Publication years (book.publication_year) to see historical preferences
                - Any other relevant fields in the CSV

                Focus on:
                - Reading frequency and volume trends
                - Preferred book lengths and complexity
                - Rating patterns and preferences
                - Any notable habits or patterns

                Provide 3-5 key insights about their reading behavior.""",
                agent=pattern_agent,
                expected_output="A concise analysis with 3-5 bullet points highlighting the most interesting reading patterns and habits"
            )

            pattern_crew = Crew(
                agents=[pattern_agent],
                tasks=[pattern_task],
                process=Process.sequential,
                verbose=True
            )

            results['patterns'] = pattern_crew.kickoff()

        # Genre & Diversity Analysis
        if analysis_type in ['diversity', 'comprehensive']:
            diversity_agent = self.genre_diversity_specialist()

            # Extract author gender info if available
            gender_info = ""
            if 'author_gender' in df.columns:
                gender_dist = df['author_gender'].value_counts()
                gender_info = f"\nAuthor Gender Distribution: {gender_dist.to_dict()}"

            diversity_task = Task(
                description=f"""Evaluate the diversity of reading choices for this user:
                {data_summary}
                {gender_info}

                Use the CSV search tool to query the books_read.csv file for diversity analysis.
                You can search for:
                - Author demographics (book.authors.author.name, author_gender if available)
                - Publication years (book.publication_year) to analyze era diversity
                - Author variety and repeat authors (book.authors.author.id)
                - Book titles and descriptions to infer genres and themes
                - Average ratings (book.average_rating) to understand popular vs niche choices

                Focus on:
                - Diversity of authors (gender, background if known)
                - Range of publication years and eras
                - Variety in book types and themes
                - Areas for potential expansion

                Provide encouraging feedback and 2-3 suggestions for broadening reading horizons.""",
                agent=diversity_agent,
                expected_output="A supportive analysis highlighting reading diversity strengths and 2-3 specific suggestions for expanding literary horizons"
            )

            diversity_crew = Crew(
                agents=[diversity_agent],
                tasks=[diversity_task],
                process=Process.sequential,
                verbose=True
            )

            results['diversity'] = diversity_crew.kickoff()

        # Personalized Recommendations
        if analysis_type in ['recommendations', 'comprehensive']:
            recommender_agent = self.personalized_recommender()

            # Get top-rated books
            top_books = df[df['rating'].isin(['4','5'])].nlargest(5, 'rating')['book.title_without_series'].tolist() if not df.empty else []

            rec_task = Task(
                description=f"""Generate personalized book recommendations for this user:
                {data_summary}

                Their favorite books include: {', '.join(top_books[:5]) if top_books else 'No ratings available'}

                Use the CSV search tool to query the books_read.csv file to understand their preferences.
                You can search for:
                - Highest-rated books (rating field) to understand what they love
                - Favorite authors (book.authors.author.name) for author preferences
                - Preferred book lengths (book.num_pages)
                - Publication year preferences (book.publication_year)
                - Reading patterns (read_at_year) to identify current interests

                Provide:
                - 3 specific book recommendations with brief explanations
                - Why each book matches their reading profile
                - How each recommendation helps them explore something new

                Make recommendations diverse and thoughtful.""",
                agent=recommender_agent,
                expected_output="Three specific book recommendations with titles, authors, and personalized explanations for why each book would appeal to this reader"
            )

            rec_crew = Crew(
                agents=[recommender_agent],
                tasks=[rec_task],
                process=Process.sequential,
                verbose=True
            )

            results['recommendations'] = rec_crew.kickoff()

        return results


def get_ai_insights(df: pd.DataFrame, user_name: str, analysis_type: str = "comprehensive") -> Dict[str, str]:
    """
    Convenience function to get AI-powered insights from book data

    Args:
        df: DataFrame containing book reading data
        user_name: Name of the user being analyzed
        analysis_type: Type of analysis to perform

    Returns:
        Dictionary with analysis results
    """
    agents = BookAnalysisAgents()
    return agents.analyze_reading_data(df, user_name, analysis_type)
