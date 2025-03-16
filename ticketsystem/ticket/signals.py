import nltk
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TicketPost, Ticket
from nltk.sentiment import SentimentIntensityAnalyzer
import logging
import os

logger = logging.getLogger(__name__)


def setup_nltk_data():
    try:
        nltk_data_dir = os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'nltk_data')
        if nltk_data_dir not in nltk.data.path:
            nltk.data.path.append(nltk_data_dir)
        logger.info("NLTK data path configured successfully")
    except Exception as e:
        logger.error(f"Error setting up NLTK data path: {str(e)}")
        raise


setup_nltk_data()


@receiver(post_save, sender=TicketPost)
def analyze_ticket_sentiment(sender, instance, created, **kwargs):
    try:
        if not created:
            return

        ticket = instance.ticket

        if ticket.posts.count() == 1:
            sia = SentimentIntensityAnalyzer()

            sentiment_scores = sia.polarity_scores(instance.message)

            compound_score = sentiment_scores['compound']

            if compound_score >= 0.05:
                sentiment = 'Positive'
            elif compound_score <= -0.05:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'

            ticket.sentiment = sentiment
            ticket.save()

            logger.info(
                f"Sentiment analysis completed for Ticket #{ticket.id}: {sentiment} (score: {compound_score:.2f})")

    except Exception as e:
        logger.error(
            f"Error in sentiment analysis for TicketPost {instance.id}: {str(e)}")
