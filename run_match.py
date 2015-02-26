from kuhn3p import betting, deck, dealer, players
from random import Random

rng         = Random()
rng.seed(31337)  # each seed corresponds to a different set of hands

num_hands   = 3000
the_players = [players.Chump(0.99, 0.01, 0.0), 
    players.Chump(0.99, 0.01, 0.0), 
    players.Bluffer(0.2) ]

total = [0, 0, 0]

log = open('round.log','w');
log.write("#hand\tfirst_player\tterminal_state_num\tterminal_state_string\n");
for hand in range(num_hands):
	first          = hand % 3
	second         = (first + 1) % 3
	third          = (second + 1) % 3

	this_players   = [the_players[first], the_players[second], the_players[third]]

	(state, delta) = dealer.play_hand(this_players, deck.shuffled(rng))
	for i in range(3):
		total[(first + i)%3] += delta[i]

        # writing results of hand to log
        log.write("\t".join([str(hand), str(first), str(state), str(betting.to_string(state))]))
        log.write("\n")
        

for i in range(3):
	print the_players[i], total[i]
