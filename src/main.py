from MarkowitzClasses import MarkowitzOptimizer

if __name__ == "__main__":
    x = MarkowitzOptimizer(['AAPL', 'MSFT', "NVDA"])
    print(x.suggest_etfs())