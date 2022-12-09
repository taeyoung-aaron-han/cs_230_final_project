import rlcard
from rlcard.agents import NolimitholdemHumanAgent as HumanAgent
from rlcard.utils import print_card, load_model, get_device
# Make environment
env = rlcard.make('no-limit-holdem')
device = get_device()
human_agent = HumanAgent(env.num_actions)
filepath = 'experiments/nolimit_holdem_dqn_basic/model.pth'
self_learn_agent = load_model(filepath, env = env, position = 1, device = device)

env.set_agents([human_agent, human_agent])


while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action
    final_state = trajectories[0][-1]
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    _action_list = []
    for i in range(1, len(action_record)+1):
        if action_record[-i][0] == state['current_player']:
            break
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses', pair[1])

    # Let's take a look at what the agent card is
    print('===============     Cards all Players    ===============')
    for hands in env.get_perfect_information()['hand_cards']:
        print_card(hands)
    
    if 'public_card' in env.get_perfect_information():
        print('\n=============== Community Card ===============')
        print_card(env.get_perfect_information()['public_card'])

    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win {} chips!'.format(payoffs[0]))
    elif payoffs[0] == 0:
        print('It is a tie.')
    else:
        print('You lose {} chips!'.format(-payoffs[0]))
    print('')

    input("Press any key to continue...")