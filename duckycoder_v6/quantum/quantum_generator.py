"""
DuckyCoder v6 Quantum Computing Support
Experimental quantum algorithm generation and circuit visualization using Qiskit.
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Quantum computing imports
try:
    import qiskit
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit.algorithms import Grover, VQE, QAOA
    from qiskit.circuit.library import QFT
    from qiskit.visualization import circuit_drawer
    HAS_QISKIT = True
except ImportError:
    HAS_QISKIT = False

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


@dataclass
class QuantumAlgorithm:
    """Represents a quantum algorithm."""
    name: str
    description: str
    circuit: Optional[Any]  # QuantumCircuit
    code: str
    qubits_required: int
    classical_bits: int
    complexity: str  # low, medium, high
    use_cases: List[str]
    metadata: Dict[str, Any]


@dataclass
class QuantumGenerationResult:
    """Result of quantum algorithm generation."""
    algorithms: List[QuantumAlgorithm]
    visualizations: List[str]
    code_snippets: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]


class QuantumCodeGenerator:
    """Quantum algorithm generator and circuit visualizer."""

    # Quantum algorithm templates
    ALGORITHM_TEMPLATES = {
        'basic_circuit': {
            'description': 'Basic quantum circuit with Hadamard and CNOT gates',
            'complexity': 'low',
            'qubits': 2,
            'use_cases': ['quantum_entanglement', 'superposition_demo']
        },
        'grover_search': {
            'description': 'Grover search algorithm for unstructured search',
            'complexity': 'medium',
            'qubits': 3,
            'use_cases': ['database_search', 'optimization']
        },
        'quantum_fourier_transform': {
            'description': 'Quantum Fourier Transform for period finding',
            'complexity': 'high',
            'qubits': 4,
            'use_cases': ['period_finding', 'phase_estimation']
        },
        'variational_quantum_eigensolver': {
            'description': 'VQE for finding ground state energies',
            'complexity': 'high',
            'qubits': 4,
            'use_cases': ['chemistry', 'optimization']
        },
        'quantum_approximate_optimization': {
            'description': 'QAOA for combinatorial optimization',
            'complexity': 'high',
            'qubits': 4,
            'use_cases': ['max_cut', 'traveling_salesman']
        },
        'bell_state': {
            'description': 'Bell state creation for quantum entanglement',
            'complexity': 'low',
            'qubits': 2,
            'use_cases': ['quantum_communication', 'teleportation']
        },
        'deutsch_jozsa': {
            'description': 'Deutsch-Jozsa algorithm for function evaluation',
            'complexity': 'medium',
            'qubits': 3,
            'use_cases': ['oracle_problems', 'quantum_advantage_demo']
        }
    }

    def __init__(self, config: Dict[str, Any]):
        """Initialize the quantum code generator."""
        self.config = config
        self.quantum_config = config.get('quantum_computing', {})
        self.logger = logging.getLogger(__name__)

        # Quantum settings
        self.enabled = self.quantum_config.get('enabled', False)
        self.framework = self.quantum_config.get('framework', 'qiskit')
        self.max_qubits = self.quantum_config.get('simulation', {}).get('max_qubits', 20)
        self.shots = self.quantum_config.get('simulation', {}).get('shots', 1024)

        if not HAS_QISKIT and self.enabled:
            self.logger.warning("Qiskit not available - quantum features disabled")
            self.enabled = False

    async def generate_quantum_algorithms(self, content: str, 
                                        language: Optional[str] = None) -> QuantumGenerationResult:
        """
        Generate quantum algorithms based on content analysis.

        Args:
            content: Source code content to analyze
            language: Programming language (must be Python for quantum)

        Returns:
            QuantumGenerationResult with generated algorithms
        """
        if not self.enabled or not HAS_QISKIT:
            return QuantumGenerationResult(
                algorithms=[],
                visualizations=[],
                code_snippets=[],
                recommendations=["Quantum computing features are disabled or Qiskit is not available"],
                metadata={'error': 'Quantum features unavailable'}
            )

        if language != 'python':
            return QuantumGenerationResult(
                algorithms=[],
                visualizations=[],
                code_snippets=[],
                recommendations=["Quantum algorithms are currently only supported for Python"],
                metadata={'unsupported_language': language}
            )

        try:
            self.logger.info("Generating quantum algorithms")

            # Analyze content for quantum patterns
            quantum_patterns = await self._analyze_quantum_patterns(content)
            
            # Generate appropriate algorithms
            algorithms = []
            visualizations = []
            code_snippets = []
            recommendations = []

            # Generate basic algorithms if no specific patterns found
            if not quantum_patterns:
                basic_algorithm = await self._generate_basic_circuit()
                algorithms.append(basic_algorithm)
                code_snippets.append(basic_algorithm.code)
                recommendations.append("Consider exploring quantum computing for optimization problems")
            else:
                # Generate algorithms based on detected patterns
                for pattern in quantum_patterns:
                    if pattern in self.ALGORITHM_TEMPLATES:
                        algorithm = await self._generate_algorithm_from_template(pattern)
                        if algorithm:
                            algorithms.append(algorithm)
                            code_snippets.append(algorithm.code)

            # Generate visualizations
            for algorithm in algorithms:
                if algorithm.circuit:
                    viz = await self._generate_circuit_visualization(algorithm.circuit, algorithm.name)
                    if viz:
                        visualizations.append(viz)

            # Add general recommendations
            recommendations.extend(await self._generate_quantum_recommendations(content))

            return QuantumGenerationResult(
                algorithms=algorithms,
                visualizations=visualizations,
                code_snippets=code_snippets,
                recommendations=recommendations,
                metadata={
                    'quantum_patterns_detected': quantum_patterns,
                    'total_algorithms_generated': len(algorithms),
                    'framework': self.framework,
                    'generated_at': datetime.now().isoformat()
                }
            )

        except Exception as e:
            self.logger.error(f"Quantum algorithm generation failed: {e}")
            return QuantumGenerationResult(
                algorithms=[],
                visualizations=[],
                code_snippets=[],
                recommendations=[],
                metadata={'error': str(e)}
            )

    async def _analyze_quantum_patterns(self, content: str) -> List[str]:
        """Analyze content for quantum computing patterns."""
        patterns_found = []
        content_lower = content.lower()

        # Pattern detection
        quantum_indicators = {
            'optimization': ['minimize', 'maximize', 'optimization', 'cost function', 'objective'],
            'search': ['search', 'find', 'lookup', 'query', 'database'],
            'machine_learning': ['neural', 'learning', 'training', 'model', 'classification'],
            'cryptography': ['encrypt', 'decrypt', 'hash', 'security', 'cryptography'],
            'simulation': ['simulate', 'model', 'physics', 'chemistry', 'molecular'],
            'linear_algebra': ['matrix', 'vector', 'eigenvalue', 'linear algebra', 'decomposition']
        }

        for pattern_type, keywords in quantum_indicators.items():
            if any(keyword in content_lower for keyword in keywords):
                # Map to quantum algorithms
                if pattern_type == 'optimization':
                    patterns_found.append('quantum_approximate_optimization')
                elif pattern_type == 'search':
                    patterns_found.append('grover_search')
                elif pattern_type in ['machine_learning', 'simulation']:
                    patterns_found.append('variational_quantum_eigensolver')
                elif pattern_type in ['cryptography', 'linear_algebra']:
                    patterns_found.append('quantum_fourier_transform')

        # Check for specific quantum mentions
        quantum_keywords = ['quantum', 'qubit', 'superposition', 'entanglement', 'interference']
        if any(keyword in content_lower for keyword in quantum_keywords):
            patterns_found.append('basic_circuit')
            patterns_found.append('bell_state')

        return list(set(patterns_found))  # Remove duplicates

    async def _generate_basic_circuit(self) -> QuantumAlgorithm:
        """Generate a basic quantum circuit demonstration."""
        if not HAS_QISKIT:
            raise ImportError("Qiskit is required for quantum circuit generation")

        # Create basic circuit
        qreg = QuantumRegister(2, 'q')
        creg = ClassicalRegister(2, 'c')
        circuit = QuantumCircuit(qreg, creg)

        # Add gates
        circuit.h(qreg[0])  # Hadamard gate
        circuit.cx(qreg[0], qreg[1])  # CNOT gate
        circuit.measure(qreg, creg)  # Measure

        # Generate code
        code = '''"""
