"""
SEIR.

Models based on simple SEIR.
Susceptible, Exposed, Infected, Removed.

(c) Copyright Aleksander J. Dubas, 2020.
"""
import matplotlib.pyplot as plt
from random import random


def stochastic(rate):
    """Calculate integer change."""
    change = int(rate)
    remainder = rate - change
    if random() < remainder:
        change += 1
    return change


class SEIRD():
    """Classic SEIRD model with discrete population."""

    def __init__(self, population,
                 beta=0.33, gamma=0.2, sigma=0.11, mort=0.01):
        """Initalise model."""
        self.N = population
        self.S = [self.N - 1]
        self.E = [0]
        self.I = [1]
        self.R = [0]
        self.D = [0]
        self.beta = beta
        self.gamma = gamma
        self.sigma = sigma
        self.mort = mort

    def advance_day(self):
        """Advance one day in the model."""
        dS = -stochastic(self.beta*self.I[-1]*self.S[-1]/float(self.N))
        dE = -dS - stochastic(self.gamma*self.E[-1])
        dI = -dE - dS - stochastic(self.sigma*self.I[-1])
        dR = -dI - dE - dS
        dD = stochastic(self.mort*dR)
        dR = dR - dD
        self.S.append(self.S[-1] + dS)
        self.E.append(self.E[-1] + dE)
        self.I.append(self.I[-1] + dI)
        self.R.append(self.R[-1] + dR)
        self.D.append(self.D[-1] + dD)
        # checksum
        assert (self.S[-1] + self.E[-1] + self.I[-1] +
                self.R[-1] + self.D[-1] == self.N)
        return

    def run_model(self):
        """Run the model until there are no Exposed or Infected."""
        while (self.I[-1] + self.E[-1] > 0):
            self.advance_day()
        return


def plot_model(model):
    """Run a model and plot the results."""
    model.run_model()
    print("Number dead: {}".format(model.D[-1]))
    days = range(len(model.S))
    plt.plot(days, model.S, label="Susceptible")
    plt.plot(days, model.E, label="Exposed")
    plt.plot(days, model.I, label="Infected")
    plt.plot(days, model.R, label="Recovered")
    plt.plot(days, model.D, label="Dead")
    plt.xlabel("Time [days]")
    plt.ylabel("People")
    plt.legend()
    plt.show()
