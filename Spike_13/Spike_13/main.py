"""
Created by Kieran Bates

This is the main class for Spike_13
"""

from world import World
from agent import Agent
from planner import Planner
from action import Action


def create_actions(path):
    """creates a list of actions from contents of file"""
    # read contents of file
    actions_file = open(path, "r")
    print(actions_file.name)
    lines = actions_file.readlines()
    actions_file.close()

    # convert each line into an Action putting them in the actions list
    actions = []
    for line in lines:
        line = line.replace("\n", "")
        # print(line)
        split = line.split(",")
        name = split[0]
        time_taken = int(split[1])
        priority = int(split[2])
        repeatable = split[3] == "True"
        description = split[4]
        needs = []
        split_needs = split[5].split(":")
        for need in split_needs:
            if need != "":
                needs.append(need)
        modifiers = []
        split_modifiers = split[6].split(":")
        for modifier in split_modifiers:
            # if "\n" in modifier:
                # modifier = modifier.replace("\n", "")
            if modifier != "":
                modifiers.append(float(modifier))

        actions.append(Action(name, time_taken, priority, repeatable, description, needs, modifiers))

    return actions


if __name__ == '__main__':
    plan_actions = create_actions("./actions/actions.txt")

    # search for the agents starter action, Wake Up, and remove it
    # from the planners actions
    agent_action = None
    for action in plan_actions:
        if action.name == "Start":
            agent_action = action
            break

    assert agent_action is not None, "Start action not in file"

    planner = Planner(plan_actions)
    agent = Agent(planner, agent_action)
    planner.agent = agent
    world = World(agent)
    play = True

    world.render()

    while play:
        # game loop
        while world.play:
            world.update()
            world.render()

        if agent.alive:
            play_again = input("Play again? [Y/N]")

            play_again = play_again.capitalize()
            if play_again == "N":
                play = False
            else:
                world = World(agent, world.current_time)
        else:
            play = False

    if not agent.alive:
        death = []

        for need in agent.needs:
            if need.value == 0 and need.zero_time == 15:
                death.append(need.name)

        out = "\n----------------------------------------\n"
        out += "The agent died from: "
        for i in range(len(death)):
            out += death[i] + ", "
        print(out)

    print("Final Needs:")
    for need in agent.needs:
        print("\t" + need.name + ": " + str(need.value))

    world.to_file()

    print(">> Done! <<")
