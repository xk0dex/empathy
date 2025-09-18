"""
Historical trends analyzer for team health metrics over time.
Provides week-over-week, month-over-month comparisons and trend visualization.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class TrendPoint:
    """Single point in time for trend analysis."""
    date: str
    team_health_score: float
    sentiment_score: float
    collaboration_score: float
    activity_score: float
    commit_count: int
    contributor_count: int
    avg_commit_size: float

@dataclass
class TrendAnalysis:
    """Complete trend analysis results."""
    period: str  # 'weekly', 'monthly', 'quarterly'
    data_points: List[TrendPoint]
    trends: Dict[str, float]  # metric -> percentage change
    insights: List[str]
    period_comparison: Optional[Dict[str, float]] = None

class HistoricalTrendsAnalyzer:
    """Analyzes team health trends over time periods."""
    
    def __init__(self):
        self.metrics = [
            'team_health_score', 'sentiment_score', 'collaboration_score',
            'activity_score', 'commit_count', 'contributor_count', 'avg_commit_size'
        ]
    
    def analyze_weekly_trends(self, commits_data: List[Dict], weeks: int = 12) -> TrendAnalysis:
        """
        Analyze weekly trends for the last N weeks.
        
        Args:
            commits_data: List of commit dictionaries with dates and metrics
            weeks: Number of weeks to analyze (default 12)
            
        Returns:
            TrendAnalysis object with weekly trend data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks)
        
        # Group commits by week
        weekly_data = self._group_by_period(commits_data, 'week', start_date, end_date)
        
        # Calculate metrics for each week
        data_points = []
        for week_start, week_commits in weekly_data.items():
            if week_commits:  # Only include weeks with commits
                metrics = self._calculate_week_metrics(week_commits)
                data_points.append(TrendPoint(
                    date=week_start.strftime('%Y-%m-%d'),
                    **metrics
                ))
        
        # Calculate trends and insights
        trends = self._calculate_trends(data_points)
        insights = self._generate_insights(data_points, trends, 'weekly')
        
        return TrendAnalysis(
            period='weekly',
            data_points=data_points,
            trends=trends,
            insights=insights
        )
    
    def analyze_monthly_trends(self, commits_data: List[Dict], months: int = 6) -> TrendAnalysis:
        """
        Analyze monthly trends for the last N months.
        
        Args:
            commits_data: List of commit dictionaries with dates and metrics
            months: Number of months to analyze (default 6)
            
        Returns:
            TrendAnalysis object with monthly trend data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)  # Approximate
        
        # Group commits by month
        monthly_data = self._group_by_period(commits_data, 'month', start_date, end_date)
        
        # Calculate metrics for each month
        data_points = []
        for month_start, month_commits in monthly_data.items():
            if month_commits:  # Only include months with commits
                metrics = self._calculate_month_metrics(month_commits)
                data_points.append(TrendPoint(
                    date=month_start.strftime('%Y-%m'),
                    **metrics
                ))
        
        # Calculate trends and insights
        trends = self._calculate_trends(data_points)
        insights = self._generate_insights(data_points, trends, 'monthly')
        
        return TrendAnalysis(
            period='monthly',
            data_points=data_points,
            trends=trends,
            insights=insights
        )
    
    def compare_periods(self, commits_data: List[Dict], 
                       period1_start: datetime, period1_end: datetime,
                       period2_start: datetime, period2_end: datetime) -> Dict[str, float]:
        """
        Compare metrics between two specific time periods.
        
        Args:
            commits_data: List of commit dictionaries
            period1_start, period1_end: First period boundaries
            period2_start, period2_end: Second period boundaries
            
        Returns:
            Dictionary with percentage changes between periods
        """
        # Filter commits for each period
        period1_commits = [c for c in commits_data 
                          if period1_start <= datetime.fromisoformat(c['date']) <= period1_end]
        period2_commits = [c for c in commits_data 
                          if period2_start <= datetime.fromisoformat(c['date']) <= period2_end]
        
        # Calculate metrics for each period
        metrics1 = self._calculate_period_metrics(period1_commits)
        metrics2 = self._calculate_period_metrics(period2_commits)
        
        # Calculate percentage changes
        comparison = {}
        for metric in self.metrics:
            if metrics1[metric] > 0:
                change = ((metrics2[metric] - metrics1[metric]) / metrics1[metric]) * 100
                comparison[metric] = round(change, 2)
            else:
                comparison[metric] = 0.0
        
        return comparison
    
    def _group_by_period(self, commits_data: List[Dict], period: str, 
                        start_date: datetime, end_date: datetime) -> Dict[datetime, List[Dict]]:
        """Group commits by time period (week/month)."""
        grouped = defaultdict(list)
        
        for commit in commits_data:
            commit_date = datetime.fromisoformat(commit['date'])
            
            if start_date <= commit_date <= end_date:
                if period == 'week':
                    # Start of week (Monday)
                    week_start = commit_date - timedelta(days=commit_date.weekday())
                    period_key = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                elif period == 'month':
                    # Start of month
                    period_key = commit_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                
                grouped[period_key].append(commit)
        
        return dict(grouped)
    
    def _calculate_week_metrics(self, week_commits: List[Dict]) -> Dict[str, float]:
        """Calculate metrics for a week's worth of commits."""
        return self._calculate_period_metrics(week_commits)
    
    def _calculate_month_metrics(self, month_commits: List[Dict]) -> Dict[str, float]:
        """Calculate metrics for a month's worth of commits."""
        return self._calculate_period_metrics(month_commits)
    
    def _calculate_period_metrics(self, commits: List[Dict]) -> Dict[str, float]:
        """Calculate all metrics for a given set of commits."""
        if not commits:
            return {metric: 0.0 for metric in self.metrics}
        
        # Basic counts
        commit_count = len(commits)
        contributors = set(commit.get('author', 'unknown') for commit in commits)
        contributor_count = len(contributors)
        
        # Calculate average commit size (lines changed)
        commit_sizes = [commit.get('lines_changed', 0) for commit in commits]
        avg_commit_size = np.mean(commit_sizes) if commit_sizes else 0.0
        
        # Sentiment analysis (mock calculation - would use real sentiment analyzer)
        sentiment_scores = [commit.get('sentiment', 0.5) for commit in commits]
        sentiment_score = np.mean(sentiment_scores) if sentiment_scores else 0.5
        
        # Collaboration score (based on number of unique contributors and interaction)
        collaboration_score = min(contributor_count / max(commit_count * 0.3, 1), 1.0)
        
        # Activity score (based on commit frequency and size)
        days_in_period = 7  # Assume weekly for now
        commits_per_day = commit_count / days_in_period
        activity_score = min(commits_per_day / 5.0, 1.0)  # Normalize to 5 commits/day = 1.0
        
        # Overall team health score (weighted average)
        team_health_score = (
            sentiment_score * 0.4 +
            collaboration_score * 0.3 +
            activity_score * 0.3
        )
        
        return {
            'team_health_score': round(team_health_score, 3),
            'sentiment_score': round(sentiment_score, 3),
            'collaboration_score': round(collaboration_score, 3),
            'activity_score': round(activity_score, 3),
            'commit_count': commit_count,
            'contributor_count': contributor_count,
            'avg_commit_size': round(avg_commit_size, 1)
        }
    
    def _calculate_trends(self, data_points: List[TrendPoint]) -> Dict[str, float]:
        """Calculate percentage change trends for each metric."""
        if len(data_points) < 2:
            return {metric: 0.0 for metric in self.metrics}
        
        trends = {}
        for metric in self.metrics:
            values = [getattr(point, metric) for point in data_points]
            
            if len(values) >= 2 and values[0] > 0:
                # Calculate percentage change from first to last value
                change = ((values[-1] - values[0]) / values[0]) * 100
                trends[metric] = round(change, 2)
            else:
                trends[metric] = 0.0
        
        return trends
    
    def _generate_insights(self, data_points: List[TrendPoint], 
                          trends: Dict[str, float], period: str) -> List[str]:
        """Generate human-readable insights from trend data."""
        insights = []
        
        # Team health trend
        health_trend = trends.get('team_health_score', 0)
        if health_trend > 10:
            insights.append(f"🟢 Team health improved significantly (+{health_trend:.1f}%) over the last {period} period")
        elif health_trend > 5:
            insights.append(f"🟡 Team health improved moderately (+{health_trend:.1f}%) over the last {period} period")
        elif health_trend < -10:
            insights.append(f"🔴 Team health declined significantly ({health_trend:.1f}%) over the last {period} period")
        elif health_trend < -5:
            insights.append(f"🟡 Team health declined moderately ({health_trend:.1f}%) over the last {period} period")
        
        # Activity trends
        activity_trend = trends.get('activity_score', 0)
        if activity_trend > 20:
            insights.append("📈 Development activity increased substantially")
        elif activity_trend < -20:
            insights.append("📉 Development activity decreased substantially")
        
        # Collaboration trends
        collab_trend = trends.get('collaboration_score', 0)
        if collab_trend > 15:
            insights.append("🤝 Team collaboration improved notably")
        elif collab_trend < -15:
            insights.append("👥 Team collaboration decreased - consider pair programming or code reviews")
        
        # Sentiment trends
        sentiment_trend = trends.get('sentiment_score', 0)
        if sentiment_trend > 10:
            insights.append("😊 Team sentiment became more positive")
        elif sentiment_trend < -10:
            insights.append("😟 Team sentiment became more negative - consider team retrospectives")
        
        # Data quality insights
        if len(data_points) < 4:
            insights.append("⚠️ Limited data available - more time needed for reliable trends")
        
        # Commit patterns
        avg_commits = np.mean([point.commit_count for point in data_points])
        if avg_commits < 1:
            insights.append("⚠️ Very low commit frequency - consider breaking down work into smaller tasks")
        elif avg_commits > 50:
            insights.append("⚡ High commit frequency - ensure commits are meaningful and well-documented")
        
        return insights
    
    def export_trends_data(self, trend_analysis: TrendAnalysis, format: str = 'json') -> str:
        """
        Export trend analysis data in specified format.
        
        Args:
            trend_analysis: TrendAnalysis object to export
            format: Export format ('json', 'csv')
            
        Returns:
            Formatted string data
        """
        if format == 'json':
            # Convert to dict for JSON serialization
            data = asdict(trend_analysis)
            return json.dumps(data, indent=2)
        
        elif format == 'csv':
            # Create CSV with data points
            if not trend_analysis.data_points:
                return "No data available"
            
            # Header
            csv_lines = ['date,team_health_score,sentiment_score,collaboration_score,activity_score,commit_count,contributor_count,avg_commit_size']
            
            # Data rows
            for point in trend_analysis.data_points:
                row = f"{point.date},{point.team_health_score},{point.sentiment_score},{point.collaboration_score},{point.activity_score},{point.commit_count},{point.contributor_count},{point.avg_commit_size}"
                csv_lines.append(row)
            
            return '\n'.join(csv_lines)
        
        else:
            raise ValueError(f"Unsupported format: {format}")

