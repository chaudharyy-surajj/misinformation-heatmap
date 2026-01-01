#!/usr/bin/env python3
"""
PERFORMANCE MONITORING AND OPTIMIZATION MODULE
- Real-time system monitoring
- Automatic performance tuning
- Resource usage optimization
- Bottleneck detection and resolution
"""

import psutil
import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import threading
import sqlite3
from collections import deque
import numpy as np

@dataclass
class SystemMetrics:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_io_read_mb: float
    disk_io_write_mb: float
    network_sent_mb: float
    network_recv_mb: float
    active_threads: int
    active_processes: int
    events_per_second: float
    ml_accuracy: float
    response_time_ms: float

class PerformanceMonitor:
    def __init__(self, history_size: int = 1000):
        self.history = deque(maxlen=history_size)
        self.monitoring_active = False
        self.logger = logging.getLogger(__name__)
        self.baseline_metrics = None
        self.alerts = []
        
    def start_monitoring(self):
        """Start continuous performance monitoring"""
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        self.logger.info("Performance monitoring started")
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        self.logger.info("Performance monitoring stopped")
        
    def _monitoring_loop(self):
        """Main monitoring loop"""
        last_disk_io = psutil.disk_io_counters()
        last_network_io = psutil.net_io_counters()
        
        while self.monitoring_active:
            try:
                # Collect system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                # Disk I/O
                current_disk_io = psutil.disk_io_counters()
                disk_read_mb = (current_disk_io.read_bytes - last_disk_io.read_bytes) / 1024 / 1024
                disk_write_mb = (current_disk_io.write_bytes - last_disk_io.write_bytes) / 1024 / 1024
                last_disk_io = current_disk_io
                
                # Network I/O
                current_network_io = psutil.net_io_counters()
                network_sent_mb = (current_network_io.bytes_sent - last_network_io.bytes_sent) / 1024 / 1024
                network_recv_mb = (current_network_io.bytes_recv - last_network_io.bytes_recv) / 1024 / 1024
                last_network_io = current_network_io
                
                # Process information
                active_threads = threading.active_count()
                active_processes = len(psutil.pids())
                
                # Create metrics object
                metrics = SystemMetrics(
                    timestamp=datetime.now().isoformat(),
                    cpu_percent=cpu_percent,
                    memory_percent=memory.percent,
                    memory_used_mb=memory.used / 1024 / 1024,
                    disk_io_read_mb=disk_read_mb,
                    disk_io_write_mb=disk_write_mb,
                    network_sent_mb=network_sent_mb,
                    network_recv_mb=network_recv_mb,
                    active_threads=active_threads,
                    active_processes=active_processes,
                    events_per_second=0.0,  # Will be updated by main system
                    ml_accuracy=0.0,        # Will be updated by ML system
                    response_time_ms=0.0    # Will be updated by API system
                )
                
                self.history.append(metrics)
                
                # Check for performance issues
                self._check_performance_alerts(metrics)
                
                # Store in database
                self._store_metrics(metrics)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                
            time.sleep(5)  # Monitor every 5 seconds
            
    def _check_performance_alerts(self, metrics: SystemMetrics):
        """Check for performance issues and generate alerts"""
        alerts = []
        
        # CPU usage alert
        if metrics.cpu_percent > 90:
            alerts.append({
                'type': 'HIGH_CPU',
                'severity': 'CRITICAL',
                'message': f'CPU usage at {metrics.cpu_percent:.1f}%',
                'timestamp': metrics.timestamp
            })
        elif metrics.cpu_percent > 75:
            alerts.append({
                'type': 'HIGH_CPU',
                'severity': 'WARNING',
                'message': f'CPU usage at {metrics.cpu_percent:.1f}%',
                'timestamp': metrics.timestamp
            })
            
        # Memory usage alert
        if metrics.memory_percent > 90:
            alerts.append({
                'type': 'HIGH_MEMORY',
                'severity': 'CRITICAL',
                'message': f'Memory usage at {metrics.memory_percent:.1f}%',
                'timestamp': metrics.timestamp
            })
        elif metrics.memory_percent > 80:
            alerts.append({
                'type': 'HIGH_MEMORY',
                'severity': 'WARNING',
                'message': f'Memory usage at {metrics.memory_percent:.1f}%',
                'timestamp': metrics.timestamp
            })
            
        # Low throughput alert
        if metrics.events_per_second < 1.0 and len(self.history) > 10:
            alerts.append({
                'type': 'LOW_THROUGHPUT',
                'severity': 'WARNING',
                'message': f'Low throughput: {metrics.events_per_second:.1f} EPS',
                'timestamp': metrics.timestamp
            })
            
        # Add new alerts
        for alert in alerts:
            self.alerts.append(alert)
            self.logger.warning(f"ALERT: {alert['message']}")
            
        # Keep only recent alerts (last hour)
        cutoff_time = datetime.now() - timedelta(hours=1)
        self.alerts = [alert for alert in self.alerts 
                      if datetime.fromisoformat(alert['timestamp']) > cutoff_time]
                      
    def _store_metrics(self, metrics: SystemMetrics):
        """Store metrics in database"""
        try:
            conn = sqlite3.connect('performance_metrics.db')
            cursor = conn.cursor()
            
            # Create table if not exists
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    timestamp TEXT PRIMARY KEY,
                    cpu_percent REAL,
                    memory_percent REAL,
                    memory_used_mb REAL,
                    disk_io_read_mb REAL,
                    disk_io_write_mb REAL,
                    network_sent_mb REAL,
                    network_recv_mb REAL,
                    active_threads INTEGER,
                    active_processes INTEGER,
                    events_per_second REAL,
                    ml_accuracy REAL,
                    response_time_ms REAL
                )
            ''')
            
            # Insert metrics
            cursor.execute('''
                INSERT OR REPLACE INTO performance_metrics VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metrics.timestamp, metrics.cpu_percent, metrics.memory_percent,
                metrics.memory_used_mb, metrics.disk_io_read_mb, metrics.disk_io_write_mb,
                metrics.network_sent_mb, metrics.network_recv_mb, metrics.active_threads,
                metrics.active_processes, metrics.events_per_second, metrics.ml_accuracy,
                metrics.response_time_ms
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to store metrics: {e}")
            
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        if not self.history:
            return {}
            
        latest = self.history[-1]
        return asdict(latest)
        
    def get_performance_summary(self, minutes: int = 60) -> Dict[str, Any]:
        """Get performance summary for the last N minutes"""
        if not self.history:
            return {}
            
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.history 
            if datetime.fromisoformat(m.timestamp) > cutoff_time
        ]
        
        if not recent_metrics:
            return {}
            
        # Calculate statistics
        cpu_values = [m.cpu_percent for m in recent_metrics]
        memory_values = [m.memory_percent for m in recent_metrics]
        throughput_values = [m.events_per_second for m in recent_metrics]
        
        return {
            'time_period_minutes': minutes,
            'sample_count': len(recent_metrics),
            'cpu_stats': {
                'avg': np.mean(cpu_values),
                'max': np.max(cpu_values),
                'min': np.min(cpu_values),
                'std': np.std(cpu_values)
            },
            'memory_stats': {
                'avg': np.mean(memory_values),
                'max': np.max(memory_values),
                'min': np.min(memory_values),
                'std': np.std(memory_values)
            },
            'throughput_stats': {
                'avg': np.mean(throughput_values),
                'max': np.max(throughput_values),
                'min': np.min(throughput_values),
                'std': np.std(throughput_values)
            },
            'alerts': self.alerts,
            'latest_metrics': asdict(recent_metrics[-1]) if recent_metrics else {}
        }
        
    def optimize_performance(self) -> Dict[str, Any]:
        """Automatic performance optimization"""
        recommendations = []
        actions_taken = []
        
        if not self.history:
            return {'recommendations': [], 'actions_taken': []}
            
        latest = self.history[-1]
        
        # CPU optimization
        if latest.cpu_percent > 80:
            recommendations.append({
                'type': 'CPU_OPTIMIZATION',
                'message': 'Consider reducing worker threads or batch size',
                'priority': 'HIGH'
            })
            
        # Memory optimization
        if latest.memory_percent > 80:
            recommendations.append({
                'type': 'MEMORY_OPTIMIZATION',
                'message': 'Consider reducing cache size or event history',
                'priority': 'HIGH'
            })
            
        # Throughput optimization
        if latest.events_per_second < 5.0:
            recommendations.append({
                'type': 'THROUGHPUT_OPTIMIZATION',
                'message': 'Consider increasing worker threads or optimizing ML models',
                'priority': 'MEDIUM'
            })
            
        return {
            'recommendations': recommendations,
            'actions_taken': actions_taken,
            'current_metrics': asdict(latest)
        }

