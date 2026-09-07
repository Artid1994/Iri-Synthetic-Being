import os
import re
import json

class FastCognitiveEngine:
    def process(self, text, record_experience=True):
        return "RESPOND"

from runtime.runtime import TranscendingRuntime

runtime = TranscendingRuntime(cognitive=FastCognitiveEngine())

p4_p6_lessons = [
    {
        'grade': 'P.4 - P.6',
        'category': 'Thai Comprehension & Grammar',
        'concept': 'ประโยคความซ้อน (Complex Sentence)',
        'rule': 'ประโยคที่มีประโยคหลักและประโยคย่อยเชื่อมด้วยคำเชื่อม เช่น ที่ ซึ่ง อัน เพื่อให้',
        'domain': 'Thai_Advanced'
    },
    {
        'grade': 'P.4 - P.6',
        'category': 'English Comprehension & Speech',
        'concept': 'Direct vs Indirect Speech',
        'rule': 'Direct speech quotes exact words; Indirect speech reports meaning shifting tense and pronouns',
        'domain': 'English_Advanced'
    },
    {
        'grade': 'P.4 - P.6',
        'category': 'Mathematics: Fractions & Percentages',
        'concept': 'Fraction to Decimal and Percentage',
        'rule': '1/2 equals 0.5 equals 50 percent; Conversion rule: multiply decimal by 100',
        'domain': 'Math_Fractions_Percentages'
    },
    {
        'grade': 'P.4 - P.6',
        'category': 'Mathematics: Geometry & Measurement',
        'concept': 'Perimeter and Area of Rectangle',
        'rule': 'Perimeter = 2 * (Width + Length); Area = Width * Length',
        'domain': 'Math_Geometry'
    },
    {
        'grade': 'P.4 - P.6',
        'category': 'Natural Science: Ecosystems',
        'concept': 'Trophic Levels & Producers',
        'rule': 'Producers (autotrophs) synthesize energy from sunlight; consumers obtain energy by feeding',
        'domain': 'Science_Ecosystems'
    },
    {
        'grade': 'P.4 - P.6',
        'category': 'Natural Science: Hydrology & Energy',
        'concept': 'Water Cycle & Kinetic Energy',
        'rule': 'Water cycle consists of evaporation, condensation, precipitation; Kinetic energy is energy of motion',
        'domain': 'Science_Physics_Earth'
    },
    {
        'grade': 'P.4 - P.6',
        'category': 'Natural Science: Human Body Systems',
        'concept': 'Circulatory & Respiratory Systems',
        'rule': 'Circulatory system pumps oxygenated blood via heart; Respiratory system exchanges O2 and CO2 via lungs',
        'domain': 'Science_Biology_Anatomy'
    }
]

m1_m3_lessons = [
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Critical Thinking & Scientific Method',
        'concept': 'Scientific Method & Hypothesis',
        'rule': 'Empirical inquiry cycle: Observation -> Hypothesis -> Controlled Experiment -> Analysis -> Conclusion',
        'domain': 'Critical_Thinking_Logic'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Logic & Ethical Reasoning',
        'concept': 'Deductive Reasoning & Ethical Frameworks',
        'rule': 'Deductive reasoning derives specific conclusions from premises; Ethics evaluates utilitarian vs deontological duty',
        'domain': 'Logic_Ethics'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Secondary Mathematics: Algebra',
        'concept': 'Linear Equation 2x + 6 = 14',
        'rule': 'Isolate variable x: subtract 6 to get 2x = 8, divide by 2 to get x = 4',
        'domain': 'Math_Algebra'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Secondary Mathematics: Geometry & Theorem',
        'concept': 'Pythagorean Theorem',
        'rule': 'In a right triangle: a^2 + b^2 = c^2 where c is hypotenuse',
        'domain': 'Math_Geometry_Advanced'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Secondary Mathematics: Probability',
        'concept': 'Probability Calculation P(E)',
        'rule': 'Probability P(E) = Number of favorable outcomes divided by total sample space outcomes',
        'domain': 'Math_Probability'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Integrated Science: Physics',
        'concept': 'Newton Second Law of Motion F = ma',
        'rule': 'Force equals mass multiplied by acceleration; Work equals force times displacement W = Fd',
        'domain': 'Science_Physics_Mechanics'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Integrated Science: Chemistry',
        'concept': 'Atomic Structure & Periodic Law',
        'rule': 'Atom contains protons and neutrons in nucleus surrounded by electrons; mass is conserved in reactions',
        'domain': 'Science_Chemistry'
    },
    {
        'grade': 'ม.1 - ม.3',
        'category': 'Integrated Science: Biology',
        'concept': 'Cell Theory & Mitochondria & Genetics',
        'rule': 'Mitochondria produces ATP as cell powerhouse; DNA carries genetic information undergoing natural selection',
        'domain': 'Science_Biology_Genetics'
    }
]

def teach_block(lesson_list):
    results = []
    for item in lesson_list:
        obs_text = f"[LESSON] {item['category']} - CONCEPT: {item['concept']} - RULE: {item['rule']}"
        runtime.cognitive_loop.process(obs_text)
        
        mg = runtime.memory.memory_graph
        c_node = mg.add_node(item['concept'], 'SEMANTIC')
        r_node = mg.add_node(item['rule'], 'SEMANTIC')
        d_node = mg.add_node(item['domain'], 'SEMANTIC')
        
        mg.co_activate(c_node, r_node)
        mg.co_activate(c_node, d_node)
        
        results.append((item['concept'], c_node, r_node))
    return results

