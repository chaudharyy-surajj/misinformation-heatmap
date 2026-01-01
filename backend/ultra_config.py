#!/usr/bin/env python3
"""
ULTRA HIGH-PERFORMANCE CONFIGURATION
- Optimized settings for maximum throughput and accuracy
- Dynamic configuration based on system resources
- Advanced ML model parameters
- Performance tuning presets
"""

import os
import psutil
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class PerformancePreset:
    name: str
    max_workers: int
    max_processes: int
    batch_size: int
    cache_size: int
    request_timeout: int
    processing_interval: int
    max_articles_per_source: int
    memory_limit_mb: int
    description: str

class UltraConfig:
    """Ultra high-performance configuration manager"""
    
    def __init__(self):
        self.cpu_count = os.cpu_count() or 1
        self.memory_gb = psutil.virtual_memory().total / 1024 / 1024 / 1024
        self.current_preset = self._detect_optimal_preset()
        
    def _detect_optimal_preset(self) -> PerformancePreset:
        """Automatically detect optimal performance preset based on system resources"""
        
        if self.memory_gb >= 16 and self.cpu_count >= 8:
            return self.get_preset("ULTRA_HIGH")
        elif self.memory_gb >= 8 and self.cpu_count >= 4:
            return self.get_preset("HIGH")
        elif self.memory_gb >= 4 and self.cpu_count >= 2:
            return self.get_preset("MEDIUM")
        else:
            return self.get_preset("BASIC")
    
    def get_preset(self, preset_name: str) -> PerformancePreset:
        """Get performance preset by name"""
        presets = {
            "ULTRA_HIGH": PerformancePreset(
                name="ULTRA_HIGH",
                max_workers=min(64, self.cpu_count * 8),
                max_processes=min(16, self.cpu_count * 2),
                batch_size=100,
                cache_size=50000,
                request_timeout=15,
                processing_interval=30,  # 30 seconds for ultra-fast updates
                max_articles_per_source=50,
                memory_limit_mb=8192,
                description="Maximum performance for high-end systems (16GB+ RAM, 8+ cores)"
            ),
            "HIGH": PerformancePreset(
                name="HIGH",
                max_workers=min(32, self.cpu_count * 4),
                max_processes=min(8, self.cpu_count),
                batch_size=75,
                cache_size=25000,
                request_timeout=12,
                processing_interval=45,
                max_articles_per_source=35,
                memory_limit_mb=4096,
                description="High performance for mid-range systems (8GB+ RAM, 4+ cores)"
            ),
            "MEDIUM": PerformancePreset(
                name="MEDIUM",
                max_workers=min(16, self.cpu_count * 2),
                max_processes=min(4, self.cpu_count),
                batch_size=50,
                cache_size=10000,
                request_timeout=10,
                processing_interval=60,
                max_articles_per_source=25,
                memory_limit_mb=2048,
                description="Balanced performance for standard systems (4GB+ RAM, 2+ cores)"
            ),
            "BASIC": PerformancePreset(
                name="BASIC",
                max_workers=min(8, self.cpu_count),
                max_processes=2,
                batch_size=25,
                cache_size=5000,
                request_timeout=8,
                processing_interval=120,
                max_articles_per_source=15,
                memory_limit_mb=1024,
                description="Basic performance for low-resource systems"
            )
        }
        
        return presets.get(preset_name, presets["MEDIUM"])
    
    def get_ml_config(self) -> Dict[str, Any]:
        """Get ML model configuration based on performance preset"""
        base_config = {
            "vectorizer_max_features": 10000,
            "vectorizer_ngram_range": (1, 3),
            "random_forest_estimators": 200,
            "gradient_boosting_estimators": 200,
            "ensemble_voting": "soft",
            "cross_validation_folds": 5,
            "feature_selection_k": 1000,
            "model_cache_size": 100
        }
        
        # Adjust based on preset
        if self.current_preset.name == "ULTRA_HIGH":
            base_config.update({
                "vectorizer_max_features": 20000,
                "random_forest_estimators": 500,
                "gradient_boosting_estimators": 500,
                "feature_selection_k": 2000,
                "model_cache_size": 500
            })
        elif self.current_preset.name == "HIGH":
            base_config.update({
                "vectorizer_max_features": 15000,
                "random_forest_estimators": 300,
                "gradient_boosting_estimators": 300,
                "feature_selection_k": 1500,
                "model_cache_size": 200
            })
        elif self.current_preset.name == "BASIC":
            base_config.update({
                "vectorizer_max_features": 5000,
                "random_forest_estimators": 100,
                "gradient_boosting_estimators": 100,
                "feature_selection_k": 500,
                "model_cache_size": 50
            })
            
        return base_config
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "connection_pool_size": min(50, self.current_preset.max_workers),
            "connection_timeout": 30,
            "query_timeout": 15,
            "batch_insert_size": self.current_preset.batch_size,
            "vacuum_interval_hours": 24,
            "backup_interval_hours": 6,
            "max_db_size_gb": min(10, self.memory_gb * 0.5),
            "enable_wal_mode": True,
            "enable_foreign_keys": True,
            "cache_size_mb": min(512, self.memory_gb * 50)  # 50MB per GB of RAM
        }
    
    def get_network_config(self) -> Dict[str, Any]:
        """Get network configuration for optimal RSS fetching"""
        return {
            "max_concurrent_connections": self.current_preset.max_workers,
            "connection_pool_size": min(200, self.current_preset.max_workers * 2),
            "request_timeout": self.current_preset.request_timeout,
            "max_retries": 3,
            "retry_delay": 1,
            "user_agent": "UltraHighPerformanceMisinformationDetector/2.0",
            "enable_compression": True,
            "enable_keep_alive": True,
            "dns_cache_size": 1000,
            "ssl_verify": True
        }
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring and logging configuration"""
        return {
            "log_level": "INFO",
            "log_file_max_size_mb": 100,
            "log_file_backup_count": 5,
            "metrics_collection_interval": 5,
            "metrics_retention_days": 30,
            "alert_thresholds": {
                "cpu_warning": 75,
                "cpu_critical": 90,
                "memory_warning": 80,
                "memory_critical": 95,
                "disk_warning": 85,
                "disk_critical": 95,
                "throughput_warning": 1.0,
                "response_time_warning": 5000  # milliseconds
            },
            "enable_performance_profiling": True,
            "enable_memory_profiling": False,  # Only for debugging
            "enable_real_time_dashboard": True
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            "enable_rate_limiting": True,
            "rate_limit_requests_per_minute": 1000,
            "enable_cors": True,
            "allowed_origins": ["*"],  # Restrict in production
            "enable_api_key_auth": False,  # Enable for production
            "enable_request_logging": True,
            "enable_input_sanitization": True,
            "max_request_size_mb": 10,
            "enable_sql_injection_protection": True
        }
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get feature flags for experimental features"""
        return {
            "enable_advanced_nlp": True,
            "enable_sentiment_analysis": True,
            "enable_entity_recognition": True,
            "enable_fact_checking_api": False,  # Requires external API
            "enable_image_analysis": False,     # Future feature
            "enable_video_analysis": False,     # Future feature
            "enable_social_media_integration": False,  # Future feature
            "enable_real_time_alerts": True,
            "enable_auto_scaling": True,
            "enable_distributed_processing": False,  # Future feature
            "enable_blockchain_verification": False,  # Future feature
            "enable_ai_explanation": True,
            "enable_multilingual_support": False  # Future feature
        }
    
    def get_rss_sources_config(self) -> Dict[str, Any]:
        """Get RSS sources configuration"""
        return {
            "max_sources": 200,
            "source_timeout": self.current_preset.request_timeout,
            "max_articles_per_source": self.current_preset.max_articles_per_source,
            "source_reliability_threshold": 0.3,
            "enable_source_validation": True,
            "enable_duplicate_detection": True,
            "duplicate_similarity_threshold": 0.85,
            "source_categories": [
                "national", "regional", "business", "technology", 
                "sports", "entertainment", "politics", "health",
                "environment", "international", "alternative"
            ],
            "tier_weights": {
                1: 1.0,    # Premium sources
                2: 0.8,    # Standard sources  
                3: 0.6     # Alternative sources
            }
        }
    
    def export_config(self) -> Dict[str, Any]:
        """Export complete configuration"""
        return {
            "system_info": {
                "cpu_count": self.cpu_count,
                "memory_gb": self.memory_gb,
                "detected_preset": self.current_preset.name
            },
            "performance_preset": {
                "name": self.current_preset.name,
                "description": self.current_preset.description,
                "max_workers": self.current_preset.max_workers,
                "max_processes": self.current_preset.max_processes,
                "batch_size": self.current_preset.batch_size,
                "cache_size": self.current_preset.cache_size,
                "request_timeout": self.current_preset.request_timeout,
                "processing_interval": self.current_preset.processing_interval,
                "max_articles_per_source": self.current_preset.max_articles_per_source,
                "memory_limit_mb": self.current_preset.memory_limit_mb
            },
            "ml_config": self.get_ml_config(),
            "database_config": self.get_database_config(),
            "network_config": self.get_network_config(),
            "monitoring_config": self.get_monitoring_config(),
            "security_config": self.get_security_config(),
            "feature_flags": self.get_feature_flags(),
            "rss_sources_config": self.get_rss_sources_config()
        }
    
    def save_config_to_file(self, filename: str = "ultra_config.json"):
        """Save configuration to JSON file"""
        import json
        config = self.export_config()
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to {filename}")
    
    def print_system_recommendations(self):
        """Print system optimization recommendations"""
        print("\n🚀 ULTRA HIGH-PERFORMANCE SYSTEM ANALYSIS")
        print("=" * 50)
        print(f"🖥️  System: {self.cpu_count} cores, {self.memory_gb:.1f}GB RAM")
        print(f"⚡ Preset: {self.current_preset.name}")
        print(f"📝 Description: {self.current_preset.description}")
        print(f"👥 Workers: {self.current_preset.max_workers} threads, {self.current_preset.max_processes} processes")
        print(f"📦 Batch Size: {self.current_preset.batch_size} events")
        print(f"💾 Cache: {self.current_preset.cache_size:,} items")
        print(f"⏱️  Update Interval: {self.current_preset.processing_interval}s")
        print(f"📰 Articles/Source: {self.current_preset.max_articles_per_source}")
        
        print("\n🎯 PERFORMANCE PREDICTIONS:")
        estimated_throughput = self.current_preset.max_workers * 0.5  # Conservative estimate
        estimated_sources = min(200, self.current_preset.max_workers * 5)
        estimated_events_per_cycle = estimated_sources * self.current_preset.max_articles_per_source * 0.3
        
        print(f"📊 Estimated Throughput: {estimated_throughput:.1f} events/second")
        print(f"📡 Effective Sources: {estimated_sources}")
        print(f"🔄 Events per Cycle: {estimated_events_per_cycle:.0f}")
        print(f"📈 Daily Processing: {estimated_events_per_cycle * (86400 / self.current_preset.processing_interval):,.0f} events")
        
        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")
        if self.memory_gb < 8:
            print("⚠️  Consider upgrading to 8GB+ RAM for better performance")
        if self.cpu_count < 4:
            print("⚠️  Consider upgrading to 4+ CPU cores for parallel processing")
        if self.current_preset.name == "ULTRA_HIGH":
            print("✅ System optimally configured for maximum performance!")
        else:
            print(f"💪 System can be upgraded to {self.get_preset('ULTRA_HIGH').name} preset with more resources")

# Global configuration instance
ultra_config = UltraConfig()

if __name__ == "__main__":
    # Display system analysis and recommendations
    ultra_config.print_system_recommendations()
    
    # Save configuration to file
    ultra_config.save_config_to_file()
    
    print(f"\n📋 Complete configuration exported to ultra_config.json")
    print("🚀 Ready for ultra high-performance misinformation detection!")