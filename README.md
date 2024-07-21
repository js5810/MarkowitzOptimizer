# MarkowitzOptimizer

## Theory of the Model and Simplifications
Just like any financial model, Markowitz's meam-variance analysis invovles simplifications and assumptions that allow us to mathematically analyze different portfolios. The assumptions are:

- Historical variance is used as a proxy for risk
- Dividends are negligible

## Limitations:
The above assumptions introduce some clear limitations of this program:
- Mean-variance analysis assumes returns are normally distributed and fails to capture any skewness which is almost always present in real life
- Using only historical data to approximate the population variance which is itself a proxy for risk can be an oversimplification since one-off events that deeply impact prices are not considered

## Citations:
The randomized user agents file `user-agents.txt` is taken from the pyetfdb_scraper repository.