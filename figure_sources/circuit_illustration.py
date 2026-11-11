#!/usr/bin/env python3
"""Reviewer-constructed Section 6.2 illustration; no primary-study evidence.

Run independently: python paper/figures/circuit_illustration.py --output-dir DIR
Only ideal Statevector evolution is used. No shots, noise model, or backend.
Edit STYLE for every visual parameter; circuits and verification are separate.
"""
import argparse
import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, state_fidelity

# Qiskit basis index = q0 + 2*q1; ket strings are |q1 q0>.
BASIS = ['00', '01', '10', '11']
ATOL = 1e-12
STYLE = dict(
    width=9.0, height=3.5, dpi=240, formats=['pdf', 'svg', 'png'],
    font_family='DejaVu Sans', font_size=12,
    state_size=12, probability_size=11, summary_size=11,
    ink='#17324d', gate_fill='#edf3f6', background='white',
    wire_width=1.4, gate_width=0.48, gate_height=0.44,
    control_radius=0.055, target_radius=0.12, gate_linewidth=1.3,
    column_start=0.85, column_step=0.90, wire_start=0.35, wire_end=3.0,
    row_positions=[1.0, 0.0], qubit_label_x=0.1,
    x_limits=[-0.1, 3.3], y_limits=[-0.4, 1.5],
    margins=dict(left=0.04, right=0.99, bottom=0.40, top=0.91, wspace=0.16),
    panel_labels=['A', 'B', 'C'], label_position=[0.0, 1.03],
    state_position=[0.50, -0.06], probability_position=[0.50, -0.30],
    ordering_label=r'Input: $|00\rangle$; basis strings: $|q_1q_0\rangle$; unlisted outcomes have probability zero.',
    ordering_position=[0.5, 0.025], label_size=14,
    summary_label=r'$P_A=P_C,\qquad \langle\psi_A|\psi_C\rangle=0$',
    summary_position=[0.5, 0.13],
    svg_hashsalt='qcc-reviewer-circuits',
)


def circuits():
    result = {}
    for name in ['A', 'B', 'C']:
        qc = QuantumCircuit(2, name=name)
        qc.h(0)
        qc.cx(1, 0) if name == 'B' else qc.cx(0, 1)
        if name == 'C':
            qc.z(0)
        result[name] = qc
    return result


def verify():
    expected = dict(A=np.array([1, 0, 0, 1])/np.sqrt(2),
                    B=np.array([1, 1, 0, 0])/np.sqrt(2),
                    C=np.array([1, 0, 0, -1])/np.sqrt(2))
    states = {name: Statevector.from_instruction(qc) for name, qc in circuits().items()}
    output = {}
    for name, sv in states.items():
        np.testing.assert_allclose(sv.data, expected[name], rtol=0, atol=ATOL)
        np.testing.assert_allclose(sv.probabilities(), np.abs(expected[name])**2, rtol=0, atol=ATOL)
        output[name] = dict(amplitudes=[[float(v.real), float(v.imag)] for v in sv.data],
                            probabilities=dict(zip(BASIS, map(float, sv.probabilities()))))
    for left, right, fidelity in [('A', 'B', .25), ('A', 'C', 0.), ('B', 'C', .25)]:
        assert not states[left].equiv(states[right]), 'Expected nonequivalence up to global phase'
        np.testing.assert_allclose(state_fidelity(states[left], states[right]), fidelity, rtol=0, atol=ATOL)
    np.testing.assert_allclose(states['A'].probabilities(), states['C'].probabilities(), rtol=0, atol=ATOL)
    return dict(status='PASS', epistemic_status='REVIEWER_CONSTRUCTED_ILLUSTRATION',
                initial_state='|00>', ordering='Basis index q0 + 2*q1; ket strings |q1 q0>',
                basis=BASIS, circuits=output,
                pairwise_fidelity={'A_B': .25, 'A_C': 0., 'B_C': .25},
                all_pairs_nonequivalent_up_to_global_phase=True,
                A_C_same_computational_basis_probabilities=True,
                tolerance=ATOL, primary_study_evidence=False)


def annotation_labels(report):
    """Derive compact exact labels from the verified amplitudes and probabilities.

    This illustration has exactly two real amplitudes of magnitude 1/sqrt(2).
    Reject any other state rather than attach a stale symbolic annotation.
    """
    labels = {}
    for name, values in report['circuits'].items():
        terms, outcomes = [], []
        for basis, (real, imag) in zip(report['basis'], values['amplitudes']):
            if abs(real) <= ATOL and abs(imag) <= ATOL:
                continue
            if abs(imag) > ATOL or not np.isclose(abs(real), 1/np.sqrt(2), rtol=0, atol=ATOL):
                raise ValueError('Annotation requires two real equal-magnitude amplitudes')
            sign = '-' if real < 0 else ('+' if terms else '')
            terms.append(sign + r'|' + basis + r'\rangle')
            if not np.isclose(values['probabilities'][basis], .5, rtol=0, atol=ATOL):
                raise ValueError('Annotation requires probability 1/2 for each displayed outcome')
            outcomes.append(f'P_{name}({basis})')
        if len(terms) != 2:
            raise ValueError('Annotation requires exactly two nonzero amplitudes')
        labels[name] = dict(state=r'$|\psi_' + name + r'\rangle=(' + ''.join(terms) + r')/\sqrt{2}$',
                            probabilities='$' + '='.join(outcomes) + r'=1/2$')
    return labels


