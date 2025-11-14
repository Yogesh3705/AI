from itertools import product
import re

# Function to extract all unique propositional symbols from sentences
def extract_symbols(sentences):
    symbols = set()
    for sentence in sentences:
        symbols.update(re.findall(r'\b[A-Z]\b', sentence))
    return symbols

# Function to evaluate a sentence under a given model
def pl_true(sentence, model):
    # Replace symbols in sentence with their truth values
    expr = sentence
    for symbol, value in model.items():
        expr = expr.replace(symbol, str(value))
    try:
        # Evaluate the boolean expression
        return eval(expr)
    except Exception as e:
        raise ValueError(f"Error evaluating sentence '{sentence}' with model {model}: {e}")

# Truth Table Enumeration Algorithm
def tt_entails(KB, alpha):
    # Step 1: Collect all propositional symbols
    symbols = list(extract_symbols(KB | {alpha}))
    
    # Step 2: Generate all possible truth value combinations
    for values in product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        
        # Step 3: Evaluate KB and alpha in the current model
        kb_true = all(pl_true(sentence, model) for sentence in KB)
        alpha_true = pl_true(alpha, model)
        
        # Step 3b: If KB is True but alpha is False, entailment fails
        if kb_true and not alpha_true:
            return False
    
    # Step 4: No counterexample found, KB entails alpha
    return True

# Example usage:
if __name__ == "__main__":
    # Define Knowledge Base (KB) and Query (alpha)
    KB = {"A and B"}        # Example KB
    alpha = "A"             # Query α
    
    result = tt_entails(KB, alpha)
    print(f"KB entails alpha? {result}")
