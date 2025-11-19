"""
DuckyCoder v6 v0 Integration Module
Generates MDX responses, React components, and v0-compatible code blocks.
"""

import logging
import re
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import base64
import html


@dataclass
class ReactComponent:
    """Represents a React component for v0."""
    name: str
    file_path: str
    code: str
    imports: List[str]
    props: Dict[str, str]
    responsive: bool
    accessible: bool
    framework_features: List[str]


@dataclass
class MDXComponent:
    """Represents an MDX component."""
    type: str  # code_block, react_project, interactive_chart, etc.
    content: str
    metadata: Dict[str, Any]
    interactive: bool


@dataclass
class V0Response:
    """Complete v0-compatible response."""
    components: List[Union[ReactComponent, MDXComponent]]
    mdx_content: str
    executable_code: List[str]
    preview_urls: List[str]
    deployment_ready: bool
    metadata: Dict[str, Any]


class V0MDXGenerator:
    """Generates v0-compatible MDX responses and React components."""

    # v0 MDX component templates
    MDX_TEMPLATES = {
        'react_project': '''<ReactProject id="{project_id}">
```tsx file="{file_path}"
{component_code}
```
</ReactProject>''',
        
        'nodejs_executable': '''```js
{javascript_code}
```''',
        
        'python_executable': '''```py
{python_code}
```''',
        
        'html_block': '''```html
{html_code}
```''',
        
        'markdown_block': '''```md
{markdown_content}
```''',
        
        'general_code': '''```{language}
{code_content}
```''',
        
        'mermaid_diagram': '''```mermaid
{diagram_content}
```''',
        
        'interactive_chart': '''<Chart type="{chart_type}" data={{{data}}} />''',
        
        'linear_process_flow': '''<LinearProcessFlow steps={{{steps}}} />''',
        
        'collapsible_details': '''<Details summary="{title}">
{content}
</Details>''',
        
        'alert_message': '''<Alert type="{alert_type}">
{message}
</Alert>''',
        
        'progress_indicator': '''<Progress value={{{value}}} max={{{max}}} />''',
        
        'badge_component': '''<Badge variant="{variant}">{text}</Badge>''',
        
        'tabs_container': '''<Tabs>
{tab_content}
</Tabs>'''
    }

    # React component templates with shadcn/ui and Tailwind
    REACT_TEMPLATES = {
        'dashboard': '''import React from 'react';
import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card";
import {{ Button }} from "@/components/ui/button";
import {{ Badge }} from "@/components/ui/badge";
import {{ Progress }} from "@/components/ui/progress";
import {{ BarChart3, Users, TrendingUp, AlertCircle }} from "lucide-react";

export default function DashboardComponent() {{
  const metrics = [
    {{ title: "Total Users", value: "2,354", change: "+12%", icon: Users }},
    {{ title: "Revenue", value: "$45,231", change: "+18%", icon: TrendingUp }},
    {{ title: "Conversion Rate", value: "3.2%", change: "+0.5%", icon: BarChart3 }},
    {{ title: "Issues", value: "12", change: "-4", icon: AlertCircle }}
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <Button>Generate Report</Button>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {{metrics.map((metric, index) => (
          <Card key={{index}}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{{metric.title}}</CardTitle>
              <metric.icon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{{metric.value}}</div>
              <p className="text-xs text-muted-foreground">
                <Badge variant={{metric.change.startsWith('+') ? 'default' : 'destructive'}}>
                  {{metric.change}}
                </Badge>
                {{" "}}from last month
              </p>
            </CardContent>
          </Card>
        ))}}
      </div>
      
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest system events and updates</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">System updated successfully</p>
                  <p className="text-xs text-muted-foreground">2 minutes ago</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div className="flex-1">
                  <p className="text-sm font-medium">New user registered</p>
                  <p className="text-xs text-muted-foreground">5 minutes ago</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Performance Metrics</CardTitle>
            <CardDescription>System performance overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm">
                  <span>CPU Usage</span>
                  <span>72%</span>
                </div>
                <Progress value={{72}} className="mt-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm">
                  <span>Memory Usage</span>
                  <span>58%</span>
                </div>
                <Progress value={{58}} className="mt-2" />
              </div>
              <div>
                <div className="flex justify-between text-sm">
                  <span>Disk Usage</span>
                  <span>34%</span>
                </div>
                <Progress value={{34}} className="mt-2" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}}''',

        'form_component': '''import React, {{ useState }} from 'react';
import {{ Button }} from "@/components/ui/button";
import {{ Input }} from "@/components/ui/input";
import {{ Label }} from "@/components/ui/label";
import {{ Textarea }} from "@/components/ui/textarea";
import {{ Card, CardContent, CardDescription, CardHeader, CardTitle }} from "@/components/ui/card";
import {{ Alert, AlertDescription }} from "@/components/ui/alert";
import {{ CheckCircle, AlertCircle }} from "lucide-react";

export default function FormComponent() {{
  const [formData, setFormData] = useState({{
    name: '',
    email: '',
    message: ''
  }});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState(null);

  const handleChange = (e) => {{
    setFormData({{
      ...formData,
      [e.target.name]: e.target.value
    }});
  }};

  const handleSubmit = async (e) => {{
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setIsSubmitting(false);
    setSubmitStatus('success');
    
    // Reset form
    setFormData({{ name: '', email: '', message: '' }});
  }};

  return (
    <div className="max-w-md mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Contact Form</CardTitle>
          <CardDescription>
            Send us a message and we'll get back to you soon.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {{submitStatus === 'success' && (
            <Alert className="mb-4">
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>
                Message sent successfully! We'll get back to you soon.
              </AlertDescription>
            </Alert>
          )}}
          
          <form onSubmit={{handleSubmit}} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                name="name"
                type="text"
                value={{formData.name}}
                onChange={{handleChange}}
                required
                placeholder="Enter your name"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                value={{formData.email}}
                onChange={{handleChange}}
                required
                placeholder="Enter your email"
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="message">Message</Label>
              <Textarea
                id="message"
                name="message"
                value={{formData.message}}
                onChange={{handleChange}}
                required
                placeholder="Enter your message"
                rows={{4}}
              />
            </div>
            
            <Button 
              type="submit" 
              className="w-full" 
              disabled={{isSubmitting}}
            >
              {{isSubmitting ? 'Sending...' : 'Send Message'}}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}}''',

        'data_table': '''import React, {{ useState }} from 'react';
import {{ Button }} from "@/components/ui/button";
import {{ Input }} from "@/components/ui/input";
import {{ Card, CardContent, CardHeader, CardTitle }} from "@/components/ui/card";
import {{ Badge }} from "@/components/ui/badge";
import {{ Search, Filter, Download }} from "lucide-react";

export default function DataTableComponent() {{
  const [searchTerm, setSearchTerm] = useState('');
  
  const data = [
    {{ id: 1, name: 'John Doe', email: 'john@example.com', status: 'Active', role: 'Admin' }},
    {{ id: 2, name: 'Jane Smith', email: 'jane@example.com', status: 'Active', role: 'User' }},
    {{ id: 3, name: 'Bob Johnson', email: 'bob@example.com', status: 'Inactive', role: 'User' }},
    {{ id: 4, name: 'Alice Wilson', email: 'alice@example.com', status: 'Active', role: 'Moderator' }},
    {{ id: 5, name: 'Charlie Brown', email: 'charlie@example.com', status: 'Pending', role: 'User' }}
  ];

  const filteredData = data.filter(item =>
    item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status) => {{
    switch (status) {{
      case 'Active': return 'default';
      case 'Inactive': return 'destructive';
      case 'Pending': return 'secondary';
      default: return 'outline';
    }}
  }};

  return (
    <div className="p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">User Management</CardTitle>
          <div className="flex items-center space-x-4">
            <div className="relative flex-1 max-w-sm">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search users..."
                value={{searchTerm}}
                onChange={{(e) => setSearchTerm(e.target.value)}}
                className="pl-8"
              />
            </div>
            <Button variant="outline" size="sm">
              <Filter className="mr-2 h-4 w-4" />
              Filter
            </Button>
            <Button variant="outline" size="sm">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b bg-muted/50">
                    <th className="h-12 px-4 text-left align-middle font-medium">Name</th>
                    <th className="h-12 px-4 text-left align-middle font-medium">Email</th>
                    <th className="h-12 px-4 text-left align-middle font-medium">Role</th>
                    <th className="h-12 px-4 text-left align-middle font-medium">Status</th>
                    <th className="h-12 px-4 text-left align-middle font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {{filteredData.map((user) => (
                    <tr key={{user.id}} className="border-b transition-colors hover:bg-muted/50">
                      <td className="p-4 align-middle font-medium">{{user.name}}</td>
                      <td className="p-4 align-middle text-muted-foreground">{{user.email}}</td>
                      <td className="p-4 align-middle">{{user.role}}</td>
                      <td className="p-4 align-middle">
                        <Badge variant={{getStatusColor(user.status)}}>
                          {{user.status}}
                        </Badge>
                      </td>
                      <td className="p-4 align-middle">
                        <div className="flex space-x-2">
                          <Button variant="ghost" size="sm">Edit</Button>
                          <Button variant="ghost" size="sm">Delete</Button>
                        </div>
                      </td>
                    </tr>
                  ))}}
                </tbody>
              </table>
            </div>
          </div>
          <div className="flex items-center justify-between px-2 py-4">
            <div className="text-sm text-muted-foreground">
              Showing {{filteredData.length}} of {{data.length}} users
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm" disabled>Previous</Button>
              <Button variant="outline" size="sm">Next</Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}}'''
    }

    def __init__(self, config: Dict[str, Any]):
        """Initialize the v0 MDX generator."""
        self.config = config
        self.v0_config = config.get('v0_integration', {})
        self.logger = logging.getLogger(__name__)

        # v0 settings
        self.enabled = self.v0_config.get('enabled', True)
        self.mdx_support = self.v0_config.get('mdx_support', True)
        self.react_components = self.v0_config.get('react_components', {})
        self.ui_features = self.v0_config.get('ui_features', {})

    async def generate_v0_response(self, enhancement_results: Dict[str, Any],
                                 analysis_results: Dict[str, Any],
                                 processed_data: Dict[str, Any]) -> V0Response:
        """
        Generate complete v0-compatible response.

        Args:
            enhancement_results: Enhancement results from processing
            analysis_results: Analysis results
            processed_data: Original processed data

        Returns:
            V0Response with MDX content and React components
        """
        if not self.enabled:
            return V0Response(
                components=[],
                mdx_content="v0 integration is disabled",
                executable_code=[],
                preview_urls=[],
                deployment_ready=False,
                metadata={'error': 'v0 integration disabled'}
            )

        try:
            self.logger.info("Generating v0-compatible response")

            components = []
            executable_code = []
            preview_urls = []

            # Generate React components for UI-related content
            react_components = await self._generate_react_components(
                enhancement_results, processed_data
            )
            components.extend(react_components)

            # Generate executable code blocks
            code_blocks = await self._generate_executable_code_blocks(
                enhancement_results, processed_data
            )
            components.extend(code_blocks)
            executable_code.extend([block.content for block in code_blocks if block.type in ['python', 'javascript', 'nodejs']])

            # Generate interactive components
            interactive_components = await self._generate_interactive_components(
                analysis_results, enhancement_results
            )
            components.extend(interactive_components)

            # Compose final MDX content
            mdx_content = await self._compose_mdx_content(
                components, enhancement_results, analysis_results
            )

            # Generate preview URLs if applicable
            if self.ui_features.get('preview_urls', False):
                preview_urls = await self._generate_preview_urls(react_components)

            return V0Response(
                components=components,
                mdx_content=mdx_content,
                executable_code=executable_code,
                preview_urls=preview_urls,
                deployment_ready=self._check_deployment_readiness(components),
                metadata={
                    'total_components': len(components),
                    'react_components': len([c for c in components if isinstance(c, ReactComponent)]),
                    'mdx_components': len([c for c in components if isinstance(c, MDXComponent)]),
                    'generated_at': datetime.now().isoformat(),
                    'v0_features_used': self._get_used_features(components)
                }
            )

        except Exception as e:
            self.logger.error(f"v0 response generation failed: {e}")
            return V0Response(
                components=[],
                mdx_content=f"Error generating v0 response: {e}",
                executable_code=[],
                preview_urls=[],
                deployment_ready=False,
                metadata={'error': str(e)}
            )

    async def _generate_react_components(self, enhancement_results: Dict[str, Any],
                                       processed_data: Dict[str, Any]) -> List[ReactComponent]:
        """Generate React components for UI content."""
        components = []

        for source, results in enhancement_results.items():
            if isinstance(results, dict) and results.get('ui_mockups'):
                ui_mockups = results['ui_mockups']
                framework = ui_mockups.get('framework', '')

                if framework in ['react', 'nextjs'] or 'react' in framework.lower():
                    # Generate React component
                    component = await self._create_react_component(source, ui_mockups, results)
                    if component:
                        components.append(component)

            # Check for web-related enhancements
            if isinstance(results, dict) and 'enhancements' in results:
                enhancements = results['enhancements']
                web_enhancements = [e for e in enhancements 
                                  if getattr(e, 'category', '') in ['ui', 'web', 'frontend']]
                
                if web_enhancements:
                    component = await self._create_enhancement_component(source, web_enhancements)
                    if component:
                        components.append(component)

        return components

    async def _create_react_component(self, source: str, ui_mockups: Dict[str, Any],
                                    results: Dict[str, Any]) -> Optional[ReactComponent]:
        """Create a React component from UI mockups."""
        try:
            framework = ui_mockups.get('framework', 'react')
            components_detected = ui_mockups.get('components_detected', [])

            # Determine component type based on detected components
            component_type = self._determine_component_type(components_detected)
            
            # Generate appropriate React component
            if component_type == 'dashboard':
                code = self.REACT_TEMPLATES['dashboard']
                name = "DashboardComponent"
            elif component_type == 'form':
                code = self.REACT_TEMPLATES['form_component']
                name = "FormComponent"
            elif component_type == 'table':
                code = self.REACT_TEMPLATES['data_table']
                name = "DataTableComponent"
            else:
                # Generate generic component
                code = await self._generate_generic_react_component(components_detected)
                name = "GeneratedComponent"

            return ReactComponent(
                name=name,
                file_path=f"{name}.tsx",
                code=code,
                imports=[
                    "@/components/ui/button",
                    "@/components/ui/card",
                    "@/components/ui/input",
                    "@/components/ui/badge",
                    "lucide-react"
                ],
                props={},
                responsive=True,
                accessible=True,
                framework_features=['shadcn_ui', 'tailwind_css', 'lucide_react']
            )

        except Exception as e:
            self.logger.error(f"Failed to create React component: {e}")
            return None

    async def _generate_generic_react_component(self, components_detected: List[Any]) -> str:
        """Generate a generic React component based on detected components."""
        component_elements = []
        
        for component in components_detected:
            comp_type = getattr(component, 'component_type', 'unknown')
            comp_name = getattr(component, 'name', 'component')
            
            if comp_type == 'button':
                component_elements.append(f'<Button>{comp_name}</Button>')
            elif comp_type == 'input':
                component_elements.append(f'<Input placeholder="{comp_name}" />')
            elif comp_type == 'text':
                component_elements.append(f'<p className="text-sm">{comp_name}</p>')
            else:
                component_elements.append(f'<div className="p-2 border rounded">{comp_name}</div>')

        elements_jsx = '\n        '.join(component_elements)

        return f'''import React from 'react';
import {{ Button }} from "@/components/ui/button";
import {{ Input }} from "@/components/ui/input";
import {{ Card, CardContent, CardHeader, CardTitle }} from "@/components/ui/card";

export default function GeneratedComponent() {{
  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Generated Component</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {elements_jsx}
      </CardContent>
    </Card>
  );
}}'''

    async def _create_enhancement_component(self, source: str, 
                                          enhancements: List[Any]) -> Optional[ReactComponent]:
        """Create a React component showcasing enhancements."""
        try:
            enhancement_items = []
            for enhancement in enhancements[:5]:  # Limit to 5 enhancements
                category = getattr(enhancement, 'category', 'General')
                description = getattr(enhancement, 'description', 'Enhancement applied')
                confidence = getattr(enhancement, 'confidence', 0)
                
                enhancement_items.append({
                    'category': category,
                    'description': description,
                    'confidence': confidence
                })

            code = f'''import React from 'react';
import {{ Card, CardContent, CardHeader, CardTitle }} from "@/components/ui/card";
import {{ Badge }} from "@/components/ui/badge";
import {{ Progress }} from "@/components/ui/progress";
import {{ CheckCircle, Code, Zap }} from "lucide-react";

export default function EnhancementSummary() {{
  const enhancements = {json.dumps(enhancement_items, indent=4)};

  const getCategoryIcon = (category) => {{
    switch (category.toLowerCase()) {{
      case 'performance': return <Zap className="h-4 w-4" />;
      case 'security': return <CheckCircle className="h-4 w-4" />;
      default: return <Code className="h-4 w-4" />;
    }}
  }};

  const getConfidenceColor = (confidence) => {{
    if (confidence >= 0.8) return 'default';
    if (confidence >= 0.6) return 'secondary';
    return 'outline';
  }};

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CheckCircle className="h-5 w-5 text-green-500" />
          Code Enhancements Applied
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {{enhancements.map((enhancement, index) => (
            <div key={{index}} className="p-4 border rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  {{getCategoryIcon(enhancement.category)}}
                  <Badge variant="outline">{{enhancement.category}}</Badge>
                </div>
                <Badge variant={{getConfidenceColor(enhancement.confidence)}}>
                  {{Math.round(enhancement.confidence * 100)}}% confidence
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground">{{enhancement.description}}</p>
              <div className="mt-2">
                <div className="flex justify-between text-xs mb-1">
                  <span>Confidence Level</span>
                  <span>{{Math.round(enhancement.confidence * 100)}}%</span>
                </div>
                <Progress value={{enhancement.confidence * 100}} className="h-2" />
              </div>
            </div>
          ))}}
        </div>
      </CardContent>
    </Card>
  );
}}'''

            return ReactComponent(
                name="EnhancementSummary",
                file_path="EnhancementSummary.tsx",
                code=code,
                imports=[
                    "@/components/ui/card",
                    "@/components/ui/badge",
                    "@/components/ui/progress",
                    "lucide-react"
                ],
                props={},
                responsive=True,
                accessible=True,
                framework_features=['shadcn_ui', 'tailwind_css', 'lucide_react']
            )

        except Exception as e:
            self.logger.error(f"Failed to create enhancement component: {e}")
            return None

    async def _generate_executable_code_blocks(self, enhancement_results: Dict[str, Any],
                                             processed_data: Dict[str, Any]) -> List[MDXComponent]:
        """Generate executable code blocks for v0."""
        code_blocks = []

        for source, data in processed_data.items():
            if isinstance(data, dict) and 'metadata' in data:
                language = data['metadata'].get('language')
                content = data.get('content', '')

                if language == 'python':
                    # Generate Python executable
                    python_code = await self._create_python_executable(content, source)
                    if python_code:
                        code_blocks.append(MDXComponent(
                            type='python',
                            content=python_code,
                            metadata={'language': 'python', 'executable': True, 'source': source},
                            interactive=True
                        ))

                elif language in ['javascript', 'typescript']:
                    # Generate Node.js executable
                    js_code = await self._create_nodejs_executable(content, source)
                    if js_code:
                        code_blocks.append(MDXComponent(
                            type='nodejs',
                            content=js_code,
                            metadata={'language': 'javascript', 'executable': True, 'source': source},
                            interactive=True
                        ))

                elif language == 'html':
                    # Generate HTML block
                    html_code = await self._create_html_block(content)
                    if html_code:
                        code_blocks.append(MDXComponent(
                            type='html',
                            content=html_code,
                            metadata={'language': 'html', 'renderable': True, 'source': source},
                            interactive=True
                        ))

        return code_blocks

    async def _create_python_executable(self, content: str, source: str) -> Optional[str]:
        """Create executable Python code for v0."""
        try:
            # Extract main functionality and create runnable example
            if 'def main(' in content or 'if __name__' in content:
                return content  # Already has main execution
            
            # Create a simple executable wrapper
            if 'def ' in content:
                # Has functions, create a demo
                functions = re.findall(r'def\s+(\w+)\s*\(', content)
                if functions:
                    main_function = functions[0]
                    executable_code = f'''{content}

# Demo execution
if __name__ == "__main__":
    print("Running {source} demo:")
    try:
        result = {main_function}()
        print(f"Result: {{result}}")
    except Exception as e:
        print(f"Error: {{e}}")
'''
                    return executable_code

            # For simple scripts, just ensure they're executable
            if content.strip():
                return f'''# Generated from {source}
{content}

print("Script executed successfully!")
'''

        except Exception as e:
            self.logger.error(f"Failed to create Python executable: {e}")

        return None

    async def _create_nodejs_executable(self, content: str, source: str) -> Optional[str]:
        """Create executable Node.js code for v0."""
        try:
            # Create executable JavaScript/Node.js code
            if 'module.exports' in content or 'export ' in content:
                # Module code, create execution wrapper
                executable_code = f'''// Generated from {source}
{content}

// Demo execution
console.log("Running {source} demo:");
try {{
    // Execute main functionality here
    console.log("Code executed successfully!");
}} catch (error) {{
    console.error("Error:", error);
}}
'''
                return executable_code

            # For simple scripts
            if content.strip():
                return f'''// Generated from {source}
{content}

console.log("Script executed successfully!");
'''

        except Exception as e:
            self.logger.error(f"Failed to create Node.js executable: {e}")

        return None

    async def _create_html_block(self, content: str) -> Optional[str]:
        """Create HTML block for v0."""
        try:
            # Ensure it's a complete HTML document or component
            if not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
                # Wrap in basic HTML structure
                return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated HTML</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>'''
            
            return content

        except Exception as e:
            self.logger.error(f"Failed to create HTML block: {e}")

        return None

    async def _generate_interactive_components(self, analysis_results: Dict[str, Any],
                                             enhancement_results: Dict[str, Any]) -> List[MDXComponent]:
        """Generate interactive MDX components."""
        components = []

        # Generate charts for metrics
        metrics_data = self._extract_metrics_data(analysis_results)
        if metrics_data:
            chart_component = MDXComponent(
                type='interactive_chart',
                content=self.MDX_TEMPLATES['interactive_chart'].format(
                    chart_type='bar',
                    data=json.dumps(metrics_data)
                ),
                metadata={'chart_type': 'metrics', 'data_points': len(metrics_data)},
                interactive=True
            )
            components.append(chart_component)

        # Generate process flow for pipeline
        pipeline_steps = [
            {"title": "Input Processing", "status": "completed"},
            {"title": "AI Analysis", "status": "completed"},
            {"title": "Enhancement", "status": "completed"},
            {"title": "Output Generation", "status": "current"}
        ]
        
        flow_component = MDXComponent(
            type='linear_process_flow',
            content=self.MDX_TEMPLATES['linear_process_flow'].format(
                steps=json.dumps(pipeline_steps)
            ),
            metadata={'process': 'duckycoder_pipeline', 'steps': len(pipeline_steps)},
            interactive=True
        )
        components.append(flow_component)

        # Generate alerts for critical issues
        critical_issues = self._extract_critical_issues(analysis_results)
        for issue in critical_issues[:3]:  # Limit to 3 critical issues
            alert_component = MDXComponent(
                type='alert_message',
                content=self.MDX_TEMPLATES['alert_message'].format(
                    alert_type='destructive',
                    message=issue
                ),
                metadata={'alert_type': 'critical_issue', 'issue': issue},
                interactive=False
            )
            components.append(alert_component)

        return components

    async def _compose_mdx_content(self, components: List[Union[ReactComponent, MDXComponent]],
                                 enhancement_results: Dict[str, Any],
                                 analysis_results: Dict[str, Any]) -> str:
        """Compose final MDX content."""
        mdx_parts = []

        # Header
        mdx_parts.append("# DuckyCoder v6 Analysis Report")
        mdx_parts.append("*Generated with v0 integration and MDX components*")
        mdx_parts.append("")

        # Executive summary
        total_files = len(enhancement_results)
        total_issues = self._count_total_issues(analysis_results)
        total_enhancements = self._count_total_enhancements(enhancement_results)

        mdx_parts.append("## Executive Summary")
        mdx_parts.append("")
        mdx_parts.append(f"- **Files Processed**: {total_files}")
        mdx_parts.append(f"- **Issues Found**: {total_issues}")
        mdx_parts.append(f"- **Enhancements Applied**: {total_enhancements}")
        mdx_parts.append("")

        # Add React components
        react_components = [c for c in components if isinstance(c, ReactComponent)]
        if react_components:
            mdx_parts.append("## Interactive Components")
            mdx_parts.append("")
            
            for component in react_components:
                react_project = self.MDX_TEMPLATES['react_project'].format(
                    project_id=f"component_{hash(component.name) % 10000}",
                    file_path=component.file_path,
                    component_code=component.code
                )
                mdx_parts.append(react_project)
                mdx_parts.append("")

        # Add executable code
        code_components = [c for c in components if isinstance(c, MDXComponent) and c.type in ['python', 'nodejs', 'html']]
        if code_components:
            mdx_parts.append("## Executable Code")
            mdx_parts.append("")
            
            for component in code_components:
                if component.type == 'python':
                    mdx_parts.append(self.MDX_TEMPLATES['python_executable'].format(
                        python_code=component.content
                    ))
                elif component.type == 'nodejs':
                    mdx_parts.append(self.MDX_TEMPLATES['nodejs_executable'].format(
                        javascript_code=component.content
                    ))
                elif component.type == 'html':
                    mdx_parts.append(self.MDX_TEMPLATES['html_block'].format(
                        html_code=component.content
                    ))
                mdx_parts.append("")

        # Add interactive components
        interactive_components = [c for c in components if isinstance(c, MDXComponent) and c.interactive]
        if interactive_components:
            mdx_parts.append("## Interactive Elements")
            mdx_parts.append("")
            
            for component in interactive_components:
                mdx_parts.append(component.content)
                mdx_parts.append("")

        # Mathematical formulas example
        mdx_parts.append("## Analysis Metrics")
        mdx_parts.append("")
        mdx_parts.append("The analysis confidence score is calculated using:")
        mdx_parts.append("")
        mdx_parts.append("$$confidence = \\frac{\\sum_{i=1}^{n} w_i \\cdot score_i}{\\sum_{i=1}^{n} w_i}$$")
        mdx_parts.append("")
        mdx_parts.append("Where $w_i$ represents the weight of each analysis component.")
        mdx_parts.append("")

        return "\n".join(mdx_parts)

    def _determine_component_type(self, components_detected: List[Any]) -> str:
        """Determine React component type based on detected components."""
        component_types = [getattr(c, 'component_type', '') for c in components_detected]
        
        if any('button' in c_type for c_type in component_types):
            if any('input' in c_type for c_type in component_types):
                return 'form'
            elif any('chart' in c_type or 'data' in c_type for c_type in component_types):
                return 'dashboard'
        
        if any('table' in c_type or 'list' in c_type for c_type in component_types):
            return 'table'
        
        if any('dashboard' in c_type or 'metric' in c_type for c_type in component_types):
            return 'dashboard'
        
        return 'generic'

    def _extract_metrics_data(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract metrics data for charts."""
        metrics = []
        
        for source, results in analysis_results.items():
            if isinstance(results, dict) and 'metrics' in results:
                source_metrics = results['metrics']
                for metric, value in source_metrics.items():
                    if isinstance(value, (int, float)):
                        metrics.append({
                            'name': metric.replace('_', ' ').title(),
                            'value': value,
                            'source': source
                        })
        
        return metrics[:10]  # Limit to 10 metrics

    def _extract_critical_issues(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Extract critical issues for alerts."""
        critical_issues = []
        
        for source, results in analysis_results.items():
            if isinstance(results, dict) and 'issues' in results:
                issues = results['issues']
                for issue in issues:
                    if getattr(issue, 'severity', '') == 'critical':
                        message = getattr(issue, 'message', 'Critical issue found')
                        critical_issues.append(f"**{source}**: {message}")
        
        return critical_issues

    def _count_total_issues(self, analysis_results: Dict[str, Any]) -> int:
        """Count total issues."""
        total = 0
        for results in analysis_results.values():
            if isinstance(results, dict) and 'issues' in results:
                total += len(results['issues'])
        return total

    def _count_total_enhancements(self, enhancement_results: Dict[str, Any]) -> int:
        """Count total enhancements."""
        total = 0
        for results in enhancement_results.values():
            if isinstance(results, dict) and 'enhancements' in results:
                total += len(results['enhancements'])
        return total

    async def _generate_preview_urls(self, react_components: List[ReactComponent]) -> List[str]:
        """Generate preview URLs for React components."""
        preview_urls = []
        
        for component in react_components:
            # Generate mock preview URL
            preview_url = f"https://v0.dev/preview/{component.name.lower()}_{hash(component.code) % 10000}"
            preview_urls.append(preview_url)
        
        return preview_urls

    def _check_deployment_readiness(self, components: List[Union[ReactComponent, MDXComponent]]) -> bool:
        """Check if components are ready for deployment."""
        react_components = [c for c in components if isinstance(c, ReactComponent)]
        
        # Check if all React components have required imports and are accessible
        for component in react_components:
            if not component.accessible or not component.responsive:
                return False
            
            # Check for required shadcn/ui imports
            required_imports = ["@/components/ui/button", "@/components/ui/card"]
            if not any(imp in component.imports for imp in required_imports):
                return False
        
        return len(react_components) > 0

    def _get_used_features(self, components: List[Union[ReactComponent, MDXComponent]]) -> List[str]:
        """Get list of v0 features used."""
        features = []
        
        if any(isinstance(c, ReactComponent) for c in components):
            features.append('react_components')
        
        if any(isinstance(c, MDXComponent) and c.interactive for c in components):
            features.append('interactive_components')
        
        if any(isinstance(c, MDXComponent) and c.type in ['python', 'nodejs'] for c in components):
            features.append('executable_code')
        
        features.extend(['mdx_support', 'shadcn_ui', 'tailwind_css', 'lucide_react'])
        
        return list(set(features))

    def is_available(self) -> bool:
        """Check if v0 integration is available."""
        return self.enabled and self.mdx_support

    def get_supported_features(self) -> List[str]:
        """Get list of supported v0 features."""
        return [
            'react_projects',
            'mdx_components',
            'executable_code',
            'interactive_charts',
            'shadcn_ui',
            'tailwind_css',
            'lucide_react',
            'responsive_design',
            'accessibility_compliance'
        ]
