#!/usr/bin/env python


import time
import matplotlib.pyplot as plt


class ForwardChecking:
    def __init__(self, knowledge, rules):
        """
        This constructor takes knowledge and rules as arguments
        This will create a forward checking object
        knowledge is supposed to be the aromic streings
        rules is supposed to be tuples of the premises and the conclusions
        """
        self.initial_knowledge = set(knowledge)
        self.rules = rules


    def entails(self, query):
        """
        This function takes query as an argument
        This function will take a query and see if its in the knowledge and rules and trace it
        This function returns the boolean value if the query is in the facts and the trace for the query
        """
        knowledge = set(self.initial_knowledge)
        trace = []
        old_count = -1
        inference_steps = 0

        while old_count != len(knowledge):
            old_count = len(knowledge)
            changed = False
            
            for premises, conclusion in self.rules:
                inference_steps += 1
                if all(premise in knowledge for premise in premises):
                    if conclusion not in knowledge:
                        knowledge.add(conclusion)
                        trace.append(f"Derived {conclusion} from {premises}")
                        changed = True
            if not changed:
                break
        return query in knowledge, trace, inference_steps


def scaling_experiement(num_k, knowledge, rules, query):
    """
    This function takes the number of k unrelated knwledge to add
    This cuntion returns the results of the experiment
    """
    results = []

    for k in range(0, num_k + 1):
        knowledge_k, rules_k = add_neutral_rules(knowledge, rules, k)

        fc = ForwardChecking(knowledge_k, rules_k)

        start = time.perf_counter()
        result, trace, steps = fc.entails(query)
        end = time.perf_counter()

        runtime = end - start
        results.append((k, runtime, steps, len(rules_k), result))
    return results


def add_neutral_rules(knowledge, rules, k):
    """
    This function takes 3 arguments
    knowledge is neutral facts to add
    rules is the rule set 
    k is the number of neutral rules to add
    """
    new_knowledge = set(knowledge)
    new_rules = list(rules)

    for i in range(k):
        start_fact = f"Start_{i}"
        new_knowledge.add(start_fact)
        new_rules.append(({start_fact}, f"Step1_{i}"))
        new_rules.append(({f"Step1_{i}"}, f"Step2_{i}")) 
        new_rules.append(({f"Step2_{i}"}, f"Step3_{i}"))
        new_rules.append(({f"Step3_{i}"}, f"Final_{i}"))

    return new_knowledge, new_rules


def plot_results(results):
    """
    This function takes one argument
    results are the metrics taken from the experiments
    This funciton will plot the runtime differentces between k values
    This fucnti9o nwill plot the inference step differences between k values
    This function doesnt return anything
    """
    title = "Forward Chaining Runtime Scaling"
    k_values = [r[0] for r in results]
    runtimes = [r[1] for r in results]
    steps = [r[2] for r in results]
    
    plt.figure(figsize=(10, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(k_values, runtimes, 'bo-', linewidth=2, markersize=6)
    plt.xlabel('Number of Neutral Rules (k)')
    plt.ylabel('Runtime (seconds)')
    plt.title(f'{title} - Runtime vs k')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(k_values, steps, 'ro-', linewidth=2, markersize=6)
    plt.xlabel('Number of Neutral Rules (k)')
    plt.ylabel('Number of Inference Steps')
    plt.title(f'{title} - Inference Steps vs k')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def main():
    knowledge = {"P"}
    rules = [
        ({"P"}, "Q"),
        ({"Q"}, "R"),
        ({"R"}, "S"),
        ({"S"}, "T"),
    ]
    query = "T"
    ks = [5, 10, 15]

    for num in ks:
        results = scaling_experiement(num, knowledge, rules, query)

        print(f"For k up to {num} neutral rules:")
        for (k, runtime, steps, total_rules, result) in results:
            print(f"k={k:2d}")
            print(f"Runtime: {runtime:.8f}")
            print(f"Steps: {steps}")
            print(f"Total Rules: {total_rules}")
            print(f"Result: {result}")
            print()
        print()
        print()
        plot_results(results)


if __name__ == '__main__':
    main()