Basic Quantum Circuit with Superposition and Entanglement
Generated by DuckyCoder v6 Quantum Module
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.visualization import plot_histogram

def create_basic_quantum_circuit():
    """Create a basic quantum circuit demonstrating superposition and entanglement."""
    
    # Create quantum and classical registers
    qreg = QuantumRegister(2, 'q')
    creg = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(qreg, creg)
    
    # Apply Hadamard gate to create superposition
    circuit.h(qreg[0])
    
    # Apply CNOT gate to create entanglement
    circuit.cx(qreg[0], qreg[1])
    
    # Measure the qubits
    circuit.measure(qreg, creg)
    
    return circuit

def run_quantum_circuit():
    """Execute the quantum circuit and return results."""
    circuit = create_basic_quantum_circuit()
    
    # Use Qiskit Aer simulator
    backend = Aer.get_backend('qasm_simulator')
    
    # Execute circuit
    job = execute(circuit, backend, shots=1024)
    result = job.result()
    counts = result.get_counts(circuit)
    
    print("Measurement results:")
    for outcome, count in counts.items():
        probability = count / 1024
        print(f"  |{outcome}⟩: {count} times ({probability:.1%})")
    
    return counts

if __name__ == "__main__":
    run_quantum_circuit()
'''

        return QuantumAlgorithm(
            name="Basic Quantum Circuit",
            description="Demonstrates quantum superposition and entanglement",
            circuit=circuit,
            code=code,
            qubits_required=2,
            classical_bits=2,
            complexity="low",
            use_cases=["quantum_education", "entanglement_demo", "superposition_demo"],
            metadata={
                "gates_used": ["H", "CNOT", "Measure"],
                "quantum_concepts": ["superposition", "entanglement", "measurement"]
            }
        )

    async def _generate_algorithm_from_template(self, template_name: str) -> Optional[QuantumAlgorithm]:
        """Generate quantum algorithm from template."""
        if template_name not in self.ALGORITHM_TEMPLATES:
            return None

        template = self.ALGORITHM_TEMPLATES[template_name]

        try:
            if template_name == 'grover_search':
                return await self._generate_grover_algorithm()
            elif template_name == 'quantum_fourier_transform':
                return await self._generate_qft_algorithm()
            elif template_name == 'bell_state':
                return await self._generate_bell_state()
            elif template_name == 'deutsch_jozsa':
                return await self._generate_deutsch_jozsa()
            else:
                # Generate basic template
                return await self._generate_basic_circuit()

        except Exception as e:
            self.logger.error(f"Failed to generate {template_name}: {e}")
            return None

    async def _generate_grover_algorithm(self) -> QuantumAlgorithm:
        """Generate Grover's search algorithm."""
        num_qubits = 3
        qreg = QuantumRegister(num_qubits, 'q')
        creg = ClassicalRegister(num_qubits, 'c')
        circuit = QuantumCircuit(qreg, creg)

        # Initialize superposition
        for i in range(num_qubits):
            circuit.h(qreg[i])

        # Oracle (mark |101⟩)
        circuit.cz(qreg[0], qreg[2])
        circuit.cz(qreg[1], qreg[2])

        # Diffusion operator
        for i in range(num_qubits):
            circuit.h(qreg[i])
            circuit.x(qreg[i])
        
        circuit.h(qreg[2])
        circuit.ccx(qreg[0], qreg[1], qreg[2])
        circuit.h(qreg[2])
        
        for i in range(num_qubits):
            circuit.x(qreg[i])
            circuit.h(qreg[i])

        circuit.measure(qreg, creg)

        code = '''"""
Grover's Search Algorithm
Quantum search algorithm with quadratic speedup
Generated by DuckyCoder v6 Quantum Module
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
import math

def grovers_algorithm(n_qubits: int, marked_item: str):
    """
    Implement Grover's search algorithm.
    
    Args:
        n_qubits: Number of qubits (determines search space size)
        marked_item: Binary string representing the marked item
    
    Returns:
        QuantumCircuit implementing Grover's algorithm
    """
    qreg = QuantumRegister(n_qubits, 'q')
    creg = ClassicalRegister(n_qubits, 'c')
    circuit = QuantumCircuit(qreg, creg)
    
    # Step 1: Initialize superposition
    for i in range(n_qubits):
        circuit.h(qreg[i])
    
    # Step 2: Calculate optimal number of iterations
    N = 2**n_qubits
    optimal_iterations = int(math.pi * math.sqrt(N) / 4)
    
    for iteration in range(optimal_iterations):
        # Oracle: mark the target item
        oracle(circuit, qreg, marked_item)
        
        # Diffusion operator (amplitude amplification)
        diffusion_operator(circuit, qreg)
    
    # Step 3: Measure
    circuit.measure(qreg, creg)
    
    return circuit

def oracle(circuit, qreg, marked_item):
    """Oracle that marks the target item by flipping its amplitude."""
    # Example oracle for |101⟩
    if marked_item == "101":
        circuit.cz(qreg[0], qreg[2])
        circuit.cz(qreg[1], qreg[2])

def diffusion_operator(circuit, qreg):
    """Diffusion operator for amplitude amplification."""
    n_qubits = len(qreg)
    
    # Apply Hadamard gates
    for i in range(n_qubits):
        circuit.h(qreg[i])
    
    # Apply X gates
    for i in range(n_qubits):
        circuit.x(qreg[i])
    
    # Multi-controlled Z gate
    if n_qubits == 3:
        circuit.h(qreg[2])
        circuit.ccx(qreg[0], qreg[1], qreg[2])
        circuit.h(qreg[2])
    
    # Apply X gates again
    for i in range(n_qubits):
        circuit.x(qreg[i])
    
    # Apply Hadamard gates again
    for i in range(n_qubits):
        circuit.h(qreg[i])

def run_grovers_search():
    """Execute Grover's algorithm."""
    circuit = grovers_algorithm(3, "101")
    
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1024)
    result = job.result()
    counts = result.get_counts(circuit)
    
    print("Grover's search results:")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for outcome, count in sorted_counts:
        probability = count / 1024
        print(f"  |{outcome}⟩: {count} times ({probability:.1%})")
    
    return counts

