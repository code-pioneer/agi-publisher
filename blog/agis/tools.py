from blog.agis import create_blog, proof_reading_blog, revise_blog, publish_blog_html, publish_blog_md, save_to_file, generate_filename_extension

def agent_tools():
    tools = []
    tools.append(create_blog.setup())
    tools.append(proof_reading_blog.setup()) 
    tools.append(revise_blog.setup())       
    tools.append(publish_blog_html.setup())
    tools.append(publish_blog_md.setup())
    tools.append(save_to_file.setup())
    tools.append(generate_filename_extension.setup())
    return tools

def tools_profiles():
    profiles = []
    profiles.append(create_blog.profile())
    profiles.append(proof_reading_blog.profile())
    profiles.append(revise_blog.profile())
    profiles.append(publish_blog_html.profile())
    profiles.append(publish_blog_md.profile())
    profiles.append(save_to_file.profile())
    profiles.append(generate_filename_extension.profile())
    return profiles


def tool_profile(tool_name):
    profiles = tools_profiles()
    tools = agent_tools()
    for tool in tools:
        if tool.name == tool_name:
            return profiles[tools.index(tool)]
    return None