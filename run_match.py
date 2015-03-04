from kuhn3p import betting, deck, dealer, players
from random import Random

# to index
# actor to player order
def apo(actor, first): return ( actor + first ) % 3

rng         = Random()
rng.seed(31337)  # each seed corresponds to a different set of hands

num_hands   = 3000
the_players = [players.Chump(0.99, 0.01, 0.0),
               players.bluff_advanced(),
               players.Bluffer(0.2) ]

total = [0, 0, 0]

log = open('round.log','w');
log.write("## Definition of player names\n" +
          "ID\t0\t" + the_players[0].__class__.__name__ + "\n"
          "ID\t1\t" + the_players[1].__class__.__name__ + "\n"
          "ID\t2\t" + the_players[2].__class__.__name__ + "\n"
		  "## For delta and card numbers starting player is 0 (i.e. delta_0 and card_0)" + "\n"
)

log.write("#hand\tfirst_player_ID\tterminal_state_num\tterminal_state_string" +
		  "\tdelta_0\tdelta_1\tdelta_2" +
		  "\twinning_player_ID\tcard_0\tcard_1\tcard_2\tcard_burned" +
		  "\twallet_0\twallet_1\twallet_2" +
		  "\n");
for hand in range(num_hands):
	first          = hand % 3
	second         = (first + 1) % 3
	third          = (second + 1) % 3
	actor_order    = [first, second, third]

	this_players   = [the_players[first], the_players[second], the_players[third]]

	cards = deck.shuffled(rng)
	(state, delta) = dealer.play_hand(this_players, cards)
	for i in range(3):
		total[(first + i)%3] += delta[i]

	# writing results of hand to log
	log.write("\t".join([str(hand), str(first), str(state), str(betting.to_string(state)),
						 "\t".join(map(str, [ delta[apo(i, first)] for i in actor_order ])),
						 str(apo(dealer.winner(state, cards), first)),
						 "\t".join( map(str, map(deck.card_to_string,
												 [ cards[i] for i in [apo(first,first), apo(second,first), apo(third,first), 3] ]
										 ))),
						 "\t".join(map(str, total))
				 ]))
	log.write("\n")
        

for i in range(3):
	print the_players[i], total[i]