if __name__ == "__main__":
    run_grovers_search()
'''

        return QuantumAlgorithm(
            name="Grover's Search Algorithm",
            description="Quantum search algorithm with quadratic speedup over classical search",
            circuit=circuit,
            code=code,
            qubits_required=num_qubits,
            classical_bits=num_qubits,
            complexity="medium",
            use_cases=["database_search", "optimization", "unstructured_search"],
            metadata={
                "time_complexity": "O(√N)",
                "quantum_advantage": "quadratic_speedup",
                "gates_used": ["H", "CZ", "CCX", "Measure"]
            }
        )

    async def _generate_qft_algorithm(self) -> QuantumAlgorithm:
        """Generate Quantum Fourier Transform algorithm."""
        num_qubits = 4
        qreg = QuantumRegister(num_qubits, 'q')
        creg = ClassicalRegister(num_qubits, 'c')
        circuit = QuantumCircuit(qreg, creg)

        # Apply QFT
        qft = QFT(num_qubits)
        circuit.append(qft, qreg)
        circuit.measure(qreg, creg)

        code = '''"""
Quantum Fourier Transform (QFT)
Quantum version of the discrete Fourier transform
Generated by DuckyCoder v6 Quantum Module
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.circuit.library import QFT
import numpy as np

def quantum_fourier_transform(n_qubits: int):
    """
    Implement Quantum Fourier Transform.
    
    Args:
        n_qubits: Number of qubits for the QFT
    
    Returns:
        QuantumCircuit implementing QFT
    """
    qreg = QuantumRegister(n_qubits, 'q')
    creg = ClassicalRegister(n_qubits, 'c')
    circuit = QuantumCircuit(qreg, creg)
    
    # Apply QFT using Qiskit's built-in implementation
    qft = QFT(n_qubits)
    circuit.append(qft, qreg)
    
    # Measure
    circuit.measure(qreg, creg)
    
    return circuit

def manual_qft(circuit, qreg):
    """Manual implementation of QFT for educational purposes."""
    n = len(qreg)
    
    for i in range(n):
        # Apply Hadamard gate
        circuit.h(qreg[i])
        
        # Apply controlled rotation gates
        for j in range(i + 1, n):
            angle = 2 * np.pi / (2**(j - i + 1))
            circuit.cp(angle, qreg[j], qreg[i])
    
    # Swap qubits to reverse the order
    for i in range(n // 2):
        circuit.swap(qreg[i], qreg[n - 1 - i])

def prepare_input_state(circuit, qreg, state_vector):
    """Prepare an input state for QFT demonstration."""
    # Example: prepare |1010⟩ state
    circuit.x(qreg[1])
    circuit.x(qreg[3])

def run_qft_demo():
    """Demonstrate Quantum Fourier Transform."""
    n_qubits = 4
    qreg = QuantumRegister(n_qubits, 'q')
    creg = ClassicalRegister(n_qubits, 'c')
    circuit = QuantumCircuit(qreg, creg)
    
    # Prepare input state
    prepare_input_state(circuit, qreg, "|1010⟩")
    
    # Apply QFT
    manual_qft(circuit, qreg)
    
    # Measure
    circuit.measure(qreg, creg)
    
    # Execute
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1024)
    result = job.result()
    counts = result.get_counts(circuit)
    
    print("QFT results:")
    for outcome, count in counts.items():
        probability = count / 1024
        print(f"  |{outcome}⟩: {count} times ({probability:.1%})")
    
    return counts

if __name__ == "__main__":
    run_qft_demo()
'''

        return QuantumAlgorithm(
            name="Quantum Fourier Transform",
            description="Quantum version of the discrete Fourier transform",
            circuit=circuit,
            code=code,
            qubits_required=num_qubits,
            classical_bits=num_qubits,
            complexity="high",
            use_cases=["period_finding", "phase_estimation", "shor_algorithm"],
            metadata={
                "time_complexity": "O(n²)",
                "classical_equivalent": "Fast Fourier Transform O(n log n)",
                "gates_used": ["H", "CP", "SWAP", "Measure"]
            }
        )

    async def _generate_bell_state(self) -> QuantumAlgorithm:
        """Generate Bell state (maximally entangled state)."""
        qreg = QuantumRegister(2, 'q')
        creg = ClassicalRegister(2, 'c')
        circuit = QuantumCircuit(qreg, creg)

        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
        circuit.measure(qreg, creg)

        code = '''"""