# Example usage and testing
if __name__ == "__main__":
    # Sample commit data for testing
    sample_commits = [
        {
            'date': '2025-09-01T10:00:00',
            'author': 'alice',
            'message': 'Fix critical bug in user authentication',
            'lines_changed': 45,
            'sentiment': 0.3
        },
        {
            'date': '2025-09-02T14:30:00',
            'author': 'bob',
            'message': 'Add new feature for dashboard',
            'lines_changed': 120,
            'sentiment': 0.8
        },
        {
            'date': '2025-09-08T09:15:00',
            'author': 'alice',
            'message': 'Refactor database connection logic',
            'lines_changed': 80,
            'sentiment': 0.6
        },
        {
            'date': '2025-09-15T16:45:00',
            'author': 'charlie',
            'message': 'Implement user feedback improvements',
            'lines_changed': 95,
            'sentiment': 0.7
        }
    ]
    
    analyzer = HistoricalTrendsAnalyzer()
    
    # Test weekly trends
    weekly_trends = analyzer.analyze_weekly_trends(sample_commits, weeks=4)
    print("Weekly Trends:")
    print(f"Data points: {len(weekly_trends.data_points)}")
    print(f"Team health trend: {weekly_trends.trends['team_health_score']}%")
    print("Insights:")
    for insight in weekly_trends.insights:
        print(f"  - {insight}")
    
    print("\n" + "="*50 + "\n")
    
    # Test monthly trends
    monthly_trends = analyzer.analyze_monthly_trends(sample_commits, months=2)
    print("Monthly Trends:")
    print(f"Data points: {len(monthly_trends.data_points)}")
    print(f"Team health trend: {monthly_trends.trends['team_health_score']}%")
    
    # Test export
    json_export = analyzer.export_trends_data(weekly_trends, 'json')
    print(f"\nJSON Export length: {len(json_export)} characters")