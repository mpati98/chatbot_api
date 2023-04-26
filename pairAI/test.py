from core.agents import create_agent_from_model_file

def Model_init():
    # import model from the model file can be pretrained or fine tuned

    blender_agent = create_agent_from_model_file(
        "zoo:blender/blender_90M/model")
    return blender_agent

blender_agent = Model_init()
text_to_sys = input("Say somthing: ")
blender_agent.observe({'text': text_to_sys, 'episode_done': False})
response = blender_agent.act()  # From bot
print(response['text'])