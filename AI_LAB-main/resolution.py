# --- Resolution Theorem Prover (Propositional Logic) ---

import itertools

def negate_literal(lit):
    return lit[1:] if lit.startswith('~') else '~' + lit

def parse_clause(clause_str):
    # Split a clause like "A v ~B" into {'A', '~B'}
    return set(x.strip() for x in clause_str.split('v'))

def clause_to_str(clause):
    if not clause:
        return "EMPTY"
    return " v ".join(sorted(clause))

def resolve(clause1, clause2):
    resolvents = []
    for lit in clause1:
        if negate_literal(lit) in clause2:
            new_clause = (clause1 - {lit}) | (clause2 - {negate_literal(lit)})
            # Remove complementary literals like A and ~A in same clause (tautology)
            if any(negate_literal(x) in new_clause for x in new_clause):
                continue
            resolvents.append(new_clause)
    return resolvents

def resolution_proof(premises, conclusion):
    print("=== Resolution Proof ===")
    print("Premises:")
    for p in premises:
        print("  ", p)
    print("Conclusion to prove:", conclusion)

    # Convert all premises and ¬S into CNF clauses
    clauses = [parse_clause(p) for p in premises]
    negated_conclusion = negate_literal(conclusion)
    clauses.append({negated_conclusion})

    print("\nInitial Clauses (including negated conclusion):")
    for c in clauses:
        print("  ", clause_to_str(c))

    new = set()
    step = 0

    while True:
        step += 1
        pairs = list(itertools.combinations(clauses, 2))
        print(f"\n--- Iteration {step} ---")
        generated_this_round = 0

        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            for resolvent in resolvents:
                print(f"Resolved ({clause_to_str(ci)}) and ({clause_to_str(cj)}) → {clause_to_str(resolvent)}")

                if not resolvent:
                    print("\n✅ Derived EMPTY CLAUSE → Contradiction found. The conclusion is TRUE.")
                    return True
                if resolvent not in clauses and resolvent not in new:
                    new.add(frozenset(resolvent))
                    generated_this_round += 1

        if not new:
            print("\n❌ No new clauses. The conclusion CANNOT be proven from the premises.")
            return False

        for c in new:
            clauses.append(set(c))

        print(f"Added {generated_this_round} new clauses.")

# --- Example Usage ---

premises = [
    "P v Q",
    "~P v R",
    "~Q",
    "~R"
]
conclusion = "False"  # Want to test if 'False' follows (unsatisfiable set)

resolution_proof(premises, "R")