def render(output_dir, style=None):
    # Diagrams are drawn directly from the verified Qiskit instruction objects.
    style = copy.deepcopy(STYLE if style is None else style)
    report = verify()
    labels = annotation_labels(report)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    plt.rcParams.update({'font.family': style['font_family'], 'font.size': style['font_size'],
                         'svg.hashsalt': style['svg_hashsalt'], 'svg.fonttype': 'none', 'pdf.fonttype': 42})
    fig, axes = plt.subplots(1, 3, figsize=(style['width'], style['height']))
    fig.patch.set_facecolor(style['background'])
    fig.subplots_adjust(**style['margins'])
    for ax, (name, qc), label in zip(axes, circuits().items(), style['panel_labels']):
        ax.set(xlim=style['x_limits'], ylim=style['y_limits'])
        ax.set_aspect('equal', adjustable='box')
        ax.axis('off')
        y = style['row_positions']
        for qubit in range(2):
            ax.plot([style['wire_start'], style['wire_end']], [y[qubit]]*2,
                    color=style['ink'], lw=style['wire_width'])
            ax.text(style['qubit_label_x'], y[qubit], f'$q_{qubit}$', va='center', ha='center', color=style['ink'])
        for column, instruction in enumerate(qc.data):
            x = style['column_start'] + style['column_step']*column
            indices = [qc.find_bit(q).index for q in instruction.qubits]
            if instruction.operation.name == 'cx':
                control, target = [y[q] for q in indices]
                ax.plot([x, x], [control, target], color=style['ink'], lw=style['gate_linewidth'])
                ax.add_patch(Circle((x, control), style['control_radius'], color=style['ink']))
                radius = style['target_radius']
                ax.add_patch(Circle((x, target), radius, facecolor=style['background'], edgecolor=style['ink'], lw=style['gate_linewidth'], zorder=3))
                ax.plot([x-radius, x+radius], [target, target], color=style['ink'], lw=style['gate_linewidth'], zorder=4)
                ax.plot([x, x], [target-radius, target+radius], color=style['ink'], lw=style['gate_linewidth'], zorder=4)
            else:
                assert instruction.operation.name in {'h', 'z'}
                yy = y[indices[0]]
                w, h = style['gate_width'], style['gate_height']
                ax.add_patch(Rectangle((x-w/2, yy-h/2), w, h, facecolor=style['gate_fill'], edgecolor=style['ink'], lw=style['gate_linewidth'], zorder=3))
                ax.text(x, yy, instruction.operation.name.upper(), ha='center', va='center', color=style['ink'], zorder=4)
        ax.text(*style['label_position'], label, transform=ax.transAxes, fontsize=style['label_size'], weight='bold', color=style['ink'])
        ax.text(*style['state_position'], labels[name]['state'], transform=ax.transAxes,
                fontsize=style['state_size'], ha='center', va='top', color=style['ink'])
        ax.text(*style['probability_position'], labels[name]['probabilities'], transform=ax.transAxes,
                fontsize=style['probability_size'], ha='center', va='top', color=style['ink'])
    fig.text(*style['summary_position'], style['summary_label'], ha='center',
             fontsize=style['summary_size'], color=style['ink'])
    fig.text(*style['ordering_position'], style['ordering_label'], ha='center', fontsize=style['probability_size'], color=style['ink'])
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for ext in style['formats']:
        assert ext in {'pdf', 'svg', 'png'}
        path = output_dir/f'circuit_illustration.{ext}'
        metadata = {'CreationDate': None, 'ModDate': None, 'Creator': 'QCC Python illustration'} if ext == 'pdf' else ({'Date': None, 'Creator': 'QCC Python illustration'} if ext == 'svg' else {'Software': 'QCC Python illustration'})
        fig.savefig(path, dpi=style['dpi'], metadata=metadata, facecolor=style['background'])
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    plt.close(fig)
    report.update(visualization_parameters=style, annotations=labels, output_sha256=hashes,
                  generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  versions={name: importlib.metadata.version(name) for name in ['qiskit', 'numpy', 'matplotlib']})
    (output_dir/'circuit_illustration.provenance.json').write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(render(args.output_dir), sort_keys=True))
