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
    print(f'Numer of Tools: {len(tools)} TOOLS: {[tool.name for tool in tools]}')

    return tools