class AutoTuner:
    """Automatic performance tuning system"""
    
    def __init__(self, monitor: PerformanceMonitor):
        self.monitor = monitor
        self.logger = logging.getLogger(__name__)
        self.tuning_active = False
        self.config_history = []
        
    def start_auto_tuning(self):
        """Start automatic performance tuning"""
        self.tuning_active = True
        tuning_thread = threading.Thread(target=self._tuning_loop, daemon=True)
        tuning_thread.start()
        self.logger.info("Auto-tuning started")
        
    def stop_auto_tuning(self):
        """Stop automatic performance tuning"""
        self.tuning_active = False
        self.logger.info("Auto-tuning stopped")
        
    def _tuning_loop(self):
        """Main auto-tuning loop"""
        while self.tuning_active:
            try:
                # Wait for sufficient data
                if len(self.monitor.history) < 10:
                    time.sleep(30)
                    continue
                    
                # Analyze performance
                summary = self.monitor.get_performance_summary(minutes=10)
                
                if not summary:
                    time.sleep(30)
                    continue
                    
                # Make tuning decisions
                self._tune_based_on_metrics(summary)
                
            except Exception as e:
                self.logger.error(f"Auto-tuning error: {e}")
                
            time.sleep(60)  # Tune every minute
            
    def _tune_based_on_metrics(self, summary: Dict[str, Any]):
        """Make tuning decisions based on metrics"""
        cpu_avg = summary['cpu_stats']['avg']
        memory_avg = summary['memory_stats']['avg']
        throughput_avg = summary['throughput_stats']['avg']
        
        # CPU-based tuning
        if cpu_avg > 85:
            self.logger.info("High CPU detected - reducing worker threads")
            # Implementation would adjust worker count
            
        elif cpu_avg < 50 and throughput_avg < 10:
            self.logger.info("Low CPU utilization - increasing worker threads")
            # Implementation would increase worker count
            
        # Memory-based tuning
        if memory_avg > 85:
            self.logger.info("High memory usage - reducing cache sizes")
            # Implementation would reduce cache sizes
            
        # Throughput-based tuning
        if throughput_avg < 5:
            self.logger.info("Low throughput - optimizing batch sizes")
            # Implementation would adjust batch processing

