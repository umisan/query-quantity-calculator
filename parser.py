import re
from typing import List, Tuple, Set


class DatalogParser:
    def __init__(self):
        self.pattern = re.compile(r'^([A-Za-z][A-Za-z0-9_]*)\s*\(\s*([^)]+)\s*\)$')
    
    def parse_query(self, query_text: str) -> List[Tuple[str, List[str]]]:
        relations = []
        for line in query_text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            match = self.pattern.match(line)
            if not match:
                raise ValueError(f"Invalid relation format: {line}")
            
            relation_name = match.group(1)
            args_str = match.group(2)
            args = [arg.strip() for arg in args_str.split(',')]
            
            relations.append((relation_name, args))
        
        return relations
    
    def get_all_variables(self, relations: List[Tuple[str, List[str]]]) -> Set[str]:
        variables = set()
        for _, args in relations:
            variables.update(args)
        return variables