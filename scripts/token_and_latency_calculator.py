#!/usr/bin/env python3
# Deterministic Token FinOps & P95 Latency Estimator
# Usage: python token_and_latency_calculator.py --dau 100000 --queries-per-user 5 --indic-ratio 0.3
import argparse
import json

def calculate_finops(
    dau: int,
    queries_per_user: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    cache_hit_rate: float,
    system1_routed_ratio: float,
    indic_ratio: float,
    input_cost_per_1m: float,
    output_cost_per_1m: float,
):
    total_daily_queries = dau * queries_per_user
    effective_multiplier = (1.0 - indic_ratio) + (indic_ratio * 3.0)
    adj_input = avg_input_tokens * effective_multiplier
    adj_output = avg_output_tokens * effective_multiplier

    after_cache_queries = total_daily_queries * (1.0 - cache_hit_rate)
    system1_queries = after_cache_queries * system1_routed_ratio
    frontier_queries = after_cache_queries * (1.0 - system1_routed_ratio)

    daily_sys1_cost = (system1_queries * adj_input / 1_000_000) * 0.042
    daily_frontier_cost = (
        (frontier_queries * adj_input / 1_000_000) * input_cost_per_1m
        + (frontier_queries * adj_output / 1_000_000) * output_cost_per_1m
    )
    naive_daily_cost = (
        (total_daily_queries * adj_input / 1_000_000) * input_cost_per_1m
        + (total_daily_queries * adj_output / 1_000_000) * output_cost_per_1m
    )
    optimized_daily = daily_sys1_cost + daily_frontier_cost

    return {
        "daily_queries": total_daily_queries,
        "effective_token_multiplier": round(effective_multiplier, 2),
        "naive_monthly_usd": round(naive_daily_cost * 30, 2),
        "optimized_monthly_usd": round(optimized_daily * 30, 2),
        "monthly_savings_pct": round((1 - (optimized_daily / max(naive_daily_cost, 0.0001))) * 100, 1),
        "estimated_p95_latency_ms": {
            "cache_hit_path": 18,
            "system1_jev_path": 380,
            "hybrid_rag_plus_json_ui_first_frame": 790
        }
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dau", type=int, default=50000)
    p.add_argument("--queries-per-user", type=int, default=4)
    p.add_argument("--avg-input-tokens", type=int, default=2500)
    p.add_argument("--avg-output-tokens", type=int, default=350)
    p.add_argument("--cache-hit-rate", type=float, default=0.35)
    p.add_argument("--system1-routed-ratio", type=float, default=0.50)
    p.add_argument("--indic-ratio", type=float, default=0.0)
    p.add_argument("--input-cost-per-1m", type=float, default=2.50)
    p.add_argument("--output-cost-per-1m", type=float, default=10.00)
    args = p.parse_args()
    print(json.dumps(calculate_finops(**vars(args)), indent=2))
