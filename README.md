# MarkowitzOptimizer

## Problem Description
Given a user's stock portfolio, our goal is to recommend a few ETFs to add to the portfolio to help boost return while keeping risk minimal. The unique constraint of our problem is that we are adding onto an existing portfolio instead of building one from scratch. Thus, we modify the classic mean-variance model to tailor it to our needs.

## Modified Markowitz's Mean-Variance Model and Assumptions
Just like any financial model, Markowitz's meam-variance analysis invovles simplifications and assumptions that allow us to mathematically analyze different portfolios. The assumptions of the model are:

- Historical variance is used as a proxy for risk
- Returns are distributed normally

In our modification we further assume:
- The user wants to keep the stocks they currently own and our goal is to suggest ETFs to add along with optimal share sizes
- The improved portfolio will consist of 70% stocks and 30% ETFs
- Dividends are negligible
- The user has a moderate risk appetite and can choose their own return-risk pair after being given a list of options

With these assumptions, we model the problem as follows. Let $X$ be a continuous random variable for the return of a portfolio containing $n$ total assets. Furthermore, let $X_{i}$ be random variables for the return of the $i\text{th}$ asset in the portfolio for $1 \leq i \leq n$. We then have

$$\displaystyle{X=\sum_{i=1}^{n}w_{i}X_{i}}$$

where $w_i$ is the weight of the $i\text{th}$ asset. Note that $w_{i}$ can have negative value (indicating being short the asset) as long as $w_1 + w_2 + \cdots + w_n = 1$. So far, this is identical to the usual setup of mean-variance analysis. We now introduce our twist which is that the last $s$ assets are stocks already in the portfolio with fixed weights that we won't change. So, we only have control over $w_1, \cdots, w_{n-s}$ which are weights for how many of each ETF to go long or short. Keeping this in mind, the linearity of expectation and expanding the variance of a sum of random variables in terms of pairwise covariances gives us

$$\displaystyle{E(X)=\sum_{i=1}^{n}w_{i}E(X_{i}) \ \ \ \ and \ \ \ \ Var(X)=\sum_{i=1}^{n}w_{i}^2 Var(X_{i}) + 2\sum_{i < j}w_{i}w_{j}Cov(X_{i}, X_{j})}$$

We can rewrite the two quantities in terms of the $\color{red}\textbf{part we can optimize}$ and the $\color{blue}\textbf{constant part}$

$$\displaystyle{E(X)={\color{red}\sum_{i=1}^{n-s}w_{i}E(X_{i})} + {\color{blue}\sum_{i=n-s+1}^{n}w_{i}E(X_{i})} }$$ 

$$\displaystyle{Var(X)={\color{red}\sum_{i=1}^{n-s}w_{i}^2 Var(X_{i})} + {\color{red}2\cdot \Bigg( \sum_{i < j \leq n-s}w_{i}w_{j}Cov(X_{i}, X_{j}) \Bigg) + 2\cdot \Bigg( \sum_{i \leq n-s \text{ and } j > n-s}w_{i}w_{j}Cov(X_{i}, X_{j}) \Bigg) } + {\color{blue}\sum_{i=n-s+1}^{n}w_{i}^2 Var(X_{i}) + 2\cdot \Bigg( \sum_{n-s < i < j}w_{i}w_{j}Cov(X_{i}, X_{j}) \Bigg) } }$$

So our goal is to find the optimal values of $w_{1}, \cdots, w_{n-s}$ that sum to $\frac{3}{7}(w_{n-s+1}+\cdots+w_{n})$ which is a constant since the weights for stocks are predetermined. The $\frac{3}{7}$ ratio ensures that the final portfolio will have 30% of holdings in ETFs.

Since we do not know the population mean, variance, and covariance of the $X_{i}$'s, we use sampled values obtained from data provided on `yahoo finance` and `etfdb` to approximate the expected return and portfolio variance. We do this by taking $k$ samples of historical monthly returns for each asset. Let the monthly returns for asset $i$ be $\[x_{1}^{(i)}, x_{2}^{(i)}, \cdots, x_{k}^{(i)}\]$. Then, the sample metrics to approximate $E(X_i)$, $Var(X_i)$, and $Cov(X_i, X_j)$ are respectively:

$$\overline{x^{(i)}}=\frac{x_{1}^{(i)}+\cdots+x_{k}^{(i)}}{k}, \ \ \ \ {s^{(i)}}^2 = \frac{1}{k-1}\cdot \sum_{a=1}^{k} (x_{a}^{(i)} - \overline{x^{(i)}} )^2, \ \ \ \ {s^{ij}}^2=\frac{1}{k-1} \cdot \sum_{a=1}^{k}(r_{a}^{(i)} - \overline{r^{(i)}}) (r_{a}^{(j)} - \overline{r^{(j)}})$$

Substituting these quantities above, we now have an optimization problem where we need to find the best $\[w_1, w_2, \cdots, w_n\]$ that minimizes variance given a fixed expected return. This can be done using Lagrange multipliers.

## Limitations:
The assumptions of our model introduce some clear limitations:
- Mean-variance analysis assumes returns are normally distributed and fails to capture any skewness which is almost always present in real life
- Using only historical data to approximate the population variance which is itself a proxy for risk can be an oversimplification since one-off events that deeply impact prices are not considered

## Future Work:
One way to improve the model is to experiment with different proportions of stocks and ETFs. We fixed this to be 7 to 3 here but we could also parametrize the ratio itself to further optimize the problem. This would introduce some additional constraints but would still be solvable from a mathematical perspective. Another improvement we could make is to assume that returns are distributed log normal instead of being normal. This accounts for skew which provides a more accurate picture of real life price movements.

## Citations:
The randomized user agents file `user-agents.txt` is taken from the pyetfdb_scraper repository.
