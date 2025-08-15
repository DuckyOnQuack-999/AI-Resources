"""
DuckyCoder v6 Configuration Manager
Handles all configuration aspects including modes, formats, and integrations.
"""

import json
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass, asdict


@dataclass
class InputConfig:
    """Configuration for input processing."""
    supported_formats: List[str]
    auto_convert_encoding: bool
    handle_binary: bool
    max_file_size: str
    recursive_directory_scan: bool
    cross_language_deps: bool
    ai_filetype_detection: bool


@dataclass
class ModeConfig:
    """Configuration for operational modes."""
    full_pipeline: bool
    realtime_collaboration: Dict[str, Any]
    continuous_integration: Dict[str, Any]
    security_scanning: Dict[str, Any]
    ui_design: Dict[str, Any]
    debug_assistant: bool
    api_validation: bool
    doc_generator: bool
    performance_profiling: Dict[str, Any]
    quantum_computing: Dict[str, Any]


@dataclass
class ExportConfig:
    """Configuration for export formats."""
    default_formats: List[str]
    output_directory: str
    include_metadata: bool
    compression: bool
    version_control: bool


@dataclass
class SecurityConfig:
    """Configuration for security features."""
    enable_scanning: bool
    compliance_profiles: Dict[str, List[str]]
    enforcement_level: str
    remediation_suggestions: bool
    audit_trail: Dict[str, Any]


