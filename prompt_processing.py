import json
import google.generativeai as genai
from types import SimpleNamespace

# Initialize the Gemini model
# TODO -> anonymize
genai.configure(api_key='AIzaSyAqoFQLkZ3MUPNRZ_o5gTsOLkk6nGSJIlg')
model = genai.GenerativeModel('gemini-1.5-pro')

# Define language-version mapping
language_versions = {
    "Python": ["3.12", "3.11", "3.10", "3.9", "3.8", "3.7", "2.7"],
    "JavaScript": ["ES2023", "ES2022", "ES2021", "ES2020", "ES2019", "ES2018", "ES6"],
}

def extract_tasks(specification):
    if not specification:
        return None
    extraction_prompt = f"""You are a senior software engineer building a project with the following specification:
    <projectSpecification>
    {specification}
    </projectSpecification>
    Separate each of your tasks ONLY with newlines - do NOT use bullet points or a numbered list. 
    Here is an example of how to format your answer:
    <example>
    Aggregate feedback from surveys.
    Aggregate feedback from social media platforms.
    Perform natural language processing to categorize feedback.
    Detect sentiment in feedback.
    Generate visual reports highlighting common issues.
    Generate visual reports highlighting customer sentiment trends.
    Provide recommendations for product improvements based on analysis.
    </example>
    Tasks:
    """
    # TODO -> query the actual
    # response = model.generate_content(extraction_prompt)
    response = SimpleNamespace()
    response.text = """Design and develop the architecture of the Integrated Development Environment (IDE).
    Implement support for multiple programming languages (Python, Java, C++, JavaScript, etc.) in the IDE.
    Build a user-friendly interface for code editing, debugging, and testing within the IDE.
    Create a project management module with features for task creation, assignment, and tracking.
    Develop a system for monitoring project deadlines and progress, and generating reports.
    Integrate a comprehensive library of research materials, including academic papers and technical articles.
    Implement tools for efficient note-taking, citation management, and collaborative document editing.
    Develop data analysis and visualization tools capable of handling complex datasets.
    Enable users to import, clean, manipulate, and graphically represent data.
    Build features for real-time code sharing, peer review, and remote pair programming.
    Create a platform for users to share their work, projects, and findings with the community.
    Develop automated testing frameworks for different programming languages.
    Implement continuous integration and deployment pipelines for seamless code validation and deployment.
    Curate a library of educational resources, including tutorials, coding challenges, and interactive learning modules.
    Design learning paths and personalize content recommendations based on user skill level and interests.
    Develop a user authentication and authorization system to manage user accounts and permissions.
    Ensure the application is scalable, secure, and performs well under high user loads.
    Implement logging and monitoring systems to track application performance and identify potential issues.
    Conduct thorough testing to ensure all features function as expected and meet quality standards.
    Gather feedback from users and stakeholders to continuously improve the application and its features.
    Stay updated with the latest trends and technologies in software development and incorporate them as needed."""
    # print(response.text)
    return [line.strip() for line in response.text.split('\n') if line.strip()]

def get_libraries(specification, language, version):
    tasks = extract_tasks(specification)
    # TODO -> placeholder
    with open('ex_jtao_out.json') as f:
        api_response = json.load(f)
    markdown_output = ""

    for item in api_response:
        markdown_output += f"## {item['name']}\n\n"
        markdown_output += f"**Description:** {item['description']}\n\n"
        markdown_output += "**Key Features:**\n"
        for feature in item['key_features'].split(", "):
            markdown_output += f"- {feature}\n"
        markdown_output += "\n"

    return markdown_output

def initialize_chat(initial_prompt):
    chat = model.start_chat(history=[])
    chat.send_message(initial_prompt)
    return chat

def get_streaming_response(chat, prompt):
    response = chat.send_message(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text
