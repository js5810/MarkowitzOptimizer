from MarkowitzClasses import MarkowitzOptimizer

if __name__ == "__main__":
    x = MarkowitzOptimizer([('AAPL', 2), ('MSFT', 5), ("NVDA", 1)])
    print(x.suggest_etfs())