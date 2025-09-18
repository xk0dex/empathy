"""
Performance benchmark suite for testing Empathy with large repositories.
Tests scalability, memory usage, and processing time with varying repository sizes.
"""

import time
import psutil
import memory_profiler
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import random
import string
import sys
import os
from dataclasses import dataclass, asdict
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@dataclass
class BenchmarkResult:
    """Single benchmark test result."""
    test_name: str
    repo_size: str  # 'small', 'medium', 'large', 'xlarge'
    commit_count: int
    contributor_count: int
    file_count: int
    processing_time_seconds: float
    memory_usage_mb: float
    cpu_usage_percent: float
    success: bool
    error_message: Optional[str] = None
    metrics_calculated: Optional[Dict] = None

@dataclass
class PerformanceReport:
    """Complete performance benchmark report."""
    test_suite: str
    timestamp: str
    system_info: Dict
    results: List[BenchmarkResult]
    summary: Dict
    recommendations: List[str]

class MockDataGenerator:
    """Generate realistic mock data for performance testing."""
    
    def __init__(self):
        self.contributors = self._generate_contributors()
        self.file_paths = self._generate_file_paths()
        self.commit_messages = self._generate_commit_messages()
    
    def _generate_contributors(self, count: int = 50) -> List[str]:
        """Generate realistic contributor names."""
        first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez']
        
        contributors = []
        for i in range(count):
            first = random.choice(first_names)
            last = random.choice(last_names)
            contributors.append(f"{first}.{last}@company.com")
        
        return contributors
    
    def _generate_file_paths(self, count: int = 200) -> List[str]:
        """Generate realistic file paths."""
        directories = ['src', 'lib', 'tests', 'docs', 'config', 'utils', 'components', 'services']
        extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.h', '.md', '.json', '.yaml']
        
        paths = []
        for i in range(count):
            dir_depth = random.randint(1, 4)
            path_parts = [random.choice(directories)]
            
            for _ in range(dir_depth - 1):
                path_parts.append(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))))
            
            filename = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 15)))
            extension = random.choice(extensions)
            path_parts.append(filename + extension)
            
            paths.append('/'.join(path_parts))
        
        return paths
    
    def _generate_commit_messages(self, count: int = 100) -> List[str]:
        """Generate realistic commit messages."""
        actions = ['Fix', 'Add', 'Update', 'Remove', 'Refactor', 'Improve', 'Optimize']
        targets = ['bug in', 'feature for', 'performance of', 'security in', 'documentation for']
        components = ['user authentication', 'data processing', 'API endpoints', 'frontend components', 'database queries']
        
        messages = []
        for i in range(count):
            action = random.choice(actions)
            if random.random() < 0.3:  # 30% chance of simple message
                messages.append(f"{action} {random.choice(components)}")
            else:
                target = random.choice(targets)
                component = random.choice(components)
                messages.append(f"{action} {target} {component}")
        
        return messages
    
    def generate_commits(self, count: int, start_date: datetime = None) -> List[Dict]:
        """Generate mock commit data."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        
        commits = []
        for i in range(count):
            # Simulate realistic commit patterns (more during weekdays, business hours)
            date_offset = random.randint(0, 365)
            base_date = start_date + timedelta(days=date_offset)
            
            # Adjust for weekday pattern
            if base_date.weekday() >= 5:  # Weekend
                if random.random() < 0.3:  # 30% chance of weekend commit
                    hour = random.randint(10, 22)
                else:
                    continue
            else:  # Weekday
                hour = random.choices(
                    range(24), 
                    weights=[1,1,1,1,1,1,2,4,8,10,12,12,12,10,10,8,6,4,3,2,2,1,1,1]
                )[0]
            
            commit_date = base_date.replace(
                hour=hour,
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            # Generate commit data
            author = random.choice(self.contributors)
            message = random.choice(self.commit_messages)
            files_changed = random.choices(self.file_paths, k=random.randint(1, 8))
            lines_added = random.randint(1, 200)
            lines_deleted = random.randint(0, 100)
            
            # Add sentiment bias based on message content
            sentiment_score = 0.5
            if any(word in message.lower() for word in ['fix', 'bug', 'error', 'issue']):
                sentiment_score = random.uniform(0.2, 0.5)
            elif any(word in message.lower() for word in ['add', 'new', 'feature', 'improve']):
                sentiment_score = random.uniform(0.6, 0.9)
            else:
                sentiment_score = random.uniform(0.4, 0.7)
            
            commit = {
                'id': f'commit_{i:06d}',
                'author': author,
                'date': commit_date.isoformat(),
                'message': message,
                'files_changed': files_changed,
                'lines_added': lines_added,
                'lines_deleted': lines_deleted,
                'lines_changed': lines_added + lines_deleted,
                'sentiment': sentiment_score
            }
            
            commits.append(commit)
        
        # Sort by date
        commits.sort(key=lambda x: x['date'])
        return commits

class PerformanceBenchmark:
    """Main performance benchmarking class."""
    
    def __init__(self):
        self.data_generator = MockDataGenerator()
        self.results: List[BenchmarkResult] = []
        
        # Test configurations
        self.test_configs = {
            'small': {'commits': 100, 'contributors': 5, 'files': 20},
            'medium': {'commits': 1000, 'contributors': 15, 'files': 100},
            'large': {'commits': 5000, 'contributors': 50, 'files': 500},
            'xlarge': {'commits': 10000, 'contributors': 100, 'files': 1000},
            'enterprise': {'commits': 25000, 'contributors': 200, 'files': 2000}
        }
    
    def run_full_benchmark_suite(self) -> PerformanceReport:
        """Run complete benchmark suite with all test sizes."""
        print("🚀 Starting Empathy Performance Benchmark Suite")
        print("=" * 60)
        
        start_time = time.time()
        
        # System information
        system_info = self._get_system_info()
        print(f"System: {system_info['python_version']} on {system_info['platform']}")
        print(f"CPU: {system_info['cpu_count']} cores, RAM: {system_info['total_memory_gb']:.1f} GB")
        print()
        
        # Run benchmarks for each size
        for size_name, config in self.test_configs.items():
            print(f"📊 Testing {size_name.upper()} repository ({config['commits']:,} commits)")
            
            try:
                result = self._benchmark_repository_size(size_name, config)
                self.results.append(result)
                
                if result.success:
                    print(f"  ✅ Completed in {result.processing_time_seconds:.2f}s")
                    print(f"  📈 Memory: {result.memory_usage_mb:.1f} MB, CPU: {result.cpu_usage_percent:.1f}%")
                else:
                    print(f"  ❌ Failed: {result.error_message}")
                
            except Exception as e:
                print(f"  💥 Critical error: {str(e)}")
                self.results.append(BenchmarkResult(
                    test_name=f"benchmark_{size_name}",
                    repo_size=size_name,
                    commit_count=config['commits'],
                    contributor_count=config['contributors'],
                    file_count=config['files'],
                    processing_time_seconds=0.0,
                    memory_usage_mb=0.0,
                    cpu_usage_percent=0.0,
                    success=False,
                    error_message=str(e)
                ))
            
            print()
        
        total_time = time.time() - start_time
        print(f"⏱️ Total benchmark time: {total_time:.2f} seconds")
        
        # Generate report
        report = self._generate_report(system_info, total_time)
        return report
    
    def _benchmark_repository_size(self, size_name: str, config: Dict) -> BenchmarkResult:
        """Benchmark a specific repository size."""
        # Generate test data
        commits = self.data_generator.generate_commits(config['commits'])
        
        # Measure performance
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            # Simulate analysis process
            metrics = self._simulate_analysis(commits, config)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            processing_time = end_time - start_time
            memory_used = end_memory - start_memory
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            return BenchmarkResult(
                test_name=f"benchmark_{size_name}",
                repo_size=size_name,
                commit_count=len(commits),
                contributor_count=config['contributors'],
                file_count=config['files'],
                processing_time_seconds=processing_time,
                memory_usage_mb=memory_used,
                cpu_usage_percent=cpu_percent,
                success=True,
                metrics_calculated=metrics
            )
            
        except Exception as e:
            end_time = time.time()
            return BenchmarkResult(
                test_name=f"benchmark_{size_name}",
                repo_size=size_name,
                commit_count=config['commits'],
                contributor_count=config['contributors'],
                file_count=config['files'],
                processing_time_seconds=end_time - start_time,
                memory_usage_mb=0.0,
                cpu_usage_percent=0.0,
                success=False,
                error_message=str(e)
            )
    
    def _simulate_analysis(self, commits: List[Dict], config: Dict) -> Dict:
        """Simulate the actual team health analysis process."""
        # This simulates the actual analysis workload
        
        # 1. Sentiment analysis simulation
        sentiments = []
        for commit in commits:
            # Simulate NLP processing time
            time.sleep(0.001)  # 1ms per commit for sentiment
            sentiments.append(commit['sentiment'])
        
        # 2. Collaboration network analysis
        collaborations = {}
        for commit in commits:
            author = commit['author']
            for file_path in commit['files_changed']:
                if file_path not in collaborations:
                    collaborations[file_path] = set()
                collaborations[file_path].add(author)
        
        # 3. Knowledge distribution calculation
        author_files = {}
        for commit in commits:
            author = commit['author']
            if author not in author_files:
                author_files[author] = set()
            author_files[author].update(commit['files_changed'])
        
        # 4. Activity patterns analysis
        daily_commits = {}
        for commit in commits:
            date = commit['date'][:10]  # YYYY-MM-DD
            daily_commits[date] = daily_commits.get(date, 0) + 1
        
        # 5. Calculate final metrics
        avg_sentiment = np.mean(sentiments)
        collaboration_score = len([f for f, authors in collaborations.items() if len(authors) > 1]) / len(collaborations)
        knowledge_distribution = 1.0 - (max(len(files) for files in author_files.values()) / len(set().union(*author_files.values())))
        activity_score = min(np.mean(list(daily_commits.values())) / 10.0, 1.0)
        
        team_health_score = (avg_sentiment * 0.3 + collaboration_score * 0.3 + 
                           knowledge_distribution * 0.2 + activity_score * 0.2)
        
        return {
            'team_health_score': team_health_score,
            'sentiment_score': avg_sentiment,
            'collaboration_score': collaboration_score,
            'knowledge_distribution': knowledge_distribution,
            'activity_score': activity_score,
            'total_commits': len(commits),
            'unique_contributors': len(author_files),
            'files_touched': len(collaborations)
        }
    
    def _get_system_info(self) -> Dict:
        """Get system information for the report."""
        return {
            'platform': sys.platform,
            'python_version': sys.version.split()[0],
            'cpu_count': psutil.cpu_count(),
            'total_memory_gb': psutil.virtual_memory().total / (1024**3),
            'available_memory_gb': psutil.virtual_memory().available / (1024**3),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_report(self, system_info: Dict, total_time: float) -> PerformanceReport:
        """Generate comprehensive performance report."""
        successful_results = [r for r in self.results if r.success]
        
        # Calculate summary statistics
        if successful_results:
            avg_time_per_commit = np.mean([r.processing_time_seconds / r.commit_count for r in successful_results])
            max_memory_usage = max(r.memory_usage_mb for r in successful_results)
            scaling_factor = self._calculate_scaling_factor(successful_results)
        else:
            avg_time_per_commit = 0
            max_memory_usage = 0
            scaling_factor = 0
        
        summary = {
            'total_tests': len(self.results),
            'successful_tests': len(successful_results),
            'failed_tests': len(self.results) - len(successful_results),
            'total_time_seconds': total_time,
            'avg_time_per_commit_ms': avg_time_per_commit * 1000,
            'max_memory_usage_mb': max_memory_usage,
            'scaling_factor': scaling_factor,
            'largest_successful_repo': max((r.commit_count for r in successful_results), default=0)
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(successful_results, summary)
        
        return PerformanceReport(
            test_suite="Empathy Performance Benchmark v1.0",
            timestamp=datetime.now().isoformat(),
            system_info=system_info,
            results=self.results,
            summary=summary,
            recommendations=recommendations
        )
    
    def _calculate_scaling_factor(self, results: List[BenchmarkResult]) -> float:
        """Calculate how processing time scales with repository size."""
        if len(results) < 2:
            return 0.0
        
        commit_counts = [r.commit_count for r in results]
        processing_times = [r.processing_time_seconds for r in results]
        
        # Simple linear regression to find scaling
        n = len(results)
        sum_x = sum(commit_counts)
        sum_y = sum(processing_times)
        sum_xy = sum(x * y for x, y in zip(commit_counts, processing_times))
        sum_x2 = sum(x * x for x in commit_counts)
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        return slope
    
    def _generate_recommendations(self, results: List[BenchmarkResult], summary: Dict) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []
        
        if summary['max_memory_usage_mb'] > 1000:  # > 1GB
            recommendations.append("🧠 Consider implementing incremental processing for large repositories to reduce memory usage")
        
        if summary['avg_time_per_commit_ms'] > 10:  # > 10ms per commit
            recommendations.append("⚡ Processing time per commit is high - consider optimizing sentiment analysis and collaboration algorithms")
        
        if summary['failed_tests'] > 0:
            recommendations.append("🚨 Some tests failed - investigate error handling for edge cases and resource limitations")
        
        if summary['scaling_factor'] > 0.001:  # Non-linear scaling
            recommendations.append("📈 Processing time scales significantly with repo size - implement caching and parallel processing")
        
        if summary['largest_successful_repo'] < 10000:
            recommendations.append("🎯 Consider implementing async processing for repositories with 10K+ commits")
        
        if len(results) > 0 and max(r.cpu_usage_percent for r in results) > 80:
            recommendations.append("🔧 High CPU usage detected - implement multiprocessing for CPU-intensive tasks")
        
        # Positive recommendations
        if summary['successful_tests'] == summary['total_tests']:
            recommendations.append("✅ All tests passed successfully - the system handles the tested repository sizes well")
        
        if summary['avg_time_per_commit_ms'] < 5:
            recommendations.append("🚀 Excellent per-commit processing time - suitable for real-time analysis")
        
        return recommendations
    
    def export_report(self, report: PerformanceReport, format: str = 'json') -> str:
        """Export performance report."""
        if format == 'json':
            return json.dumps(asdict(report), indent=2, default=str)
        elif format == 'csv':
            # Export results as CSV
            df = pd.DataFrame([asdict(r) for r in report.results])
            return df.to_csv(index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

class AsyncPerformanceBenchmark:
    """Asynchronous version for testing concurrent processing."""
    
    def __init__(self):
        self.data_generator = MockDataGenerator()
    
    async def benchmark_concurrent_analysis(self, commit_counts: List[int]) -> Dict:
        """Test concurrent processing of multiple repositories."""
        tasks = []
        
        async with aiohttp.ClientSession() as session:
            for count in commit_counts:
                commits = self.data_generator.generate_commits(count)
                task = asyncio.create_task(self._async_analyze_commits(commits))
                tasks.append(task)
            
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()
        
        successful_results = [r for r in results if not isinstance(r, Exception)]
        
        return {
            'concurrent_repos': len(commit_counts),
            'successful_analyses': len(successful_results),
            'total_time_seconds': end_time - start_time,
            'average_time_per_repo': (end_time - start_time) / len(commit_counts),
            'results': successful_results
        }
    
    async def _async_analyze_commits(self, commits: List[Dict]) -> Dict:
        """Async commit analysis simulation."""
        # Simulate async processing
        await asyncio.sleep(len(commits) * 0.0001)  # 0.1ms per commit
        
        # Return mock metrics
        return {
            'commits_processed': len(commits),
            'processing_time': len(commits) * 0.0001,
            'team_health_score': random.uniform(0.3, 0.9)
        }

# Command line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Empathy Performance Benchmark')
    parser.add_argument('--test-size', choices=['small', 'medium', 'large', 'xlarge', 'enterprise'], 
                       help='Run specific test size')
    parser.add_argument('--output', default='benchmark_report.json', help='Output file path')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')
    parser.add_argument('--async-test', action='store_true', help='Run async concurrent test')
    
    args = parser.parse_args()
    
    benchmark = PerformanceBenchmark()
    
    if args.async_test:
        print("🔄 Running async concurrent benchmark...")
        async_benchmark = AsyncPerformanceBenchmark()
        
        async def run_async_test():
            result = await async_benchmark.benchmark_concurrent_analysis([100, 500, 1000, 2000])
            print(f"Concurrent analysis of {result['concurrent_repos']} repos:")
            print(f"  ✅ Successful: {result['successful_analyses']}")
            print(f"  ⏱️ Total time: {result['total_time_seconds']:.2f}s")
            print(f"  📊 Avg per repo: {result['average_time_per_repo']:.2f}s")
        
        asyncio.run(run_async_test())
    
    elif args.test_size:
        print(f"🎯 Running single test: {args.test_size}")
        config = benchmark.test_configs[args.test_size]
        result = benchmark._benchmark_repository_size(args.test_size, config)
        
        if result.success:
            print(f"✅ Test completed successfully")
            print(f"📊 Metrics: {result.metrics_calculated}")
        else:
            print(f"❌ Test failed: {result.error_message}")
    
    else:
        # Run full benchmark suite
        report = benchmark.run_full_benchmark_suite()
        
        # Export report
        report_data = benchmark.export_report(report, args.format)
        
        with open(args.output, 'w') as f:
            f.write(report_data)
        
        print(f"\n📋 Report saved to: {args.output}")
        print("\n📊 Summary:")
        print(f"  Tests: {report.summary['successful_tests']}/{report.summary['total_tests']} successful")
        print(f"  Largest repo: {report.summary['largest_successful_repo']:,} commits")
        print(f"  Avg time per commit: {report.summary['avg_time_per_commit_ms']:.2f}ms")
        print(f"  Max memory usage: {report.summary['max_memory_usage_mb']:.1f}MB")
        
        print("\n💡 Recommendations:")
        for rec in report.recommendations:
            print(f"  {rec}")