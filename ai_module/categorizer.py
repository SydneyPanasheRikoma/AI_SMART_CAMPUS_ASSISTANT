"""
AI Module for complaint categorization using NLP
Uses keyword-based classification with NLTK
"""
import re
from typing import Dict, List, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class ComplaintCategorizer:
    """
    NLP-based complaint categorizer
    Uses keyword matching and text analysis to classify complaints
    """
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
        
        # Category keywords mapping
        self.category_keywords = {
            'IT Issues': [
                'internet', 'wifi', 'network', 'computer', 'laptop', 'lab',
                'software', 'hardware', 'printer', 'projector', 'system',
                'server', 'website', 'portal', 'login', 'password', 'slow',
                'connection', 'download', 'upload', 'screen', 'mouse', 'keyboard'
            ],
            'Hostel Management': [
                'hostel', 'room', 'accommodation', 'mess', 'food', 'canteen',
                'warden', 'cleanliness', 'maintenance', 'water', 'electricity',
                'bed', 'mattress', 'bathroom', 'toilet', 'hot water', 'cold water',
                'roommate', 'noise', 'hygiene', 'laundry', 'dining'
            ],
            'Academics': [
                'exam', 'test', 'marks', 'grades', 'faculty', 'professor',
                'teacher', 'course', 'class', 'lecture', 'syllabus', 'schedule',
                'timetable', 'attendance', 'assignment', 'project', 'lab report',
                'curriculum', 'subject', 'semester', 'academic', 'study'
            ],
            'Administration': [
                'certificate', 'document', 'bonafide', 'admission', 'registration',
                'fee', 'payment', 'scholarship', 'id card', 'transcript',
                'verification', 'office', 'application', 'form', 'approval',
                'process', 'department', 'staff', 'administration', 'official'
            ],
            'Library': [
                'library', 'book', 'reference', 'journal', 'reading room',
                'librarian', 'borrow', 'return', 'due date', 'fine', 'catalog',
                'search', 'database', 'e-book', 'digital', 'photocopy',
                'study space', 'quiet', 'hours', 'membership'
            ],
            'Sports & Recreation': [
                'sports', 'playground', 'field', 'court', 'gym', 'fitness',
                'basketball', 'football', 'cricket', 'volleyball', 'equipment',
                'recreation', 'athletic', 'tournament', 'game', 'physical',
                'exercise', 'coach', 'training', 'facility'
            ],
            'Other': []
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess complaint text
        - Convert to lowercase
        - Remove special characters
        - Tokenize
        - Remove stopwords
        - Stem words
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Tokenize
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple split if NLTK tokenizer fails
            tokens = text.split()
        
        # Remove stopwords and stem
        processed_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                stemmed = self.stemmer.stem(token)
                processed_tokens.append(stemmed)
        
        return processed_tokens
    
    def calculate_category_scores(self, tokens: List[str]) -> Dict[str, float]:
        """
        Calculate matching scores for each category
        """
        scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            # Stem category keywords
            stemmed_keywords = [self.stemmer.stem(kw.lower()) for kw in keywords]
            
            # Count matches
            for token in tokens:
                if token in stemmed_keywords:
                    score += 1
            
            scores[category] = score
        
        return scores
    
    def categorize(self, complaint_text: str, manual_category: str = None) -> Tuple[str, float]:
        """
        Categorize a complaint using NLP
        
        Args:
            complaint_text: The complaint description
            manual_category: User-selected category (optional)
        
        Returns:
            Tuple of (predicted_category, confidence_score)
        """
        # If manual category is provided and valid, use it with high confidence
        if manual_category and manual_category in self.category_keywords:
            return manual_category, 0.95
        
        # Preprocess text
        tokens = self.preprocess_text(complaint_text)
        
        # Calculate scores
        scores = self.calculate_category_scores(tokens)
        
        # Find best match
        max_score = max(scores.values())
        
        if max_score == 0:
            # No keywords matched, classify as 'Other'
            return 'Other', 0.5
        
        # Get category with highest score
        best_category = max(scores, key=scores.get)
        
        # Calculate confidence (normalized score)
        total_keywords = sum(scores.values())
        confidence = max_score / total_keywords if total_keywords > 0 else 0.5
        confidence = min(confidence, 0.99)  # Cap at 0.99
        
        return best_category, confidence
    
    def get_category_suggestions(self, complaint_text: str, top_n: int = 3) -> List[Tuple[str, float]]:
        """
        Get top N category suggestions with confidence scores
        """
        tokens = self.preprocess_text(complaint_text)
        scores = self.calculate_category_scores(tokens)
        
        # Sort by score
        sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate confidence for top N
        suggestions = []
        total_score = sum(scores.values())
        
        for category, score in sorted_categories[:top_n]:
            if total_score > 0:
                confidence = score / total_score
            else:
                confidence = 0.0
            suggestions.append((category, confidence))
        
        return suggestions


# Global categorizer instance
categorizer = ComplaintCategorizer()


def categorize_complaint(complaint_text: str, manual_category: str = None) -> Dict:
    """
    Convenience function to categorize a complaint
    
    Returns:
        Dictionary with category and confidence
    """
    category, confidence = categorizer.categorize(complaint_text, manual_category)
    
    return {
        'category': category,
        'confidence': confidence
    }
