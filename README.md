Penneys Game

Penney's Game is a game played with coins, where two players each select a series of 3 Heads or Tails, such as 'Heads Tails Heads' or 'Tails Tails Heads', and flip a coin until one of the two sequences shows up first. This is a fun way to trick your friends, because after Player 1 makes their selection, there is a statistically best option for Player 2 to select to give themselves the best odds of winning.
The Humble-Nishiyama Game is a variation with playing cards, where each player selects a sequence of 3 red or black cards (suits and numbers don't matter), and see which comes up first.
There are two variations to score this game. The first uses 'tricks', or based on number of times each players sequence appears in a deck. When a players sequence comes up, they get one point, and then the deck is dealt until all cards are gone. Whoever recieved more 'tricks', or whose sequence appeared more times in that deck, wins. The other version uses card counts, so that when a players sequence appears, they collect all the cards since the start or the last sequence appeared. The game continues until all the cards are dealt, and players add up their cards, and whoever collected the most wins.

Our Investigation

The purpose of this project was to determine the statistically best selection for the second player based on the first players choice for each way of scoring. Interestingly, the odds for each variation are slightly different, and for some selections the ideal choice is different for scoring with tricks or cards.

How to run our code

To run our code, simply call the main.py file, and an input will appear asking the user how many more decks they want to simulate. Simply type in a number and press enter. Then, that many decks will be simulated in batches of maximum 1000, where every new 1000 decks uses a different random seed. Those decks will used to siumulate games for both strategies, and the results will be added to a database where heatmaps, one for each strategy, will be made based on data from all total simulated games, including the old games already scored and the new ones just added. The heatmaps will show the odds of Player 2 winning with each of the 8 possible sequences based on each of the 8 possible sequences chosen by player one. The odds of a tie will also be dispalyed in parentheses next to the odds of winning.

Findings

Through our millions of decks of simulated cards, we have found the ideal selections for Player 2 for both strategies. For the tricks strategy, the best odds are, if Player 1s sequence is 1-2-3, Player 2 should select (Not 2)-1-2. For the tricks strategy, this gives Player 2 the best chance of winning. Interestingly for the Cards Strategy, while that strategy often gives a good chance of winning, the best strategy for Player 1 selecting BRB is RRB, and for RBR its BBR. The best odds are still select the first two colors chosen by player 1 and put a different color at the beginning, so you catch the beginning of any potentially winning sequence for them, but with a slight variation for these two instances.