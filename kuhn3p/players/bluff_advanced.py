import random
from kuhn3p import betting, deck, Player

class bluff_advanced(Player):
	def __init__(self, rng=random.Random()):
		self.bluff = 0.25
		self.rng   = rng

                # this is where I'll keep my estimates of other players' bluff ratios
                self.otherBluff = [0,0]

        # let's do something right when we get the hand
        # why not calculate the probability of winning if nobody folds!
        def start_hand(self, position, card):
                if card == 4:
                        self.base_prob_win = 1.0;
                elif card == 3:
                        self.base_prob_win = 1.0/3;
                elif card < 3:
                        self.base_prob_win = 0.0;

	def act(self, state, card):

                # stay in game with probability according to base prob
                stay_in_game = False
                if self.rng.random() < self.base_prob_win:
                        stay_in_game = True
                        
                if betting.can_bet(state):
                        if stay_in_game:
                                return betting.BET
                        else:
                                return betting.CHECK
		else:
			if stay_in_game:
				return betting.CALL
			else:
				return betting.FOLD

        # let's see if we can estimate other players' bluffing rate
        # for now, let's just identify a bluffer by someone who raised and did not have an ace
	def end_hand(self, position, card, state, shown_cards):

                # nobody raised
                if state == 12: return
                
                raiser = betting.bettor(state)
                
                # if we raised, then do nothing
                if raiser == position: return

                # check to make sure there actually was a showdown
                if betting.is_showdown(state) is False:
                        return

                assert shown_cards[raiser] is not None
                
                # check card of raiser is not an ace
                if shown_cards[raiser] != deck.ACE:
                        bluff = 1
                else:
                        bluff = 0
                        
                # figure out which one of the two players was the raiser
                if position == 0:
                        if raiser == 1:
                                raiser_rel_pos = 0
                        else:
                                raiser_rel_pos = 1
                elif position == 1:
                        if raiser == 2:
                                raiser_rel_pos = 0
                        else:
                                raiser_rel_pos = 1
                else:
                        raiser_rel_pos = raiser
                
                # now just average with weight previous bluff
                # estimate with current bluff result
                self.otherBluff[raiser_rel_pos] = (9 * self.otherBluff[raiser_rel_pos] + bluff) / 10.0
                
                        
	def __str__(self):
		return 'Bluffer(bluff=%f,p1.bluff=%f,p2.bluff=%f)' % (self.bluff,self.otherBluff[0],self.otherBluff[1])