class ConfigurationManager:
    """Manages DuckyCoder v6 configuration settings."""
    
    DEFAULT_CONFIG_FILE = "duckycoder_v6_config.yaml"
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = config_path or self.DEFAULT_CONFIG_FILE
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                        config = yaml.safe_load(f)
                    else:
                        config = json.load(f)
                
                self.logger.info(f"Configuration loaded from {self.config_path}")
                return self._validate_and_merge_config(config)
                
            except Exception as e:
                self.logger.error(f"Failed to load config from {self.config_path}: {e}")
                return self._get_default_config()
        else:
            self.logger.info("No configuration file found, using defaults")
            return self._get_default_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_path) or '.', exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                    yaml.dump(config, f, indent=2, default_flow_style=False)
                else:
                    json.dump(config, f, indent=2)
            
            self.logger.info(f"Configuration saved to {self.config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save config to {self.config_path}: {e}")
            return False
    
    def create_default_config(self) -> bool:
        """Create a default configuration file."""
        default_config = self._get_default_config()
        return self.save_config(default_config)
    
    def validate_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Validate configuration structure and values."""
        if config is None:
            config = self.load_config()
        
        try:
            # Validate required sections
            required_sections = [
                'input_config', 'modes', 'export_config', 'security_config',
                'logging', 'performance_monitoring'
            ]
            
            for section in required_sections:
                if section not in config:
                    self.logger.error(f"Missing required configuration section: {section}")
                    return False
            
            # Validate input config
            input_config = config.get('input_config', {})
            if not isinstance(input_config.get('supported_formats'), list):
                self.logger.error("input_config.supported_formats must be a list")
                return False
            
            # Validate modes
            modes = config.get('modes', {})
            if not isinstance(modes, dict):
                self.logger.error("modes must be a dictionary")
                return False
            
            # Validate export config
            export_config = config.get('export_config', {})
            if not isinstance(export_config.get('default_formats'), list):
                self.logger.error("export_config.default_formats must be a list")
                return False
            
            self.logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "version": "6.0.0",
            "input_config": {
                "supported_formats": [
                    "py", "sh", "ps1", "rs", "js", "java", "cs", "go", "ts", "jsx", "tsx",
                    "cpp", "c", "rb", "php", "txt", "md", "json", "xml", "ipynb", "yaml",
                    "csv", "pdf", "docx", "html", "css", "scss", "less", "vue", "svelte",
                    "dart", "kt", "swift", "r", "scala", "clj", "hs", "elm", "ml", "fs"
                ],
                "auto_convert_encoding": True,
                "handle_binary": True,
                "max_file_size": "20MB",
                "recursive_directory_scan": True,
                "cross_language_deps": True,
                "ai_filetype_detection": True
            },
            "modes": {
                "full_pipeline": True,
                "realtime_collaboration": {
                    "enabled": False,
                    "max_participants": 20,
                    "conflict_resolution": "auto"
                },
                "continuous_integration": {
                    "enabled": False,
                    "severity_threshold": "medium",
                    "block_on_errors": True,
                    "slack_notifications": False
                },
                "security_scanning": {
                    "enabled": True,
                    "scan_intensity": "comprehensive",
                    "compliance_standards": ["GDPR", "HIPAA", "PCI", "SOC2", "ISO-27001"]
                },
                "ui_design": {
                    "framework": "auto",
                    "responsive_previews": True,
                    "accessibility_checks": True,
                    "mockup_preview": True
                },
                "debug_assistant": True,
                "api_validation": True,
                "doc_generator": True,
                "performance_profiling": {
                    "enabled": True,
                    "metrics": ["cpu", "memory", "io"],
                    "alert_thresholds": {
                        "cpu": "80%",
                        "memory": "4GB",
                        "io": "100MB/s"
                    },
                    "notification_channels": ["slack", "email"]
                },
                "quantum_computing": {
                    "enabled": False,
                    "framework": "qiskit"
                }
            },
            "export_config": {
                "default_formats": ["markdown", "html", "json"],
                "output_directory": "./duckycoder_output",
                "include_metadata": True,
                "compression": False,
                "version_control": True
            },
            "security_config": {
                "enable_scanning": True,
                "compliance_profiles": {
                    "healthcare": ["HIPAA", "GDPR"],
                    "finance": ["PCI-DSS", "SOX"],
                    "general": ["ISO-27001", "SOC2", "NIST-800-53"]
                },
                "enforcement_level": "strict",
                "remediation_suggestions": True,
                "audit_trail": {
                    "encryption": "AES-256",
                    "retention_period": "90 days"
                }
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "duckycoder_v6.log",
                "max_size": "10MB",
                "backup_count": 5
            },
            "performance_monitoring": {
                "enabled": True,
                "metrics": ["cpu", "memory", "io"],
                "sampling_interval": 1.0,
                "alert_thresholds": {
                    "cpu_percent": 80.0,
                    "memory_mb": 4096,
                    "io_mb_per_sec": 100.0
                }
            },
            "ml_optimization": {
                "enabled": True,
                "model_version": "v6",
                "confidence_threshold": 0.9,
                "optimization_strategies": [
                    "performance_tuning",
                    "memory_optimization",
                    "code_refactoring"
                ]
            },
            "ui_mockup": {
                "enabled": True,
                "frameworks": [
                    "react", "vue", "angular", "flutter", "tkinter", 
                    "pyqt", "kivy", "egui", "dioxus", "tui-rs"
                ],
                "output_formats": ["ascii", "html", "svg"],
                "responsive_breakpoints": ["mobile", "tablet", "desktop"],
                "accessibility_compliance": "WCAG-2.1"
            },
            "integrations": {
                "github": {
                    "enabled": False,
                    "token": "",
                    "webhook_url": ""
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": "",
                    "channel": "#duckycoder"
                },
                "jira": {
                    "enabled": False,
                    "server_url": "",
                    "username": "",
                    "api_token": ""
                },
                "vercel": {
                    "enabled": False,
                    "token": "",
                    "team_id": ""
                }
            }
        }
    
    def _validate_and_merge_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user config and merge with defaults."""
        default_config = self._get_default_config()
        
        # Deep merge user config with defaults
        merged_config = self._deep_merge(default_config, user_config)
        
        # Validate the merged config
        if self.validate_config(merged_config):
            return merged_config
        else:
            self.logger.warning("Invalid user configuration, falling back to defaults")
            return default_config
    
    def _deep_merge(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_mode_config(self, mode_name: str) -> Dict[str, Any]:
        """Get configuration for a specific mode."""
        config = self.load_config()
        return config.get('modes', {}).get(mode_name, {})
    
    def update_mode_config(self, mode_name: str, mode_config: Dict[str, Any]) -> bool:
        """Update configuration for a specific mode."""
        config = self.load_config()
        if 'modes' not in config:
            config['modes'] = {}
        
        config['modes'][mode_name] = mode_config
        return self.save_config(config)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported input formats."""
        config = self.load_config()
        return config.get('input_config', {}).get('supported_formats', [])
    
    def is_format_supported(self, file_extension: str) -> bool:
        """Check if a file format is supported."""
        supported_formats = self.get_supported_formats()
        return file_extension.lower().lstrip('.') in supported_formats
    
    def get_export_formats(self) -> List[str]:
        """Get list of available export formats."""
        config = self.load_config()
        return config.get('export_config', {}).get('default_formats', ['markdown'])
    
    def get_security_profile(self, profile_name: str) -> List[str]:
        """Get security compliance standards for a profile."""
        config = self.load_config()
        security_config = config.get('security_config', {})
        compliance_profiles = security_config.get('compliance_profiles', {})
        return compliance_profiles.get(profile_name, [])