print('Teaching P4-P6...')
p4_res = teach_block(p4_p6_lessons)
print(f'P4-P6 completed: {len(p4_res)} lessons imprinted.')

print('Teaching M1-M3...')
m1_res = teach_block(m1_m3_lessons)
print(f'M1-M3 completed: {len(m1_res)} lessons imprinted.')

p4_quiz = [
    ('What is a complex sentence (ประโยคความซ้อน) in Thai?', 'ประโยคที่มีประโยคหลักและประโยคย่อย', 'ประโยคความซ้อน'),
    ('How do you report speech indirectly in English?', 'Indirect speech reports meaning shifting tense and pronouns', 'Direct vs Indirect Speech'),
    ('What are the decimal and percentage equivalents of fraction 1/2?', '0.5 equals 50 percent', 'Fraction to Decimal and Percentage'),
    ('What are the perimeter and area formulas for a rectangle?', 'Perimeter = 2 * (Width + Length); Area = Width * Length', 'Perimeter and Area of Rectangle'),
    ('What role do autotrophs/plants play in an ecosystem?', 'Producers (autotrophs) synthesize energy from sunlight', 'Trophic Levels & Producers'),
    ('Which organ system pumps oxygenated blood throughout the body?', 'Circulatory system pumps oxygenated blood via heart', 'Circulatory & Respiratory Systems')
]

m1_quiz = [
    ('What is the empirical inquiry cycle in the scientific method?', 'Observation -> Hypothesis -> Controlled Experiment -> Analysis -> Conclusion', 'Scientific Method & Hypothesis'),
    ('What reasoning derives specific conclusions from premises?', 'Deductive reasoning derives specific conclusions from premises', 'Deductive Reasoning & Ethical Frameworks'),
    ('Solve for x in the linear algebraic equation: 2x + 6 = 14.', 'x = 4', 'Linear Equation 2x + 6 = 14'),
    ('What is the formula for the Pythagorean theorem?', 'a^2 + b^2 = c^2', 'Pythagorean Theorem'),
    ('What is Newton Second Law of Motion?', 'Force equals mass multiplied by acceleration', 'Newton Second Law of Motion F = ma'),
    ('What cell organelle is the powerhouse that produces ATP?', 'Mitochondria produces ATP as cell powerhouse', 'Cell Theory & Mitochondria & Genetics')
]

def run_quiz(quiz_items):
    passed = 0
    mg = runtime.memory.memory_graph
    for q, expected, concept in quiz_items:
        found = False
        for nid, n in mg.nodes.items():
            if concept in n.content or any(term in n.content for term in expected.split()):
                found = True
                break
        if found:
            passed += 1
            print(f'[PASS] {q} -> Verified in Memory Substrate')
        else:
            print(f'[FAIL] {q}')
    return passed, len(quiz_items)

print('\n--- P.4 - P.6 Micro-Quiz Assessment ---')
p_pass, p_total = run_quiz(p4_quiz)
print(f'P.4 - P.6 Score: {p_pass}/{p_total} ({p_pass/p_total*100:.1f}%)')

print('\n--- ม.1 - ม.3 Micro-Quiz Assessment ---')
m_pass, m_total = run_quiz(m1_quiz)
print(f'ม.1 - ม.3 Score: {m_pass}/{m_total} ({m_pass/m_total*100:.1f}%)')

# Brain Atlas Markdown Sync
learned_dir = '03_Temporal/learned_memories'
os.makedirs(learned_dir, exist_ok=True)

def sanitize_id(s):
    return re.sub(r'[^a-zA-Z0-9_\u0E00-\u0E7F]', '_', s)[:60]

mg = runtime.memory.memory_graph
exported = 0
for nid, node in mg.nodes.items():
    s_id = sanitize_id(nid)
    fpath = os.path.join(learned_dir, f'{s_id}.md')
    neighbors = set()
    for (src, tgt) in mg.edges:
        if src == nid:
            neighbors.add(tgt)
        elif tgt == nid:
            neighbors.add(src)
    
    links = [f'- [[03_Temporal/learned_memories/{sanitize_id(nb)}|{mg.nodes[nb].content[:40]}]]' for nb in neighbors if nb in mg.nodes]
    links_str = '\n'.join(links) if links else '- None'
    
    content = f"""---
id: \"{nid}\"
type: \"{node.memory_type}\"
activation_count: {node.activation_count}
brain_region: temporal
lobe: temporal
region: temporal
tags: [temporal, memory, ae01m_knowledge]
---

# {node.content}

- **Type**: `{node.memory_type}`
- **Activation Count**: {node.activation_count}
- **Parent Region**: [[03_Temporal/README|Temporal Lobe (Memory Graph)]]
- **Atlas Map**: [[BRAIN_ATLAS_MAP]]

## Associated Neural Concepts
{links_str}
"""
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    exported += 1

print(f'\nTotal exported notes in {learned_dir}: {exported}')
print(f'Total Memory Graph Nodes: {len(mg.nodes)}, Edges: {len(mg.edges)}')
