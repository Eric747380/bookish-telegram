#!/usr/bin/env python3
"""
Dataset Generator for Frequent Itemset Mining (Part 1.2)
 
KEY INSIGHT FOR FLAT 10-50% REGION:
- Most items should be either >50% freq OR <10% freq
- Very few items in the 10-50% range
- This keeps frequent itemset count stable across 10-50% supports
"""
 
import random
import sys
from typing import List

MAX_TXN_SIZE = 25


def generate_transactions(
    universal_itemset: List[str],
    num_transactions: int
) -> List[List[str]]:
    random.seed(42)
    
    items = list(universal_itemset)
    n_items = len(items)
    
    # KEY: Create a BIMODAL distribution
    # - Many items with >50% frequency (frequent at 50%, 25%, 10%)
    # - Very few items with 10-50% frequency (the gap creates flatness)
    # - Many items with <10% frequency (only frequent at 5%)
    
    # Tier sizes - BIMODAL distribution
    ultra_high_size = max(int(n_items * 0.08), 5)    # 8% - >90% support
    high_size = max(int(n_items * 0.30), 25)         # 30% - 50-90% support (LARGE!)
    gap_size = max(int(n_items * 0.05), 3)           # 5% - 10-50% support (SMALL GAP!)
    critical_size = max(int(n_items * 0.40), 30)     # 40% - 5-10% support
    rare_size = n_items - ultra_high_size - high_size - gap_size - critical_size  # <5%
    
    ultra_high_items = items[:ultra_high_size]
    high_items = items[ultra_high_size:ultra_high_size + high_size]
    gap_items = items[ultra_high_size + high_size:ultra_high_size + high_size + gap_size]
    critical_items = items[ultra_high_size + high_size + gap_size:
                          ultra_high_size + high_size + gap_size + critical_size]
    rare_items = items[ultra_high_size + high_size + gap_size + critical_size:]
    
    # Frequency targets - BIMODAL
    freq_profile = {
        "ultra_high": 0.93,   # >90% support
        "high": 0.65,         # 50-90% support (ABOVE 50%!)
        "gap": 0.22,          # 10-50% support (FEW ITEMS HERE)
        "critical": 0.08,     # 5-10% support (MANY ITEMS)
        "rare": 0.02          # <5% support
    }
    
    # Create correlated groups for low-support items
    # This causes the explosion at 5% for Apriori
    critical_groups = [critical_items[i:i+3] for i in range(0, len(critical_items), 3)]
    
    transactions = []
    
    for _ in range(num_transactions):
        txn = set()
        
        # Ultra-high frequency items (>90%)
        for item in ultra_high_items:
            if random.random() < freq_profile["ultra_high"]:
                txn.add(item)
        
        # High frequency items (50-90%) - THE STABLE BASE
        # These items are frequent at 50%, 25%, AND 10% support
        for item in high_items:
            if random.random() < freq_profile["high"]:
                txn.add(item)
        
        # Gap items (10-50%) - VERY FEW
        # These are the only ones that become frequent between 10-50%
        for item in gap_items:
            if random.random() < freq_profile["gap"]:
                txn.add(item)
        
        # Critical items (5-10%) - THE EXPLOSION ZONE
        # These only become frequent at 5%, causing the sharp increase
        for group in critical_groups:
            if random.random() < freq_profile["critical"]:
                # High correlation creates large itemsets at 5%
                for item in group:
                    if random.random() < 0.75:
                        txn.add(item)
        
        # Rare items (<5%)
        for item in rare_items:
            if random.random() < freq_profile["rare"]:
                txn.add(item)
        
        # Ensure non-empty
        if not txn:
            txn.add(random.choice(ultra_high_items))
        
        # Cap transaction size
        if len(txn) > MAX_TXN_SIZE:
            txn = set(random.sample(sorted(txn), MAX_TXN_SIZE))
        
        transactions.append(sorted(txn))
    
    return transactions


def write_transactions_to_file(transactions: List[List[str]], filename: str):
    with open(filename, 'w') as f:
        for transaction in transactions:
            f.write(' '.join(transaction) + '\n')


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generate_dataset.py '<item1 item2 ...>' <num_transactions>")
        print("Example: python3 generate_dataset.py '1 2 3 ... 200' 15000")
        sys.exit(1)
    
    universal_itemset_str = sys.argv[1]
    num_transactions = int(sys.argv[2])
    universal_itemset = universal_itemset_str.split()
    
    print(f"Generating {num_transactions} transactions from {len(universal_itemset)} items...")
    
    transactions = generate_transactions(universal_itemset, num_transactions)
    
    output_file = "generated_transactions.dat"
    write_transactions_to_file(transactions, output_file)
    
    print(f"Dataset generated successfully: {output_file}")
    print(f"Total transactions: {len(transactions)}")
    print(f"Average transaction length: {sum(len(t) for t in transactions) / len(transactions):.2f}")
    
    # Statistics
    item_frequencies = {}
    for transaction in transactions:
        for item in transaction:
            item_frequencies[item] = item_frequencies.get(item, 0) + 1
    
    sorted_items = sorted(item_frequencies.items(), key=lambda x: x[1], reverse=True)
    
    # Count items in different support ranges
    support_90_plus = sum(1 for _, freq in sorted_items if freq/num_transactions >= 0.90)
    support_50_plus = sum(1 for _, freq in sorted_items if freq/num_transactions >= 0.50)
    support_25_plus = sum(1 for _, freq in sorted_items if freq/num_transactions >= 0.25)
    support_10_plus = sum(1 for _, freq in sorted_items if freq/num_transactions >= 0.10)
    support_5_plus = sum(1 for _, freq in sorted_items if freq/num_transactions >= 0.05)
    
    print(f"\nItems by support threshold:")
    print(f"  >= 90%: {support_90_plus} items")
    print(f"  >= 50%: {support_50_plus} items")
    print(f"  >= 25%: {support_25_plus} items")
    print(f"  >= 10%: {support_10_plus} items")
    print(f"  >=  5%: {support_5_plus} items")
    
    # KEY DIAGNOSTIC: Check the gaps
    gap_10_to_25 = support_25_plus - support_50_plus
    gap_25_to_50 = support_50_plus - support_90_plus
    gap_5_to_10 = support_10_plus - support_25_plus
    
    print(f"\nCRITICAL - Items added at each threshold:")
    print(f"  50% → 25%: +{gap_25_to_50} items (should be SMALL for flatness)")
    print(f"  25% → 10%: +{gap_5_to_10} items (should be SMALL for flatness)")
    print(f"  10% → 5%: +{support_5_plus - support_10_plus} items (should be LARGE for spike)")
    
    print(f"\nExpected behavior:")
    print(f"  If gap_25_to_50 and gap_5_to_10 are small → FLAT 10-50% region ✓")
    print(f"  If gap at 5% is large → SHARP increase at 5% ✓")


if __name__ == "__main__":
    main()
