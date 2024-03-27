from blog.agis import create_blog, generate_filename, generate_image, proof_reading_blog, revise_blog, publish_blog_html, publish_blog_md, save_to_file, search_serper

def agent_tools():
    tools = []
    tools.append(create_blog.setup())
    tools.append(proof_reading_blog.setup()) 
    tools.append(revise_blog.setup())       
    tools.append(publish_blog_html.setup())
    tools.append(publish_blog_md.setup())
    tools.append(save_to_file.setup())
    tools.append(generate_filename.setup())
    tools.append(generate_image.setup())
    tools.append(search_serper.setup())
    return tools

def tools_profiles():
    profiles = []
    tools = agent_tools()
    for tool in tools:
        profiles.append(tool_profile(tool.name))
    return profiles


def tool_profile(tool_name):
    if profile[tool_name]:
        return profile[tool_name]
    return None

profile = {

    "create_blog" : {      
        "name": "create",
        "profile": "Creator",
        "task": "Blog Writing",
        "url": "assets/img/creater.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "proof_reading_blog" : {
        "name": "editor",
        "profile": "Editor",
        "task": "Proof Reading",
        "url": "assets/img/editor.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "revise_blog" : {
        "name": "editor",
        "profile": "Editor",
        "task": "Blog Editer",
        "url": "assets/img/editor.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "publish_blog_html" : {
        "name": "publish",
        "profile": "Publisher",
        "task": "HTML Preping",
        "url": "assets/img/publisher.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "publish_blog_md" : {
          "name": "publish",
        "profile": "Publisher",
        "task": "Markdown Preping",
        "url": "assets/img/publisher.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "save_to_file" : {
        "name": "publish",
        "profile": "Publisher",
        "task": "File Saving",
        "url": "assets/img/publisher.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "generate_filename" : {
        "name": "publish",
        "profile": "Publisher",
        "task": "Blog Naming",
        "url": "assets/img/publisher.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "generate_image" : {
        "name": "generateImage",
        "profile": "Art Illustrator",
        "task": "Image Generation",
        "url": "assets/img/artist.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "search_serper" : {
        "name": "search",
        "profile": "Search",
        "task": "Google Search",
        "url": "assets/img/searcher.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
    "organizer" : {
        "name": "organizer",
        "profile": "Organizer",
        "task": "Orchestration",
        "url": "assets/img/Designer.png",
        "start_message": "Start message placeholder",
        "end_message": "End message placeholder",
        },
}