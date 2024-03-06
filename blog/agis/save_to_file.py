from langchain.agents import tool
import os


def save_file(result, filename):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop') 
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # file_name = f'blog_{timestamp}'
    file_path = os.path.join(desktop_path, filename)
    with open(file_path, 'w') as file:
        file.write(result)
@tool
def save_to_file(result: str, filename: str) -> str:
    """Save the final blog post result using the correct file type."""
    print(f'save_to_file')
    return save_file(result=result,filename=filename)