"""
AI-powered paper summarization with multi-provider support
"""
import json
import re
from typing import Dict, Tuple
import config


class AISummarizer:
    """Handles paper summarization using various AI providers"""

    def __init__(self, provider: str = None):
        """
        Initialize AI summarizer

        Args:
            provider: AI provider to use (gemini, openai, claude, grok)
        """
        self.provider = provider or config.AI_PROVIDER
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate AI client based on provider"""
        if self.provider == "gemini":
            self._initialize_gemini()
        elif self.provider == "openai":
            self._initialize_openai()
        elif self.provider == "claude":
            self._initialize_claude()
        elif self.provider == "grok":
            self._initialize_grok()
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _initialize_gemini(self):
        """Initialize Google Gemini client"""
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.client = genai.GenerativeModel('gemini-2.5-flash')
        print(f"Initialized Gemini API client")

    def _initialize_openai(self):
        """Initialize OpenAI client"""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        from openai import OpenAI
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        print(f"Initialized OpenAI API client")

    def _initialize_claude(self):
        """Initialize Anthropic Claude client"""
        if not config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        from anthropic import Anthropic
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        print(f"Initialized Claude API client")

    def _initialize_grok(self):
        """Initialize Grok client"""
        if not config.GROK_API_KEY:
            raise ValueError("GROK_API_KEY not found in environment variables")

        from openai import OpenAI
        # Grok uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=config.GROK_API_KEY,
            base_url="https://api.x.ai/v1"
        )
        print(f"Initialized Grok API client")

    def check_relevance(self, paper: Dict) -> Tuple[bool, float, str]:
        """
        Check if paper is relevant to medicine/health using AI

        Args:
            paper: Paper dictionary with title and abstract

        Returns:
            Tuple of (is_relevant, relevance_score, reasoning)
        """
        prompt = f"""Analyze if this research paper is relevant to medicine, healthcare, health, biosecurity, or medical AI/applications.

Title: {paper['title']}

Abstract: {paper['abstract']}

Primary Category: {paper['primary_category']}
Categories: {', '.join(paper['categories'])}

Respond in JSON format:
{{
    "is_relevant": true/false,
    "relevance_score": 0.0-1.0,
    "reasoning": "brief explanation",
    "medical_domains": ["list", "of", "relevant", "medical", "domains"],
    "ai_health_application": "describe AI application to health if applicable"
}}

Be strict: only mark as relevant if there's clear connection to medicine, health, biosecurity, or medical AI applications."""

        try:
            response_text = self._call_ai(prompt)
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return (
                    result.get('is_relevant', False),
                    result.get('relevance_score', 0.0),
                    result.get('reasoning', ''),
                    result.get('medical_domains', []),
                    result.get('ai_health_application', '')
                )
            else:
                print(f"Warning: Could not parse AI response as JSON")
                return False, 0.0, "Failed to parse response", [], ""

        except Exception as e:
            print(f"Error checking relevance: {e}")
            return False, 0.0, f"Error: {e}", [], ""

    def summarize_paper(self, paper: Dict) -> Dict:
        """
        Generate comprehensive summary of a paper

        Args:
            paper: Paper dictionary with title, abstract, etc.

        Returns:
            Dictionary with summary, bullet points, keywords, etc.
        """
        prompt = f"""Analyze and summarize this medical/health research paper in detail.

Title: {paper['title']}

Authors: {', '.join(paper['authors'][:5])}{'...' if len(paper['authors']) > 5 else ''}

Abstract: {paper['abstract']}

Primary Category: {paper['primary_category']}
All Categories: {', '.join(paper['categories'])}

Provide a comprehensive analysis in JSON format:
{{
    "summary": "2-3 sentence overview of the paper's main contribution and findings",
    "key_points": [
        "5-7 specific bullet points covering methodology, results, and implications"
    ],
    "medical_relevance": "Why this matters for medicine/health (1-2 sentences)",
    "keywords": ["list", "of", "5-8", "relevant", "keywords"],
    "medical_domains": ["specific", "medical", "fields"],
    "methodology": "Brief description of methods used",
    "key_findings": "Main results or discoveries",
    "clinical_impact": "Potential clinical or practical impact",
    "limitations": "Any noted limitations or caveats",
    "future_directions": "Suggested future research directions if mentioned"
}}

Be specific, technical, and focus on practical medical/health implications."""

        try:
            response_text = self._call_ai(prompt)
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                summary = json.loads(json_match.group())
                return summary
            else:
                print(f"Warning: Could not parse summary as JSON")
                return self._generate_fallback_summary(paper)

        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._generate_fallback_summary(paper)

    def _call_ai(self, prompt: str) -> str:
        """
        Call the configured AI provider with a prompt

        Args:
            prompt: The prompt to send

        Returns:
            AI response text
        """
        if self.provider == "gemini":
            response = self.client.generate_content(prompt)
            return response.text

        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content

        elif self.provider == "claude":
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif self.provider == "grok":
            response = self.client.chat.completions.create(
                model="grok-beta",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _generate_fallback_summary(self, paper: Dict) -> Dict:
        """Generate a basic fallback summary if AI fails"""
        return {
            "summary": paper['abstract'][:300] + "...",
            "key_points": ["See abstract for details"],
            "medical_relevance": "Medical/health related research",
            "keywords": paper.get('categories', []),
            "medical_domains": [paper.get('primary_category', 'Unknown')],
            "methodology": "See paper for methodology",
            "key_findings": "See abstract",
            "clinical_impact": "Potential clinical applications",
            "limitations": "Not analyzed",
            "future_directions": "Not analyzed"
        }
