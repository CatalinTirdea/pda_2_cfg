import sys
def load_cfg_file(cfg_file):
    productions = {} 
    with open(cfg_file, 'r') as f: 
        for line in f:
            left, right = line.split('->') # Împărțim linia în două părți: partea stângă și partea dreaptă a producției, separate prin simbolul ':'
            productions[left.strip()] = [r.strip() for r in right.split('|')] # Adăugăm producția în dicționarul noastru, cu partea stângă drept cheie și lista de simboluri din partea dreaptă drept valoare
    
    return productions

def is_valid_cfg(cfg):
    # Verificăm dacă simbolul de start este definit în CFG
    
    valid = True
    start_symbol = next(iter(cfg))
    if start_symbol != 'S': # Dacă simbolul de start nu este 'S', CFG-ul nu este valid
        
        return False

    # Verificăm dacă toate simbolurile neterminale folosite în producții sunt definite în CFG
    for nonterminal, rules in cfg.items():
        
        for rule in rules:
                
                for key in cfg.keys():
                    if key  in rule or "epsilon" in rule: 
                      valid = True
                      break
                    
        if valid == False:
          for nonterminal, rules in cfg.items():
            for rule in rules:
                for symbol in rule:
                  if symbol.isupper() and symbol not in cfg:
                     return False # Dacă un simbol neterminal nu este definit în CFG, CFG-ul nu este valid  
    return True


cfg=load_cfg_file(sys.argv[1])
print(is_valid_cfg(cfg))
