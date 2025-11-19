"""
DuckyCoder v6 UI Mockup Generator
Generates textual and interactive mockups for various UI frameworks.
"""

import asyncio
import logging
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import html


@dataclass
class UIComponent:
    """Represents a UI component detected in code."""
    name: str
    component_type: str
    properties: Dict[str, Any]
    children: List['UIComponent']
    line_number: Optional[int]
    framework: str


@dataclass
class MockupResult:
    """Result from mockup generation."""
    framework: str
    mockup_type: str  # ascii, html, svg, interactive
    content: str
    components_detected: List[UIComponent]
    accessibility_score: float
    responsive_features: List[str]
    metadata: Dict[str, Any]


class UIModelupGenerator:
    """Generates UI mockups for multiple frameworks."""
    
    SUPPORTED_FRAMEWORKS = {
        'react': {
            'components': ['div', 'button', 'input', 'form', 'h1', 'h2', 'h3', 'p', 'span', 'img'],
            'patterns': [r'<(\w+)([^>]*)>', r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>', r'function\s+(\w+)\s*\(']
        },
        'vue': {
            'components': ['v-btn', 'v-text-field', 'v-card', 'v-app-bar', 'v-navigation-drawer'],
            'patterns': [r'<(\w+)([^>]*)>', r'<template>', r'export\s+default']
        },
        'angular': {
            'components': ['mat-button', 'mat-input', 'mat-card', 'mat-toolbar', 'mat-sidenav'],
            'patterns': [r'<(\w+)([^>]*)>', r'@Component', r'selector:']
        },
        'flutter': {
            'components': ['Widget', 'StatefulWidget', 'StatelessWidget', 'Scaffold', 'AppBar', 'Button'],
            'patterns': [r'class\s+(\w+)\s+extends\s+\w*Widget', r'Widget\s+build', r'Scaffold\(']
        },
        'tkinter': {
            'components': ['Tk', 'Frame', 'Button', 'Label', 'Entry', 'Text', 'Canvas', 'Menu'],
            'patterns': [r'(\w+)\s*=\s*tk\.(\w+)', r'(\w+)\s*=\s*tkinter\.(\w+)', r'\.pack\(', r'\.grid\(']
        },
        'pyqt': {
            'components': ['QWidget', 'QPushButton', 'QLabel', 'QLineEdit', 'QTextEdit', 'QMainWindow'],
            'patterns': [r'(\w+)\s*=\s*(Q\w+)\s*\(', r'class\s+(\w+)\(Q\w+\)', r'\.show\(\)']
        },
        'kivy': {
            'components': ['App', 'Widget', 'Button', 'Label', 'TextInput', 'BoxLayout', 'GridLayout'],
            'patterns': [r'class\s+(\w+)\(App\)', r'class\s+(\w+)\(Widget\)', r'Builder\.load_string']
        },
        'egui': {
            'components': ['ui', 'Button', 'Label', 'TextEdit', 'Checkbox', 'Slider'],
            'patterns': [r'ui\.(\w+)', r'egui::', r'central_panel', r'side_panel']
        },
        'dioxus': {
            'components': ['component', 'div', 'button', 'input', 'form'],
            'patterns': [r'rsx!\s*\{', r'#\[component\]', r'fn\s+(\w+)\s*\(.*cx:']
        },
        'tui-rs': {
            'components': ['Block', 'Paragraph', 'List', 'Chart', 'Gauge', 'Table'],
            'patterns': [r'Block::', r'Paragraph::', r'List::', r'terminal\.draw']
        }
    }
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the UI mockup generator."""
        self.config = config
        self.ui_config = config.get('ui_mockup', {})
        self.logger = logging.getLogger(__name__)
        
        # Mockup configuration
        self.enabled = self.ui_config.get('enabled', True)
        self.output_formats = self.ui_config.get('output_formats', ['ascii', 'html'])
        self.responsive_breakpoints = self.ui_config.get('responsive_breakpoints', ['mobile', 'tablet', 'desktop'])
        self.accessibility_compliance = self.ui_config.get('accessibility_compliance', 'WCAG-2.1')
    
    async def generate_mockups(self, enhanced_data: Dict[str, Any], 
                             analysis_data: Dict[str, Any]) -> List[MockupResult]:
        """
        Generate UI mockups based on enhanced content and analysis.
        
        Args:
            enhanced_data: Enhanced content data
            analysis_data: Analysis results
            
        Returns:
            List of MockupResult objects
        """
        if not self.enabled:
            return []
        
        try:
            content = enhanced_data.get('enhanced', {}).get('content', '')
            framework = enhanced_data.get('original', {}).get('metadata', {}).get('framework')
            
            if not framework or not content:
                return []
            
            self.logger.info(f"Generating mockups for framework: {framework}")
            
            # Detect UI components
            components = await self._detect_ui_components(content, framework)
            
            if not components:
                return []
            
            # Generate mockups in different formats
            mockups = []
            
            for output_format in self.output_formats:
                mockup = await self._generate_mockup_by_format(
                    components, framework, output_format, content
                )
                if mockup:
                    mockups.append(mockup)
            
            return mockups
            
        except Exception as e:
            self.logger.error(f"Mockup generation failed: {e}")
            return []
    
    async def _detect_ui_components(self, content: str, framework: str) -> List[UIComponent]:
        """Detect UI components in the content."""
        components = []
        
        if framework not in self.SUPPORTED_FRAMEWORKS:
            return components
        
        framework_config = self.SUPPORTED_FRAMEWORKS[framework]
        patterns = framework_config['patterns']
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Framework-specific component detection
            if framework == 'react':
                components.extend(await self._detect_react_components(line_stripped, i + 1))
            elif framework == 'vue':
                components.extend(await self._detect_vue_components(line_stripped, i + 1))
            elif framework == 'angular':
                components.extend(await self._detect_angular_components(line_stripped, i + 1))
            elif framework == 'flutter':
                components.extend(await self._detect_flutter_components(line_stripped, i + 1))
            elif framework == 'tkinter':
                components.extend(await self._detect_tkinter_components(line_stripped, i + 1))
            elif framework == 'pyqt':
                components.extend(await self._detect_pyqt_components(line_stripped, i + 1))
            elif framework == 'kivy':
                components.extend(await self._detect_kivy_components(line_stripped, i + 1))
            elif framework == 'egui':
                components.extend(await self._detect_egui_components(line_stripped, i + 1))
            elif framework == 'dioxus':
                components.extend(await self._detect_dioxus_components(line_stripped, i + 1))
            elif framework == 'tui-rs':
                components.extend(await self._detect_tui_components(line_stripped, i + 1))
        
        return components
    
    async def _generate_mockup_by_format(self, components: List[UIComponent], 
                                       framework: str, output_format: str, 
                                       content: str) -> Optional[MockupResult]:
        """Generate mockup in specified format."""
        try:
            if output_format == 'ascii':
                mockup_content = await self._generate_ascii_mockup(components, framework)
            elif output_format == 'html':
                mockup_content = await self._generate_html_mockup(components, framework, content)
            elif output_format == 'svg':
                mockup_content = await self._generate_svg_mockup(components, framework)
            else:
                return None
            
            # Calculate accessibility score
            accessibility_score = await self._calculate_accessibility_score(components, content)
            
            # Detect responsive features
            responsive_features = await self._detect_responsive_features(content)
            
            return MockupResult(
                framework=framework,
                mockup_type=output_format,
                content=mockup_content,
                components_detected=components,
                accessibility_score=accessibility_score,
                responsive_features=responsive_features,
                metadata={
                    "component_count": len(components),
                    "generated_at": datetime.now().isoformat(),
                    "breakpoints": self.responsive_breakpoints
                }
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate {output_format} mockup: {e}")
            return None
    
    # Framework-specific component detection methods
    
    async def _detect_react_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect React components."""
        components = []
        
        # JSX elements
        jsx_pattern = r'<(\w+)([^>]*?)(?:/>|>.*?</\1>)'
        matches = re.finditer(jsx_pattern, line)
        
        for match in matches:
            tag_name = match.group(1)
            attributes = match.group(2)
            
            # Parse attributes
            props = {}
            attr_pattern = r'(\w+)=(?:{([^}]+)}|"([^"]*)"|\\'([^\\']*)\\')'
            attr_matches = re.finditer(attr_pattern, attributes)
            
            for attr_match in attr_matches:
                prop_name = attr_match.group(1)
                prop_value = attr_match.group(2) or attr_match.group(3) or attr_match.group(4)
                props[prop_name] = prop_value
            
            component = UIComponent(
                name=tag_name,
                component_type=self._classify_component_type(tag_name, 'react'),
                properties=props,
                children=[],
                line_number=line_num,
                framework='react'
            )
            
            components.append(component)
        
        # React hooks and component definitions
        if 'useState' in line or 'useEffect' in line:
            components.append(UIComponent(
                name='React Hook',
                component_type='state_management',
                properties={'hook_type': 'useState' if 'useState' in line else 'useEffect'},
                children=[],
                line_number=line_num,
                framework='react'
            ))
        
        return components
    
    async def _detect_vue_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect Vue components."""
        components = []
        
        # Vue template elements
        vue_pattern = r'<(v-[\w-]+|[\w-]+)([^>]*?)(?:/>|>)'
        matches = re.finditer(vue_pattern, line)
        
        for match in matches:
            tag_name = match.group(1)
            attributes = match.group(2)
            
            # Parse Vue directives and attributes
            props = {}
            attr_pattern = r'([@:v-]?[\w-]+)=(?:"([^"]*)"|\'([^\']*)\')'
            attr_matches = re.finditer(attr_pattern, attributes)
            
            for attr_match in attr_matches:
                prop_name = attr_match.group(1)
                prop_value = attr_match.group(2) or attr_match.group(3)
                props[prop_name] = prop_value
            
            component = UIComponent(
                name=tag_name,
                component_type=self._classify_component_type(tag_name, 'vue'),
                properties=props,
                children=[],
                line_number=line_num,
                framework='vue'
            )
            
            components.append(component)
        
        return components
    
    async def _detect_angular_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect Angular components."""
        components = []
        
        # Angular Material components
        mat_pattern = r'<(mat-[\w-]+)([^>]*?)(?:/>|>)'
        matches = re.finditer(mat_pattern, line)
        
        for match in matches:
            tag_name = match.group(1)
            attributes = match.group(2)
            
            props = {}
            attr_pattern = r'(\[?[\w-]+\]?)=(?:"([^"]*)"|\'([^\']*)\')'
            attr_matches = re.finditer(attr_pattern, attributes)
            
            for attr_match in attr_matches:
                prop_name = attr_match.group(1)
                prop_value = attr_match.group(2) or attr_match.group(3)
                props[prop_name] = prop_value
            
            component = UIComponent(
                name=tag_name,
                component_type=self._classify_component_type(tag_name, 'angular'),
                properties=props,
                children=[],
                line_number=line_num,
                framework='angular'
            )
            
            components.append(component)
        
        return components
    
    async def _detect_flutter_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect Flutter widgets."""
        components = []
        
        # Flutter widget instantiation
        widget_pattern = r'(\w+)\s*\('
        if 'Widget' in line or any(widget in line for widget in ['Scaffold', 'AppBar', 'Button', 'Text', 'Container']):
            matches = re.finditer(widget_pattern, line)
            
            for match in matches:
                widget_name = match.group(1)
                
                if widget_name[0].isupper():  # Widget names start with uppercase
                    component = UIComponent(
                        name=widget_name,
                        component_type=self._classify_component_type(widget_name, 'flutter'),
                        properties={},
                        children=[],
                        line_number=line_num,
                        framework='flutter'
                    )
                    
                    components.append(component)
        
        return components
    
    async def _detect_tkinter_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect Tkinter components."""
        components = []
        
        # Tkinter widget creation
        tk_pattern = r'(\w+)\s*=\s*(?:tk\.|tkinter\.)?(\w+)\s*\('
        matches = re.finditer(tk_pattern, line)
        
        for match in matches:
            var_name = match.group(1)
            widget_type = match.group(2)
            
            component = UIComponent(
                name=var_name,
                component_type=self._classify_component_type(widget_type, 'tkinter'),
                properties={'widget_type': widget_type},
                children=[],
                line_number=line_num,
                framework='tkinter'
            )
            
            components.append(component)
        
        # Layout methods
        if '.pack(' in line or '.grid(' in line or '.place(' in line:
            layout_type = 'pack' if '.pack(' in line else 'grid' if '.grid(' in line else 'place'
            components.append(UIComponent(
                name=f'{layout_type}_layout',
                component_type='layout',
                properties={'layout_type': layout_type},
                children=[],
                line_number=line_num,
                framework='tkinter'
            ))
        
        return components
    
    async def _detect_pyqt_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect PyQt components."""
        components = []
        
        # PyQt widget creation
        qt_pattern = r'(\w+)\s*=\s*(Q\w+)\s*\('
        matches = re.finditer(qt_pattern, line)
        
        for match in matches:
            var_name = match.group(1)
            widget_type = match.group(2)
            
            component = UIComponent(
                name=var_name,
                component_type=self._classify_component_type(widget_type, 'pyqt'),
                properties={'widget_type': widget_type},
                children=[],
                line_number=line_num,
                framework='pyqt'
            )
            
            components.append(component)
        
        return components
    
    async def _detect_kivy_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect Kivy components."""
        components = []
        
        # Kivy widget usage
        if any(keyword in line for keyword in ['Button', 'Label', 'TextInput', 'BoxLayout', 'GridLayout']):
            kivy_pattern = r'(\w+)\s*\('
            matches = re.finditer(kivy_pattern, line)
            
            for match in matches:
                widget_name = match.group(1)
                
                if widget_name in ['Button', 'Label', 'TextInput', 'BoxLayout', 'GridLayout']:
                    component = UIComponent(
                        name=widget_name,
                        component_type=self._classify_component_type(widget_name, 'kivy'),
                        properties={},
                        children=[],
                        line_number=line_num,
                        framework='kivy'
                    )
                    
                    components.append(component)
        
        return components
    
    async def _detect_egui_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect egui components."""
        components = []
        
        # egui UI calls
        ui_pattern = r'ui\.(\w+)\s*\('
        matches = re.finditer(ui_pattern, line)
        
        for match in matches:
            ui_method = match.group(1)
            
            component = UIComponent(
                name=ui_method,
                component_type=self._classify_component_type(ui_method, 'egui'),
                properties={},
                children=[],
                line_number=line_num,
                framework='egui'
            )
            
            components.append(component)
        
        return components
    
    async def _detect_dioxus_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect Dioxus components."""
        components = []
        
        # Dioxus RSX elements
        if 'rsx!' in line:
            # Simple detection for common HTML-like elements
            html_pattern = r'(\w+)\s*\{'
            matches = re.finditer(html_pattern, line)
            
            for match in matches:
                element_name = match.group(1)
                
                if element_name in ['div', 'button', 'input', 'form', 'p', 'h1', 'h2', 'h3']:
                    component = UIComponent(
                        name=element_name,
                        component_type=self._classify_component_type(element_name, 'dioxus'),
                        properties={},
                        children=[],
                        line_number=line_num,
                        framework='dioxus'
                    )
                    
                    components.append(component)
        
        return components
    
    async def _detect_tui_components(self, line: str, line_num: int) -> List[UIComponent]:
        """Detect TUI-rs components."""
        components = []
        
        # TUI-rs widgets
        tui_pattern = r'(\w+)::'
        matches = re.finditer(tui_pattern, line)
        
        for match in matches:
            widget_type = match.group(1)
            
            if widget_type in ['Block', 'Paragraph', 'List', 'Chart', 'Gauge', 'Table']:
                component = UIComponent(
                    name=widget_type,
                    component_type=self._classify_component_type(widget_type, 'tui-rs'),
                    properties={},
                    children=[],
                    line_number=line_num,
                    framework='tui-rs'
                )
                
                components.append(component)
        
        return components
    
    # Mockup generation methods
    
    async def _generate_ascii_mockup(self, components: List[UIComponent], framework: str) -> str:
        """Generate ASCII art mockup."""
        if not components:
            return "No UI components detected."
        
        mockup_lines = []
        mockup_lines.append(f"# {framework.upper()} UI Mockup")
        mockup_lines.append("=" * 50)
        mockup_lines.append("")
        
        # Group components by type
        component_groups = {}
        for comp in components:
            comp_type = comp.component_type
            if comp_type not in component_groups:
                component_groups[comp_type] = []
            component_groups[comp_type].append(comp)
        
        # Generate layout based on component types
        if framework in ['tkinter', 'pyqt', 'kivy']:
            mockup_lines.extend(await self._generate_desktop_ascii_layout(component_groups, framework))
        elif framework in ['react', 'vue', 'angular']:
            mockup_lines.extend(await self._generate_web_ascii_layout(component_groups, framework))
        elif framework == 'flutter':
            mockup_lines.extend(await self._generate_mobile_ascii_layout(component_groups, framework))
        elif framework == 'tui-rs':
            mockup_lines.extend(await self._generate_terminal_ascii_layout(component_groups, framework))
        else:
            mockup_lines.extend(await self._generate_generic_ascii_layout(component_groups, framework))
        
        return "\n".join(mockup_lines)
    
    async def _generate_html_mockup(self, components: List[UIComponent], 
                                   framework: str, content: str) -> str:
        """Generate HTML mockup with styling."""
        html_parts = []
        
        # HTML document structure
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <title>{framework.title()} UI Mockup</title>')
        html_parts.append('    <style>')
        html_parts.append(await self._generate_mockup_css(framework))
        html_parts.append('    </style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append(f'    <div class="mockup-container {framework}-mockup">')
        html_parts.append(f'        <h1>{framework.title()} UI Preview</h1>')
        
        # Generate component HTML
        for component in components:
            html_parts.append(await self._component_to_html(component, framework))
        
        html_parts.append('    </div>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
    
    async def _generate_svg_mockup(self, components: List[UIComponent], framework: str) -> str:
        """Generate SVG mockup."""
        svg_parts = []
        
        # SVG structure
        svg_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
        svg_parts.append('<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">')
        svg_parts.append('  <defs>')
        svg_parts.append('    <style>')
        svg_parts.append('      .component-rect { fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; }')
        svg_parts.append('      .component-text { font-family: Arial, sans-serif; font-size: 14px; }')
        svg_parts.append('      .title-text { font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; }')
        svg_parts.append('    </style>')
        svg_parts.append('  </defs>')
        
        # Title
        svg_parts.append(f'  <text x="20" y="30" class="title-text">{framework.title()} UI Components</text>')
        
        # Draw components
        y_offset = 60
        for i, component in enumerate(components):
            svg_parts.append(f'  <rect x="20" y="{y_offset}" width="200" height="40" class="component-rect"/>')
            svg_parts.append(f'  <text x="30" y="{y_offset + 25}" class="component-text">{component.name} ({component.component_type})</text>')
            y_offset += 60
        
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    # Layout generation methods
    
    async def _generate_desktop_ascii_layout(self, component_groups: Dict[str, List[UIComponent]], 
                                           framework: str) -> List[str]:
        """Generate desktop application ASCII layout."""
        layout = []
        
        layout.append("┌─────────────────────────────────────────────────┐")
        layout.append("│ Window Title Bar                        [─][□][✕] │")
        layout.append("├─────────────────────────────────────────────────┤")
        
        # Menu bar if present
        if 'menu' in component_groups:
            layout.append("│ File  Edit  View  Tools  Help                   │")
            layout.append("├─────────────────────────────────────────────────┤")
        
        # Main content area
        layout.append("│                                                 │")
        
        # Add detected components
        for comp_type, components in component_groups.items():
            if comp_type in ['button', 'input', 'control']:
                for comp in components[:3]:  # Limit to first 3 components
                    if comp_type == 'button':
                        layout.append(f"│  [ {comp.name} ]                                 │")
                    elif comp_type == 'input':
                        layout.append(f"│  {comp.name}: [________________]                │")
                    else:
                        layout.append(f"│  {comp.name}                                     │")
                layout.append("│                                                 │")
        
        # Fill remaining space
        while len(layout) < 15:
            layout.append("│                                                 │")
        
        layout.append("└─────────────────────────────────────────────────┘")
        
        return layout
    
    async def _generate_web_ascii_layout(self, component_groups: Dict[str, List[UIComponent]], 
                                       framework: str) -> List[str]:
        """Generate web application ASCII layout."""
        layout = []
        
        layout.append("┌─────────────────────────────────────────────────┐")
        layout.append("│ ← → ⟳ 🔒 website.com                            │")
        layout.append("├─────────────────────────────────────────────────┤")
        
        # Navigation/Header
        if 'navigation' in component_groups or 'header' in component_groups:
            layout.append("│ Logo    Home  About  Services  Contact         │")
            layout.append("├─────────────────────────────────────────────────┤")
        
        # Main content
        layout.append("│                                                 │")
        layout.append("│  📄 Main Content Area                          │")
        layout.append("│                                                 │")
        
        # Add detected components
        for comp_type, components in component_groups.items():
            if comp_type in ['button', 'input', 'form', 'control']:
                for comp in components[:3]:
                    if comp_type == 'button':
                        layout.append(f"│    [  {comp.name}  ]                            │")
                    elif comp_type == 'input':
                        layout.append(f"│    {comp.name}: ________________________       │")
                    elif comp_type == 'form':
                        layout.append(f"│    📝 {comp.name} Form                         │")
                    else:
                        layout.append(f"│    • {comp.name}                               │")
                layout.append("│                                                 │")
        
        # Footer
        layout.append("│                                                 │")
        layout.append("├─────────────────────────────────────────────────┤")
        layout.append("│ Footer - © 2024 Company Name                   │")
        layout.append("└─────────────────────────────────────────────────┘")
        
        return layout
    
    async def _generate_mobile_ascii_layout(self, component_groups: Dict[str, List[UIComponent]], 
                                          framework: str) -> List[str]:
        """Generate mobile application ASCII layout."""
        layout = []
        
        layout.append("    ┌─────────────────────┐")
        layout.append("    │ 🔋 📶 12:34  100% │")
        layout.append("    ├─────────────────────┤")
        layout.append("    │ ← App Name      ⋮   │")
        layout.append("    ├─────────────────────┤")
        layout.append("    │                     │")
        
        # Add detected components
        for comp_type, components in component_groups.items():
            if comp_type in ['button', 'input', 'text', 'control']:
                for comp in components[:4]:  # Limit for mobile screen
                    if comp_type == 'button':
                        layout.append(f"    │   [{comp.name}]         │")
                    elif comp_type == 'input':
                        layout.append(f"    │ {comp.name}: ____________ │")
                    elif comp_type == 'text':
                        layout.append(f"    │ {comp.name}              │")
                    else:
                        layout.append(f"    │ • {comp.name}            │")
                layout.append("    │                     │")
        
        # Fill remaining space
        while len(layout) < 20:
            layout.append("    │                     │")
        
        layout.append("    └─────────────────────┘")
        
        return layout
    
    async def _generate_terminal_ascii_layout(self, component_groups: Dict[str, List[UIComponent]], 
                                            framework: str) -> List[str]:
        """Generate terminal UI ASCII layout."""
        layout = []
        
        layout.append("┌─────────────────────────────────────────────────┐")
        layout.append("│ Terminal Application                            │")
        layout.append("├─────────────────────────────────────────────────┤")
        
        # Add TUI components
        for comp_type, components in component_groups.items():
            for comp in components:
                if comp.name == 'Block':
                    layout.append("│ ┌─ Block ──────────────────────────────────────┐ │")
                    layout.append("│ │                                             │ │")
                    layout.append("│ └─────────────────────────────────────────────┘ │")
                elif comp.name == 'Paragraph':
                    layout.append("│ Lorem ipsum dolor sit amet, consectetur...      │")
                elif comp.name == 'List':
                    layout.append("│ • Item 1                                        │")
                    layout.append("│ • Item 2                                        │")
                    layout.append("│ • Item 3                                        │")
                elif comp.name == 'Chart':
                    layout.append("│ ▁▃▅▇█▇▅▃▁ Chart Data                           │")
                else:
                    layout.append(f"│ {comp.name}                                     │")
        
        # Fill remaining space
        while len(layout) < 15:
            layout.append("│                                                 │")
        
        layout.append("└─────────────────────────────────────────────────┘")
        
        return layout
    
    async def _generate_generic_ascii_layout(self, component_groups: Dict[str, List[UIComponent]], 
                                           framework: str) -> List[str]:
        """Generate generic ASCII layout."""
        layout = []
        
        layout.append("┌─────────────────────────────────────────────────┐")
        layout.append(f"│ {framework.title()} Application UI                     │")
        layout.append("├─────────────────────────────────────────────────┤")
        layout.append("│                                                 │")
        
        # List all detected components
        for comp_type, components in component_groups.items():
            layout.append(f"│ {comp_type.title()} Components:                         │")
            for comp in components[:3]:
                layout.append(f"│   • {comp.name}                                  │")
            layout.append("│                                                 │")
        
        # Fill remaining space
        while len(layout) < 12:
            layout.append("│                                                 │")
        
        layout.append("└─────────────────────────────────────────────────┘")
        
        return layout
    
    async def _generate_mockup_css(self, framework: str) -> str:
        """Generate CSS for HTML mockup."""
        css = """
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .mockup-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }
        .component {
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: #fafafa;
        }
        .component-button {
            background: #007bff;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
        }
        .component-input {
            width: 200px;
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        .component-text {
            color: #333;
        }
        """
        
        # Framework-specific styles
        if framework == 'react':
            css += """
            .react-mockup .component {
                border-left: 4px solid #61dafb;
            }
            """
        elif framework == 'vue':
            css += """
            .vue-mockup .component {
                border-left: 4px solid #4fc08d;
            }
            """
        elif framework == 'angular':
            css += """
            .angular-mockup .component {
                border-left: 4px solid #dd0031;
            }
            """
        
        return css
    
    async def _component_to_html(self, component: UIComponent, framework: str) -> str:
        """Convert a UI component to HTML representation."""
        comp_type = component.component_type
        comp_name = html.escape(component.name)
        
        html_parts = [f'        <div class="component component-{comp_type}">']
        html_parts.append(f'            <strong>{comp_name}</strong> ({comp_type})')
        
        if comp_type == 'button':
            html_parts.append(f'            <br><button class="component-button">{comp_name}</button>')
        elif comp_type == 'input':
            html_parts.append(f'            <br><input class="component-input" placeholder="{comp_name}" />')
        elif comp_type == 'text':
            html_parts.append(f'            <br><span class="component-text">{comp_name} content</span>')
        
        # Add properties if any
        if component.properties:
            html_parts.append('            <br><small>Properties: ')
            props = ', '.join([f"{k}: {v}" for k, v in component.properties.items()])
            html_parts.append(html.escape(props))
            html_parts.append('</small>')
        
        html_parts.append('        </div>')
        
        return '\n'.join(html_parts)
    
    # Helper methods
    
    def _classify_component_type(self, component_name: str, framework: str) -> str:
        """Classify component type based on name and framework."""
        name_lower = component_name.lower()
        
        # Common classifications
        if any(keyword in name_lower for keyword in ['button', 'btn']):
            return 'button'
        elif any(keyword in name_lower for keyword in ['input', 'field', 'edit', 'entry']):
            return 'input'
        elif any(keyword in name_lower for keyword in ['text', 'label', 'paragraph', 'heading']):
            return 'text'
        elif any(keyword in name_lower for keyword in ['form', 'dialog', 'modal']):
            return 'container'
        elif any(keyword in name_lower for keyword in ['layout', 'box', 'grid', 'frame']):
            return 'layout'
        elif any(keyword in name_lower for keyword in ['menu', 'nav', 'bar']):
            return 'navigation'
        elif any(keyword in name_lower for keyword in ['list', 'table', 'chart', 'graph']):
            return 'data_display'
        elif any(keyword in name_lower for keyword in ['image', 'img', 'icon']):
            return 'media'
        else:
            return 'control'
    
    async def _calculate_accessibility_score(self, components: List[UIComponent], 
                                           content: str) -> float:
        """Calculate accessibility score for the UI."""
        score = 10.0
        
        # Check for accessibility features
        accessibility_features = [
            'alt=', 'aria-label', 'aria-describedby', 'role=', 'tabindex',
            'aria-hidden', 'aria-expanded', 'aria-current'
        ]
        
        feature_count = sum(1 for feature in accessibility_features if feature in content)
        score += feature_count * 0.5
        
        # Penalize missing accessibility in interactive components
        interactive_components = [comp for comp in components 
                                if comp.component_type in ['button', 'input', 'navigation']]
        
        if interactive_components and feature_count == 0:
            score -= 3.0
        
        # Check for semantic HTML elements
        semantic_elements = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        semantic_count = sum(1 for element in semantic_elements if element in content.lower())
        score += semantic_count * 0.3
        
        return min(10.0, max(0.0, score))
    
    async def _detect_responsive_features(self, content: str) -> List[str]:
        """Detect responsive design features."""
        features = []
        
        responsive_indicators = {
            '@media': 'media_queries',
            'viewport': 'viewport_meta',
            'rem': 'relative_units',
            'vh': 'viewport_units',
            'vw': 'viewport_units',
            'grid': 'css_grid',
            'flexbox': 'flexbox_layout',
            'flex': 'flexbox_layout',
            'responsive': 'responsive_classes',
            'mobile': 'mobile_optimization',
            'tablet': 'tablet_optimization'
        }
        
        content_lower = content.lower()
        for indicator, feature in responsive_indicators.items():
            if indicator in content_lower and feature not in features:
                features.append(feature)
        
        return features