Bell State Generation
Create maximally entangled quantum states
Generated by DuckyCoder v6 Quantum Module
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer
from qiskit.visualization import plot_histogram

def create_bell_state(bell_type: str = "phi_plus"):
    """
    Create one of the four Bell states.
    
    Args:
        bell_type: Type of Bell state ('phi_plus', 'phi_minus', 'psi_plus', 'psi_minus')
    
    Returns:
        QuantumCircuit creating the specified Bell state
    """
    qreg = QuantumRegister(2, 'q')
    creg = ClassicalRegister(2, 'c')
    circuit = QuantumCircuit(qreg, creg)
    
    if bell_type == "phi_plus":
        # |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
        
    elif bell_type == "phi_minus":
        # |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
        circuit.x(qreg[1])
        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
        
    elif bell_type == "psi_plus":
        # |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
        circuit.h(qreg[0])
        circuit.x(qreg[1])
        circuit.cx(qreg[0], qreg[1])
        
    elif bell_type == "psi_minus":
        # |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
        circuit.x(qreg[0])
        circuit.x(qreg[1])
        circuit.h(qreg[0])
        circuit.cx(qreg[0], qreg[1])
    
    circuit.measure(qreg, creg)
    return circuit

def demonstrate_entanglement():
    """Demonstrate quantum entanglement with Bell states."""
    bell_states = ["phi_plus", "phi_minus", "psi_plus", "psi_minus"]
    backend = Aer.get_backend('qasm_simulator')
    
    for bell_type in bell_states:
        print(f"\\nBell state: {bell_type}")
        circuit = create_bell_state(bell_type)
        
        job = execute(circuit, backend, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        
        for outcome, count in counts.items():
            probability = count / 1024
            print(f"  |{outcome}⟩: {count} times ({probability:.1%})")

def test_bell_inequality():
    """Test Bell's inequality to demonstrate quantum non-locality."""
    # This is a simplified demonstration
    print("Bell's inequality test demonstrates quantum non-locality")
    print("Classical physics: |E(a,b) - E(a,c)| ≤ 1 + E(b,c)")
    print("Quantum mechanics can violate this inequality!")
    
    # Create Bell state for testing
    circuit = create_bell_state("phi_plus")
    
    # In a full implementation, you would measure in different bases
    # and calculate correlation functions E(a,b), E(a,c), E(b,c)
    
    return circuit

if __name__ == "__main__":
    demonstrate_entanglement()
    test_bell_inequality()
'''

        return QuantumAlgorithm(
            name="Bell State Generation",
            description="Create maximally entangled quantum states for quantum communication",
            circuit=circuit,
            code=code,
            qubits_required=2,
            classical_bits=2,
            complexity="low",
            use_cases=["quantum_communication", "quantum_teleportation", "quantum_cryptography"],
            metadata={
                "entanglement": "maximal",
                "bell_states": ["phi_plus", "phi_minus", "psi_plus", "psi_minus"],
                "applications": ["quantum_key_distribution", "quantum_teleportation"]
            }
        )

    async def _generate_deutsch_jozsa(self) -> QuantumAlgorithm:
        """Generate Deutsch-Jozsa algorithm."""
        num_qubits = 3
        qreg = QuantumRegister(num_qubits, 'q')
        creg = ClassicalRegister(num_qubits - 1, 'c')  # Don't measure ancilla
        circuit = QuantumCircuit(qreg, creg)

        # Initialize
        for i in range(num_qubits - 1):
            circuit.h(qreg[i])
        circuit.x(qreg[num_qubits - 1])
        circuit.h(qreg[num_qubits - 1])

        # Oracle (constant function example)
        # For balanced function, add oracle gates here

        # Final Hadamards
        for i in range(num_qubits - 1):
            circuit.h(qreg[i])

        circuit.measure(qreg[:num_qubits - 1], creg)

        code = '''"""
Deutsch-Jozsa Algorithm
Determine if a function is constant or balanced with one query
Generated by DuckyCoder v6 Quantum Module
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, execute, Aer

def deutsch_jozsa_algorithm(n_qubits: int, oracle_type: str = "constant"):
    """
    Implement Deutsch-Jozsa algorithm.
    
    Args:
        n_qubits: Number of input qubits
        oracle_type: Type of oracle ("constant" or "balanced")
    
    Returns:
        QuantumCircuit implementing Deutsch-Jozsa algorithm
    """
    # Total qubits: n input qubits + 1 ancilla qubit
    total_qubits = n_qubits + 1
    qreg = QuantumRegister(total_qubits, 'q')
    creg = ClassicalRegister(n_qubits, 'c')  # Only measure input qubits
    circuit = QuantumCircuit(qreg, creg)
    
    # Step 1: Initialize input qubits in superposition
    for i in range(n_qubits):
        circuit.h(qreg[i])
    
    # Step 2: Initialize ancilla qubit in |1⟩ state
    circuit.x(qreg[n_qubits])
    circuit.h(qreg[n_qubits])
    
    # Step 3: Apply oracle
    apply_oracle(circuit, qreg, oracle_type, n_qubits)
    
    # Step 4: Apply Hadamard gates to input qubits
    for i in range(n_qubits):
        circuit.h(qreg[i])
    
    # Step 5: Measure input qubits
    circuit.measure(qreg[:n_qubits], creg)
    
    return circuit

def apply_oracle(circuit, qreg, oracle_type, n_qubits):
    """Apply oracle function to the circuit."""
    ancilla = qreg[n_qubits]
    
    if oracle_type == "constant_0":
        # f(x) = 0 for all x (do nothing)
        pass
        
    elif oracle_type == "constant_1":
        # f(x) = 1 for all x (flip ancilla)
        circuit.x(ancilla)
        
    elif oracle_type == "balanced":
        # Example balanced function: f(x) = x₀ ⊕ x₁ ⊕ ... ⊕ xₙ₋₁
        for i in range(n_qubits):
            circuit.cx(qreg[i], ancilla)
    
    else:
        raise ValueError(f"Unknown oracle type: {oracle_type}")

def run_deutsch_jozsa():
    """Demonstrate Deutsch-Jozsa algorithm."""
    n_input_qubits = 2
    oracle_types = ["constant_0", "constant_1", "balanced"]
    backend = Aer.get_backend('qasm_simulator')
    
    for oracle_type in oracle_types:
        print(f"\\nTesting {oracle_type} oracle:")
        circuit = deutsch_jozsa_algorithm(n_input_qubits, oracle_type)
        
        job = execute(circuit, backend, shots=1024)
        result = job.result()
        counts = result.get_counts(circuit)
        
        # Interpret results
        if "00" in counts and len(counts) == 1:
            print("  Result: CONSTANT function")
        else:
            print("  Result: BALANCED function")
        
        for outcome, count in counts.items():
            probability = count / 1024
            print(f"    |{outcome}⟩: {count} times ({probability:.1%})")

def quantum_advantage_explanation():
    """Explain the quantum advantage of Deutsch-Jozsa algorithm."""
    print("""
    QUANTUM ADVANTAGE:
    
    Classical approach:
    - For n-bit function, need to evaluate f(x) for 2^(n-1) + 1 inputs
      in worst case to determine if constant or balanced
    
    Quantum approach:
    - Only need ONE query to the oracle!
    - Exponential speedup for this specific problem
    
    Result interpretation:
    - If measurement gives |00...0⟩: function is CONSTANT
    - If measurement gives anything else: function is BALANCED
    """)

if __name__ == "__main__":
    quantum_advantage_explanation()
    run_deutsch_jozsa()
'''

        return QuantumAlgorithm(
            name="Deutsch-Jozsa Algorithm",
            description="Determine if a function is constant or balanced with quantum advantage",
            circuit=circuit,
            code=code,
            qubits_required=num_qubits,
            classical_bits=num_qubits - 1,
            complexity="medium",
            use_cases=["oracle_problems", "quantum_advantage_demo", "function_evaluation"],
            metadata={
                "quantum_advantage": "exponential",
                "oracle_queries": 1,
                "classical_queries": "2^(n-1) + 1 worst case",
                "problem_type": "promise_problem"
            }
        )

    async def _generate_circuit_visualization(self, circuit: Any, name: str) -> Optional[str]:
        """Generate circuit visualization."""
        if not HAS_MATPLOTLIB:
            return f"Circuit visualization for {name} (matplotlib required for visual output)"

        try:
            # Generate text-based circuit diagram
            circuit_str = str(circuit.draw(output='text'))
            
            visualization = f"""
## {name} Circuit Diagram

```
{circuit_str}
```

**Circuit Properties:**
- Qubits: {circuit.num_qubits}
- Classical bits: {circuit.num_clbits}
- Depth: {circuit.depth()}
- Gate count: {len(circuit.data)}
"""
            return visualization

        except Exception as e:
            self.logger.warning(f"Circuit visualization failed: {e}")
            return f"Circuit visualization for {name} (generation failed: {e})"

    async def _generate_quantum_recommendations(self, content: str) -> List[str]:
        """Generate quantum computing recommendations based on content."""
        recommendations = []
        content_lower = content.lower()

        # Analyze content for quantum applicability
        if 'optimization' in content_lower:
            recommendations.append(
                "Consider using Quantum Approximate Optimization Algorithm (QAOA) "
                "for combinatorial optimization problems"
            )

        if any(keyword in content_lower for keyword in ['search', 'database', 'lookup']):
            recommendations.append(
                "Grover's algorithm could provide quadratic speedup for unstructured search problems"
            )

        if any(keyword in content_lower for keyword in ['simulation', 'chemistry', 'physics']):
            recommendations.append(
                "Quantum simulation using Variational Quantum Eigensolver (VQE) "
                "could be beneficial for molecular or physical system modeling"
            )

        if any(keyword in content_lower for keyword in ['machine learning', 'ml', 'ai']):
            recommendations.append(
                "Explore Quantum Machine Learning algorithms like Quantum Neural Networks "
                "or Variational Quantum Classifiers"
            )

        if any(keyword in content_lower for keyword in ['crypto', 'security', 'encrypt']):
            recommendations.append(
                "Quantum key distribution and quantum cryptography protocols "
                "could enhance security applications"
            )

        # General recommendations
        if not recommendations:
            recommendations.extend([
                "Quantum computing could provide advantages for specific computational problems",
                "Consider quantum algorithms for optimization, search, and simulation tasks",
                "Explore quantum machine learning for AI applications"
            ])

        # Add educational recommendations
        recommendations.extend([
            "Start with basic quantum circuits to understand superposition and entanglement",
            "Use quantum simulators for development before accessing quantum hardware",
            "Consider hybrid classical-quantum algorithms for near-term applications"
        ])

        return recommendations

    def is_available(self) -> bool:
        """Check if quantum computing features are available."""
        return self.enabled and HAS_QISKIT

    def get_supported_algorithms(self) -> List[str]:
        """Get list of supported quantum algorithms."""
        return list(self.ALGORITHM_TEMPLATES.keys())

    def get_algorithm_info(self, algorithm_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific algorithm."""
        return self.ALGORITHM_TEMPLATES.get(algorithm_name)
