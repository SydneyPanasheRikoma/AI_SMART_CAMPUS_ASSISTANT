"""
Sentiment Analyzer for detecting complaint urgency
Uses TextBlob for sentiment analysis
"""
from textblob import TextBlob
from typing import Dict, Tuple
import re


class SentimentAnalyzer:
    """
    Analyzes sentiment of complaints to detect urgency level
    Negative sentiment = Higher urgency
    """
    
    def __init__(self):
        # Keywords that indicate high urgency
        self.urgent_keywords = [
            'urgent', 'immediately', 'asap', 'emergency', 'critical',
            'serious', 'severe', 'dangerous', 'broken', 'not working',
            'failed', 'unable', 'cannot', 'stuck', 'blocked', 'help',
            'please', 'very', 'extremely', 'terrible', 'worst', 'awful'
        ]
        
        # Keywords that indicate issues/problems
        self.problem_keywords = [
            'issue', 'problem', 'trouble', 'difficulty', 'concern',
            'complaint', 'error', 'fault', 'defect', 'malfunction'
        ]
    
    def analyze_sentiment(self, text: str) -> Tuple[float, float]:
        """
        Analyze sentiment of text
        
        Returns:
            Tuple of (polarity, subjectivity)
            - polarity: -1 (negative) to 1 (positive)
            - subjectivity: 0 (objective) to 1 (subjective)
        """
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity, blob.sentiment.subjectivity
        except:
            # Fallback if TextBlob fails
            return 0.0, 0.5
    
    def detect_urgent_keywords(self, text: str) -> int:
        """
        Count urgent keywords in text
        """
        text_lower = text.lower()
        count = 0
        
        for keyword in self.urgent_keywords:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.findall(pattern, text_lower)
            count += len(matches)
        
        return count
    
    def calculate_urgency_score(self, text: str) -> float:
        """
        Calculate urgency score based on sentiment and keywords
        
        Returns:
            Score between 0 and 1 (higher = more urgent)
        """
        # Get sentiment
        polarity, subjectivity = self.analyze_sentiment(text)
        
        # Count urgent keywords
        urgent_count = self.detect_urgent_keywords(text)
        
        # Calculate base urgency from negative sentiment
        # More negative = more urgent
        sentiment_urgency = max(0, -polarity)  # Convert negative polarity to positive urgency
        
        # Add keyword boost (each keyword adds urgency)
        keyword_boost = min(urgent_count * 0.15, 0.5)  # Cap at 0.5
        
        # Add subjectivity factor (more subjective = more urgent for complaints)
        subjectivity_factor = subjectivity * 0.2
        
        # Combine factors
        urgency_score = min(sentiment_urgency + keyword_boost + subjectivity_factor, 1.0)
        
        return urgency_score
    
    def determine_priority(self, text: str, manual_priority: str = None) -> str:
        """
        Determine priority level based on sentiment analysis
        
        Args:
            text: Complaint text
            manual_priority: User-selected priority (optional)
        
        Returns:
            Priority level: 'High', 'Medium', or 'Low'
        """
        # If manual priority is provided, use it
        if manual_priority and manual_priority in ['High', 'Medium', 'Low']:
            return manual_priority
        
        # Calculate urgency score
        urgency = self.calculate_urgency_score(text)
        
        # Map urgency to priority
        if urgency >= 0.6:
            return 'High'
        elif urgency >= 0.3:
            return 'Medium'
        else:
            return 'Low'
    
    def analyze_complaint(self, text: str, manual_priority: str = None) -> Dict:
        """
        Complete sentiment analysis of a complaint
        
        Returns:
            Dictionary with sentiment metrics and priority
        """
        polarity, subjectivity = self.analyze_sentiment(text)
        urgency = self.calculate_urgency_score(text)
        priority = self.determine_priority(text, manual_priority)
        urgent_keywords = self.detect_urgent_keywords(text)
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'urgency_score': urgency,
            'priority': priority,
            'urgent_keyword_count': urgent_keywords,
            'sentiment': 'negative' if polarity < -0.1 else 'positive' if polarity > 0.1 else 'neutral'
        }


# Global analyzer instance
analyzer = SentimentAnalyzer()


def analyze_complaint_sentiment(text: str, manual_priority: str = None) -> Dict:
    """
    Convenience function to analyze complaint sentiment
    """
    return analyzer.analyze_complaint(text, manual_priority)