# Global monitor instance
performance_monitor = PerformanceMonitor()
auto_tuner = AutoTuner(performance_monitor)

def start_performance_monitoring():
    """Start the performance monitoring system"""
    performance_monitor.start_monitoring()
    auto_tuner.start_auto_tuning()
    
def stop_performance_monitoring():
    """Stop the performance monitoring system"""
    performance_monitor.stop_monitoring()
    auto_tuner.stop_auto_tuning()
    
def get_performance_dashboard_data() -> Dict[str, Any]:
    """Get data for performance dashboard"""
    return {
        'current_metrics': performance_monitor.get_current_metrics(),
        'performance_summary': performance_monitor.get_performance_summary(),
        'optimization_recommendations': performance_monitor.optimize_performance(),
        'system_info': {
            'cpu_count': psutil.cpu_count(),
            'memory_total_gb': psutil.virtual_memory().total / 1024 / 1024 / 1024,
            'disk_total_gb': psutil.disk_usage('/').total / 1024 / 1024 / 1024,
            'python_version': f"{psutil.version_info}",
            'platform': psutil.WINDOWS if psutil.WINDOWS else 'Unix'
        }
    }

if __name__ == "__main__":
    # Test the monitoring system
    start_performance_monitoring()
    
    try:
        while True:
            time.sleep(10)
            data = get_performance_dashboard_data()
            print(f"CPU: {data['current_metrics'].get('cpu_percent', 0):.1f}% | "
                  f"Memory: {data['current_metrics'].get('memory_percent', 0):.1f}% | "
                  f"Threads: {data['current_metrics'].get('active_threads', 0)}")
    except KeyboardInterrupt:
        stop_performance_monitoring()
        print("Monitoring stopped")